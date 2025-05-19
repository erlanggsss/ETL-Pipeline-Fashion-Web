import pandas as pd
import logging
# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Konstanta konfigurasi
EXCHANGE_RATE = 16000
REQUIRED_COLUMNS = {"Title", "Price", "Rating", "Colors"}

def validate_input_data(data):
    """
    Memvalidasi data input sebelum transformasi.

    Args:
    data: Data mentah hasil scraping

    Returns:
    bool: True jika data valid, False sebaliknya
    """
    if not data:
        logger.warning("Data kosong")
        return False
    
    # Periksa struktur data
    try:
        df = pd.DataFrame(data)
        missing_columns = REQUIRED_COLUMNS - set(df.columns)
        
        if missing_columns:
            logger.warning(f"Kolom yang hilang: {missing_columns}")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Kesalahan validasi data: {e}")
        return False

def transform_data(data, exchange_rate=EXCHANGE_RATE):
    """
    Membersihkan dan mengubah format data dengan transformasi lanjut.

    Args:
        data: Raw data hasil scraping
        exchange_rate: Nilai tukar mata uang. Default sesuai EXCHANGE_RATE.

    Returns:
        DataFrame: Data yang telah ditransformasi
    """
    # Validasi input data
    if not validate_input_data(data):
        return pd.DataFrame()

    try:
        # Konversi ke DataFrame
        df = pd.DataFrame(data).copy()
        
        # Preprocessing kolom
        df["Price"] = (
            pd.to_numeric(df["Price"], errors="coerce")
            .mul(exchange_rate)
            .round(2)
        )
        
        # Transformasi Rating
        df["Rating"] = (
            df["Rating"]
            .astype(str)
            .str.extract(r"([\d.]+)")
            .astype(float)
        )
        df.dropna(
            subset=["Rating"], 
            inplace=True
        )
        
        # Transformasi Colors
        df["Colors"] = (
            pd.to_numeric(df["Colors"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)       
        
        df = df[df["Title"] != "Unknown Product"]
        
        logger.info(f"Transformasi selesai. Total data: {len(df)}\n")
        return df

    except Exception as e:
        logger.error(f"Kesalahan proses transformasi: {e}")
        return pd.DataFrame()
