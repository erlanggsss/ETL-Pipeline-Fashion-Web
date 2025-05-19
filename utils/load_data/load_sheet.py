import pandas as pd
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Konfigurasi logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

SPREADSHEET_ID = "1EUa65GLeKgyEoZMAnOvYIj4DdctIzn4f_MSKijFxVVQ"
SHEET_NAME = "Sheet1"

def load_sheets(df: pd.DataFrame):
    """
    Mengunggah dataframe ke Google Sheets

    Args:
    df (pd.DataFrame): DataFrame yang akan diunggah
    config (Dict[str, str], optional): Konfigurasi Google Sheets. 
    Defaults to SPREADSHEET_CONFIG.

    Returns:
    dict | None: Respons dari API Google Sheets jika berhasil, None jika terjadi kesalahan.
    """
    if df.empty:
        logger.warning("Tidak terdapat data untuk diunggah ke Google Sheets.")
        return
    
    try:
        # Autentikasi menggunakan service account
        creds = service_account.Credentials.from_service_account_file(
        "google-sheets-api.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
       
       # Inisialisasi layanan Google Sheets
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Persiapan data
        values = [df.columns.tolist()] + df.values.tolist()
        
        # Eksekusi request
        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption="RAW",
            body={"values": values}
        )

        # Mengirim request dan menerima respons
        response = request.execute()

        logger.info("Data berhasil diunggah ke Google Sheets")
        return response

    except Exception as e:
        logger.error(f"Kesalahan saat mengunggah ke Google Sheets: {e}")
        return None