import pickle
import os.path
import ntpath
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import sys
from pathlib import Path
from googleapiclient.http import MediaFileUpload
import PythonValues

#Google api scope
SCOPES = ['https://www.googleapis.com/auth/drive']


def main(file_to_backup):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #sys.path[0] is folder where script is stored on drive
    if os.path.exists(sys.path[0]+'/token.pickle'):
        with open(sys.path[0]+'/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                sys.path[0]+'/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sys.path[0]+'/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    # Call the Drive v3 API
    drive_client = service.files()
    #folder id can be obtained from google drive link to your folder
    #PythonValues is another file where i store id, you can paste your id here
    folder_id = PythonValues.folder_ids
    file_trg = ntpath.basename(file_to_backup)

#here you put name, that you want your file to have after upload and folder_id where your file should be stored
    file_metadata = {'name': file_trg,
                     'parents': [folder_id]}

#here you put file to backup, with full path
    media = MediaFileUpload(file_to_backup,
                            mimetype='application/x-7z-compressed',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                               media_body=media,
                                  fields='id').execute()
    print ('File ID: %s' % file.get('id'))


if __name__ == '__main__':
#take file list from source folder and orders them by modification date
    paths = sorted(Path(PythonValues.sourcefoldername).iterdir(), key=os.path.getmtime)
#take the last file from list
    print(paths[-1:][0])
    print(ntpath.basename(paths[-1:][0]))
    print(sys.path[0])
    #main(paths[-1:][0])