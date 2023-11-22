import pprint

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_drive_service():
    # Crear las credenciales a partir del archivo JSON descargado
    creds = service_account.Credentials.from_service_account_file(
        "./configuration/credentials.json", scopes=["https://www.googleapis.com/auth/drive"]
    )

    # Crear el cliente que interactúa con la API de Google Drive
    service = build("drive", "v3", credentials=creds)

    return service


def change_file_settings(service, file_id):
    try:
        file_metadata = {"copyRequiresWriterPermission": True, "viewersCanCopyContent": False, "writersCanShare": True}
        service.files().update(fileId=file_id, body=file_metadata).execute()
    except Exception as e:
        print("➡ Fallo en :", e)


def delete_file(service, file_id):
    try:
        service.files().delete(fileId=file_id).execute()
    except Exception as e:
        print("➡ Fallo en :", e)


def get_id_from_url(url):
    start_index = url.find("=") + 1
    end_index = url.find("&")
    return url[start_index:end_index]
