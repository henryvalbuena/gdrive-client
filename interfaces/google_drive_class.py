"""Google Drive interface module."""

from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DEBUG = False


class GDRIVE:
    """Google Drive interface class."""

    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
    ]
    SECRETS_TOKEN = 'secrets/token/token.pickle'
    SECRETS_CRED = 'secrets/credentials/credentials.json'

    def __init__(self):
        """Initialize credentials and build service."""
        # create credentials and build the service
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.SECRETS_TOKEN):
            with open(self.SECRETS_TOKEN, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.SECRETS_CRED, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.SECRETS_TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        self._service = build('drive', 'v3', credentials=creds)

    def list_drive_files(self):
        """List all the files currently present in Google Drive.

        Returns:
            List of files with details

        """
        results = self._service.files().list(
            # pageSize=10, fields="nextPageToken, files(id, name, size, mimeType, parents)").execute()
            fields='files(id,name,size,mimeType,parents)').execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return list()
        else:
            if DEBUG:
                print('Files:')
                for item in items:
                    print(u'{0} ({1}) {2}'.format(
                        item['name'],
                        item['id'],
                        item['size'] if 'size' in item else 'None'),
                        item['mimeType'],
                        item['parents'])
            return items

    def create_new_folder(self, filename, parents=[]):
        """Create a new folder with the specified name and within the parents.

        Args:
            filename: name of the file to be created
            parents: parent folder id if any

        Returns:
            File resource with metadata

        """
        return self._service.files().create(
            body={
                'name': filename,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': parents
            },
            fields='id'
        ).execute()

    def create_new_file(self, filename, parents=[]):
        """Create a new file with the specified name inside the parent directory.

        Args:
            filename: name of the file to be created
            parents: parent folder id if any

        Returns:
            File resource with metadata

        """
        return self._service.files().create(
            body={
                'name': filename,
                'parents': parents
            },
            fields='id'
        ).execute()

    def delete_file(self, fileId):
        """Delete a file or files permanently.

        Args:
            fileId: this is the id provided by google drive

        """
        self._service.files().delete(fileId=fileId).execute()

    def update_file(self, file_descriptor):
        """Update an existing file in Google Drive.

        Args:
            file_descriptor: contains file metadata to be updated

            Example:
                file_descriptor = {
                    'fileId': 'id',
                    'media': 'file_path'
                }

        """
        return self._service.files().update(
            fileId=file_descriptor['fileId'],
            body={
                'fileId': file_descriptor['fileId'],
                'name': file_descriptor['name']
            },
            media_body=MediaFileUpload(file_descriptor['media']),
            fields='id,name,parents'
        ).execute()


if DEBUG:
    # TESTING
    gd = GDRIVE()

    gd.list_drive_files()

    # print('\nCreating directory')
    # dir2 = gd.create_new_folder(filename='dir2', parents=['15Yca5J2LY0_7YIa9ub6lwZmhcBvPdkXi'])
    # print('Creating another directory\n')
    # dir3 = gd.create_new_folder(filename='dir3', parents=[dir2['id']])
    # print('Creating another directory\n')
    # dir4 = gd.create_new_folder(filename='dir4', parents=[dir3['id']])
    # print('Creating a new file id dir4')
    # gd.create_new_file(filename='f4.txt', parents=[dir4['id']])

    print('DELETING FILES')
    files = [
        '1uV-1gu7azs4oYhqjXGAA-eZcuObEZSAv',
        '1ZN-hqhq7nX0ZEfcSzp0vXRSVEFNeUQAX',
        '1fv3nE1vp7rsuw95pNwlDVgi_Qu-9owfk'
    ]
    for fid in files:
        gd.delete_file(fileId=fid)
    print('FILES DELETED')

    gd.list_drive_files()
