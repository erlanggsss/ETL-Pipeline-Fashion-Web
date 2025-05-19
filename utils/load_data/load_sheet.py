import pandas as pd
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

SPREADSHEET_ID = "[SHEET_ID]"
SHEET_NAME = "[SHEET_NAME]"

def load_sheets(df: pd.DataFrame):
    """
    Uploading a dataframe to Google Sheets

    Args:
    df (pd.DataFrame): DataFrame to upload
    config (Dict[str, str], optional): Google Sheets configuration.
    Defaults to SPREADSHEET_CONFIG.

    Returns:
    dict | None: Response from Google Sheets API on success, None on error.
    """
    if df.empty:
        logger.warning("Tidak terdapat data untuk diunggah ke Google Sheets.")
        return
    
    try:
        # Authentication Spredsheet using service account
        creds = service_account.Credentials.from_service_account_file(
        "google-sheets-api.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
       
       # Initiate Google Sheet service
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Data Preparation
        values = [df.columns.tolist()] + df.values.tolist()
        
        # Request execution
        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption="RAW",
            body={"values": values}
        )

        # Send request and receive response
        response = request.execute()

        logger.info("Data berhasil diunggah ke Google Sheets")
        return response

    except Exception as e:
        logger.error(f"Kesalahan saat mengunggah ke Google Sheets: {e}")
        return None