import os

from typing import Optional

import supervisely as sly

from dotenv import load_dotenv

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()

SLY_APP_DATA_DIR = sly.app.get_data_dir()
IMAGES_TMP_DIR = "images"
CUSTOM_DATA_KEY = "Pexels downloader"


PEXELS_API_URL = "https://api.pexels.com"
PEXELS_API_ENDPOINTS = {
    "images": "v1/search",
    "videos": "videos/search",
}
app_mode = PEXELS_API_ENDPOINTS.keys()[0]  # Default to images mode


def get_pexels_api_url() -> str:
    """Returns the Pexels API URL based on the current mode (images or videos).

    Returns:
        str: Pexels API URL for images or videos.
    """
    endpoint = PEXELS_API_ENDPOINTS[app_mode]
    if not endpoint:
        raise ValueError(
            f"Invalid app mode: {app_mode}. Available modes: {list(PEXELS_API_ENDPOINTS.keys())}"
        )
    return f"{PEXELS_API_URL}/{endpoint}"


MIN_FILE_SIZE = 1 * 1024  # 1 KB

# Settings for images search and metadata fields.
IMAGES_PER_PAGE = 80

IMAGE_SIZES = ["original", "large2x", "large", "medium", "small", "tiny"]

REQUIRED_METADATA_FIELDS = {
    "Source URL": "url",
    "License": "license",
    "Photographer name": "photographer",
}
OPTIONAL_METADATA_FIELDS = {
    "Photographer Pexels ID": "photographer_id",
    "Photographer URL": "photographer_url",
    "Image description": "alt",
}
# Download types for images.
DOWNLOAD_TYPES = {
    "files": "Copy source file to the Supervisely dataset",
    "links": "Add link to source image in the Supervisely dataset",
}
ALLOWED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]


def key_from_file() -> Optional[str]:
    """Tries to load Pexels API key from the team files.

    Returns:
        Optional[str]: returns Pexels API key if it was loaded successfully, None otherwise.
    """
    try:
        # Get pexels.env from the team files.
        INPUT_FILE = sly.env.file(True)
        api.file.download(TEAM_ID, INPUT_FILE, "pexels.env")

        # Read Pexels API key from the file.
        load_dotenv("pexels.env")
        PEXELS_API_KEY = os.environ["PEXELS_API_KEY"]

        sly.logger.info("Pexel API key was loaded from the team files.")
        return PEXELS_API_KEY
    except Exception as error:
        sly.logger.debug(
            f"Pexel API key was not loaded from the team files with error: {error}.)"
        )
