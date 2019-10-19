# Google Drive Client APP
Client application to sync/backup files to Google Drive cloud storage

## Initial idea
- Create a Python program that will be executed on a Linux platform
- The program will automatically sync the file changes with the cloud storage
- It will log the operations

## On the works
- Study the Google Drive API
- Proof of Concept

## Requirements

- Run `pip3 install -r requirements.txt`
- Go to [Enable API](https://console.developers.google.com/apis) and select Google Drive API from the list
- Create a New Project and create the credentials
- Save the *credentials.json* file in the same directory the program will be located

> The *credentials.json* is required to authenticate the application

## Commands

Run `python3 start.py` to test out the program.

## Sources
- Google Drive API [Examples](https://developers.google.com/drive/api/v3/manage-uploads) and [Documentation](https://developers.google.com/drive/api/v3/reference/files/create)
- Python client [Github Docs](https://github.com/googleapis/google-api-python-client/tree/master/docs)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
**Henry Valbuena**