import logging
import pandas as pd

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_csv(df, filename="products.csv"):
    """
    Saves a DataFrame to a CSV file with basic validation.

    Args:
    df (pd.DataFrame): The DataFrame to save
    filename (str, optional): The name of the CSV file. Defaults to "products.csv"

    Raises:
    ValueError: If the DataFrame is empty or None
    Exception: If an error occurred while writing the file
    """

    # Dataframe validation
    if df.empty:
        logging.warning("Tidak terdapat data untuk disimpan.")
        return
    
    try:
        # Saving Dataframe into csv
        df.to_csv(
            filename, 
            index=False, 
            encoding='utf-8'
        )

        logging.info(f"Data berhasil disimpan di {filename}")

    except Exception as e:
        logging.error(f"Kesalahan saat menyimpan data: {e}")
        raise