# Google Drive Client APP
Client application to sync/backup files to Google Drive cloud storage

## Initial idea
- File backups
- Scheduled backups or automatic triggers
- Operation logging

## On the works
- Study the Google Drive API
- Indexing local files
- File changes/backup triggers

## Requirements

- Run `pip3 install -r requirements.txt`
- Go to [Enable API](https://console.developers.google.com/apis) and select Google Drive API from the list
- Create a New Project and create the credentials
- Save the *credentials.json* file in secrets/credentials/
- An authentication token will be created with the necessary information in secrets/token/

> The *credentials.json* is required to authenticate the application

## Project Structure
```
├── LICENSE
├── README.md
├── ToDo.md
├── app
│   └── __init__.py
├── db
│   └── fileids.db
├── gdrive_test
│   ├── file1.txt
│   └── file2.txt
├── interfaces
│   ├── __init__.py
│   └── log_files_interface.py
├── models
│   ├── __init__.py
│   └── file_schema.py
├── precommit.sh
├── requirements.txt
├── secrets
│   ├── credentials
│   │   └── credentials.json
│   └── token
│       └── token.pickle
├── setup.py
├── start.py
└── tests
    ├── __init__.py
    └── test_unit.py
```
## Commands

Run `python3 start.py` to test out the program.

## Sources
- Google Drive API [Examples](https://developers.google.com/drive/api/v3/manage-uploads) and [Documentation](https://developers.google.com/drive/api/v3/reference/files/create)
- Python client [Github Docs](https://github.com/googleapis/google-api-python-client/tree/master/docs)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
**Henry Valbuena**