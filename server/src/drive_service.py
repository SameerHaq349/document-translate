import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

def upload_file_to_drive(file_path, name):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    
    # Define the metadata and set the MIME type to convert to Google Slides
    file_metadata = {
        "name": name,  # Use the original file name
        "mimeType": "application/vnd.google-apps.presentation",  # Convert to Google Slides
    }
    
    # Upload the PPTX file with the correct MIME type
    media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation", resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    return file.get("id")

def download_file_from_drive(file_id):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    
    # Set the file permissions to be publicly accessible
    drive_service.permissions().create(
        fileId=file_id, 
        body={"type": "anyone", "role": "reader"}
    ).execute()
    
    # Generate a direct download link for the PPTX file
    link = f"https://docs.google.com/presentation/d/{file_id}/export/pptx"
    
    return link, "translated_presentation.pptx"

def upload_image_to_drive(image_path):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    
    # Define metadata and upload the image
    photo_metadata = {"name": os.path.basename(image_path)}
    media = MediaFileUpload(image_path, mimetype="image/jpeg", resumable=True)
    photo = drive_service.files().create(body=photo_metadata, media_body=media, fields="id").execute()
    
    return photo.get("id")

def get_image_link(file_id):
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    
    # Set file permissions to be publicly accessible
    drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
    
    # Retrieve the web content link for the image
    file = drive_service.files().get(fileId=file_id, fields='webContentLink').execute()
    
    return file.get('webContentLink')

# Ensure that credentials are valid when the script is run
get_creds()
