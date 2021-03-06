from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    ]

def authenticate():
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
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.

    Args
    service: Authenticated service token, call authenticate for this parameter
    """
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def upload_file(service):    
    file_metadata = {'name': 'file1.txt'}
    media = MediaFileUpload('gdrive_test/file1.txt')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def multi_upload(file_list: str, service):
    """Prints the file IDs of the files uploaded

    Args
    files: list of files to be uploaded
    services: Authenticated service token, call authenticate for this parameter
    """
    for f in file_list:
        media = MediaFileUpload(f['file_path'])
        file = service.files().create(body=f['metadata'],
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

def main():
    # Create service
    service = build('drive', 'v3', credentials=authenticate())
    print('Service created')

    # File list
    file_list = [
        {'metadata': {'name': 'file1.txt', 'parents': ['12SF5xkNeW7Q-jA9sFwH9SWmjMO600ZK0']}, 'file_path': 'gdrive_test/file1.txt'},
        {'metadata': {'name': 'file2.txt', 'parents': ['12SF5xkNeW7Q-jA9sFwH9SWmjMO600ZK0']}, 'file_path': 'gdrive_test/file2.txt'},
    ]
    # List files in GDrive
    list_files(service)
    # Upload files
    # multi_upload(file_list, service)


if __name__ == '__main__':
    main()