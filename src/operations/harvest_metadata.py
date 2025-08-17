"""
ATTENTION (2025-08-17)
Google has restricted the Google Photos API severely in 2025, so this operation will not work anymore.
https://developers.google.com/photos/support/updates?utm_source=chatgpt.com#affected-scopes-methods

---

you can download your own picture and their metadata from google photos using google takeout
this does not work on shared albums (e.g. holidays) because you can only download your own pictures

you can download all pictures by downloading them through google photos, however if you download them this way
you get a zip file of pictures where every picture has a mtime = time of download, with no json sidecar file

this operation scrapes the mtimes from google using the google api, and overwrites the mtimes of the downloaded files

this uses the google photos api so you will need to set up a project in the google cloud console and get a token
- Go to: Google Cloud Console
- Create or select a project.
- Navigate to APIs & Services > Library.
- Search for Google Photos Library API and enable it.
- Navigate to APIs & Services > Credentials
- Click on Create Credentials > OAuth client ID:
- Application type: Desktop App
- Name: Photos API Client
- Download the credentials.json file.
- Make sure you have set yourself up as a test user.
"""
import os.path
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

google_api_token_file_path = '../settings/google__photos_api_token.pkl'


def harvest_metadata_for_folder_path_operation(folder_path: str, album_name: str, client_secret_json_file_path: str,
                                               callback) -> None:
    """
    Entrypoint for the harvest metdata operation that accepts a folder path as input.
    It tries to match all files in the folder with the metadata from the Google Photos images.
    """
    if os.path.exists(folder_path):
        callback(f"Starting to harvest metadata for folder: {folder_path}", 0)
        list_of_file_names = os.listdir(folder_path)
        list_of_file_paths = [os.path.join(folder_path, file_name) for file_name in list_of_file_names
                              if os.path.isfile(os.path.join(folder_path, file_name))]
        harvest_metadata_for_file_list_operation(list_of_file_paths, album_name, client_secret_json_file_path, callback)


def harvest_metadata_for_file_list_operation(list_of_file_paths: list[str],
                                             album_name: str,
                                             client_secret_json_file_path: str,
                                             callback) -> None:
    callback("Google restricted the Google Photos API severely in 2025, so this operation will not work anymore.", 100)
    return
    # keep old code for future reference

    photos_api_service_object = authenticate_at_google_photos(client_secret_json_file_path)
    if photos_api_service_object is None:
        callback("Failed to authenticate with Google Photos API.", 100)
        return

    metadata = get_metadata_from_google_photos_via_api(list_of_file_paths, album_name, photos_api_service_object,
                                                       callback)
    write_metadata_to_images(list_of_file_paths, metadata, callback)
    callback("Finished.", 100)


def authenticate_at_google_photos(client_secret_json_file_path: str):
    """
    Authenticate the user and return the Google Photos API service object.
    :return: google resource service object
    """
    scopes = ['https://www.googleapis.com/auth/photoslibrary']

    creds = None
    if os.path.exists(google_api_token_file_path):
        with open(google_api_token_file_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_json_file_path, scopes)
            creds = flow.run_local_server(port=0)

        with open(google_api_token_file_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)


def get_metadata_from_google_photos_via_api(list_of_file_paths: list[str], album_name: str,
                                            photos_api_service_object, callback) -> dict[str, str]:
    album_id = get_album_id(photos_api_service_object, album_name)
    if not album_id:
        callback(f"Album '{album_name}' not found in your google photos library.", 100)
        return

    callback("Fetching media items from online album...", 0)
    media_items = list_media_items_in_album(photos_api_service_object, album_id)
    total_media_items = len(media_items)
    if not media_items:
        callback("No media items found in the album.", 100)
        return
    else:
        callback(f"Found {total_media_items} items.", 100)

    # write a dict with keys = filenames and values = creation times
    metadata = {item['filename']: item.get('mediaMetadata', {}).get('creationTime') for item in media_items}
    return metadata


def get_album_id(service, album_title):
    albums = []
    next_page_token = None

    while True:
        results = service.albums().list(
            pageSize=50, pageToken=next_page_token
        ).execute()
        albums.extend(results.get('albums', []))
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    for album in albums:
        if album['title'] == album_title:
            return album['id']

    return None


def list_media_items_in_album(photos_api_service_object, album_id):
    """Build a list of media items in a given album. Handles pagination."""
    media_items = []
    next_page_token = None

    while True:
        response = photos_api_service_object.mediaItems().search(
            body={
                "albumId": album_id,
                "pageSize": 100,
                "pageToken": next_page_token
            }
        ).execute()

        items = response.get('mediaItems', [])
        media_items.extend(items)
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return media_items


def write_metadata_to_images(list_of_file_paths: list[str], metadata: dict[str, str], callback) -> None:
    # Convert ISO timestamp to epoch
    callback("Converting ISO timestamps to epoch times...", 0)
    metadata_with_ts = {}
    for key, value in metadata.items():
        if value:
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                metadata_with_ts[key] = dt.timestamp()
            except ValueError as e:
                callback(f"Could not parse date for {key}: {e}")
                metadata_with_ts[key] = None

    # Walk through the folder and apply mtimes
    callback("Modifying file mtimes based on metadata...", 0)
    total_files = len(list_of_file_paths)
    for i, file_path in enumerate(list_of_file_paths):
        file_name = os.path.basename(file_path)
        if file_name in metadata_with_ts:
            epoch_time = metadata_with_ts[file_name]
            try:
                os.utime(file_path, (epoch_time, epoch_time))  # atime, mtime
                callback("Updating file: " + file_name, int(100 * i / total_files))
            except Exception as e:
                print(f"Failed to update {file_name}: {e}")
