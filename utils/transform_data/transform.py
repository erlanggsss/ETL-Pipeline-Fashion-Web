import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration constants
EXCHANGE_RATE = 16000
REQUIRED_COLUMNS = {"Title", "Price", "Rating", "Colors"}

def validate_input_data(data):
    """
    Validate input data before transformation.

    Args:
    data: Raw data scraping result

    Returns:
    bool: True if data is valid, False otherwise
    """
    if not data:
        logger.warning("Data kosong")
        return False
    
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
    Clean and transform data with advanced transformations.

    Args:
    data: Raw data scraped
    exchange_rate: Currency exchange rate. Defaults to EXCHANGE_RATE.

    Returns:
    DataFrame: Transformed data
    """
    # Validate input data
    if not validate_input_data(data):
        return pd.DataFrame()

    try:
        # Convert into Dataframe
        df = pd.DataFrame(data).copy()
        
        # Exchange Dollars into Rupiah
        df["Price"] = (
            pd.to_numeric(df["Price"], errors="coerce")
            .mul(exchange_rate)
            .round(2)
        )
        
        #  Rating Transformation
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
        
        # Colors Transformation
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
