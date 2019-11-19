"""Start program."""

from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    ]
FILE_IDS = 'file_ids.txt'
DEBUG = True


def authenticate():
    """Authenticate the transaction."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def list_files(service):
    """Show basic usage of the Drive v3 API.

    Prints the names and ids of the first 10 files the user has access to.

    Args:
        service: Authenticated service token, call authenticate for this
        parameter

    """
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, size)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) {2}'.format(
                item['name'],
                item['id'],
                item['size'] if 'size' in item else 'None'))


def upload_file(service):
    """Upload a file to gdrive.

    Uploads a file to gdrive based on the service passed.

    Args:
        service: Authenticated service token, call authenticate for this
        parameter

    """
    if DEBUG is not True:
        file_metadata = {'name': 'file1.txt'}
        media = MediaFileUpload('gdrive_test/file1.txt')
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print('File ID: %s' % file.get('id'))


def multi_upload(file_list, service):
    """Print the file IDs of the files uploaded.

    Upload multiple files from the list to the service.

    Args:
        files: list of files to be uploaded
        services: Authenticated service token, call authenticate for this
        parameter

    """
    if DEBUG is not True:
        for f in file_list:
            media = MediaFileUpload(f['file_path'])
            file = service.files().create(body=f['metadata'],
                                          media_body=media,
                                          fields='id').execute()
            print('File ID: %s' % file.get('id'))


def main():
    """Entry method from the program."""
    # Create service
    service = build('drive', 'v3', credentials=authenticate())
    print('Service created')

    # File list
    file_list = [
        {
            'metadata': {
                'name': 'file1.txt',
                'parents': ['1VxScqKnZhPBTz_isnnBvDQfQ_I1KVh8L']
                },
            'file_path': 'gdrive_test/file1.txt'
        },
        {
            'metadata': {
                'name': 'file2.txt',
                'parents': ['1VxScqKnZhPBTz_isnnBvDQfQ_I1KVh8L']
                },
            'file_path': 'gdrive_test/file2.txt'
        },
    ]
    # List files in GDrive
    list_files(service)
    # Upload files
    multi_upload(file_list, service)


if __name__ == '__main__':
    main()
