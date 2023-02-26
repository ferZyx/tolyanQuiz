from __future__ import print_function

import base64
import io
import os
import shutil
import zipfile

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# Replace this with the path to your service account key file
service_account_file = 'service_account.json'

# Authorize using the service account
creds = Credentials.from_service_account_file(service_account_file)

# Build the Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def download_file(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    with open(f'downloaded_file.docx', 'wb') as f:
        f.write(file.getvalue())

    return file.getvalue()


def upload_with_conversion(filepath: str):
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': f'index',
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        media = MediaFileUpload(filepath,
                                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File with ID: "{file.get("id")}" has been uploaded.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


def export_as_html_zip(real_file_id, filepath):
    """Download a Document file in HTML(ZIP) format.
    Args:
        real_file_id : file ID of any workspace document format file
        filepath : path to save a zip
    Returns : IO object with location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='application/zip')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    with open(f'{filepath}', 'wb') as f:
        f.write(file.getvalue())

    return file.getvalue()


def get_questions_count(real_file_id):
    """Download a Document file in HTML(ZIP) format.
    Args:
        real_file_id : file ID of any workspace document format file
    Returns : IO object with location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='text/plain')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    file_text = str(file.getvalue())
    return file_text.count('<question>')


def make_single_html_file(zip_path, base_dir, username):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(f'{base_dir}/mainQuizApp/temp/{username}')
    os.remove(zip_path)
    html_file = f'{base_dir}/mainQuizApp/temp/{username}/index.html'
    img_folder = f'{base_dir}/mainQuizApp/temp/{username}//images'
    with open(html_file, "r") as f:
        html_content = f.read()
    if os.path.isdir(img_folder):
        for filename in os.listdir(img_folder):
            with open(os.path.join(img_folder, filename), "rb") as f:
                img_content = f.read()
            img_b64 = base64.b64encode(img_content).decode()
            html_content = html_content.replace(f'src="images/{filename}"',
                                                f"src='data:image/{filename.split('.')[-1]};base64,{img_b64}'")
        shutil.rmtree(f'{base_dir}/mainQuizApp/temp/{username}/images')
        with open(html_file, "w") as f:
            f.write(html_content)


if __name__ == '__main__':
    doc_id = '1x_AXkWo0H6fcgA-aBpZ2k7ya7bSe4dXNsNotsOfjFGg'
    print(get_questions_count(doc_id))
