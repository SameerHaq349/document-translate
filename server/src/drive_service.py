import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/presentations"]

def get_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def upload_file_to_drive(file_path):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": os.path.basename(file_path),
        "mimeType": "application/vnd.google-apps.presentation",
    }
    media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation", resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def download_file_from_drive(file_id):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    #request = drive_service.files().export_media(fileId=file_id, mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    drive_service.permissions().create(fileId=file_id,body={"type": "anyone","value":"anyone", "role":"reader"}).execute()
    request = drive_service.files().get(fileId=file_id).execute()
    link_id = request['id']
    link = "docs.google.com/presentation/d/" + link_id + "/export/pptx"
    '''
    print("request", request)
    final_file = io.BytesIO()
    downloader = MediaIoBaseDownload(final_file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    final_file.seek(0)
    print("request", request)
    print("final_file", final_file)
    print("downloader", downloader)
    print("seek", final_file.seek(0))
    '''
    return link, "translated_presentation.pptx"

def upload_image_to_drive(image_path):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    photo_metadata = {"name": os.path.basename(image_path)}
    media = MediaFileUpload(image_path, mimetype="image/jpeg", resumable=True)
    photo = drive_service.files().create(body=photo_metadata, media_body=media, fields="id").execute()
    return photo.get("id")

def get_image_link(file_id):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    permission = {'type': 'anyone', 'role': 'reader'}
    drive_service.permissions().create(fileId=file_id, body=permission).execute()
    file = drive_service.files().get(fileId=file_id, fields='webViewLink, webContentLink').execute()
    return file.get('webContentLink')



get_creds()