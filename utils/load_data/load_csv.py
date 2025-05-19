import logging
import pandas as pd

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_csv(df, filename="products.csv"):
    """
    Menyimpan DataFrame ke file CSV dengan validasi dasar.

    Args:
    df (pd.DataFrame): DataFrame yang akan disimpan
    filename (str, optional): Nama file CSV. Defaults to "products.csv"

    Raises:
    ValueError: Jika DataFrame kosong atau None
    Exception: Jika terjadi kesalahan saat menulis file
    """

    # Validasi Dataframe
    if df.empty:
        logging.warning("Tidak terdapat data untuk disimpan.")
        return
    
    try:
        # Menyimpan DataFrame ke CSV
        df.to_csv(
            filename, 
            index=False, 
            encoding='utf-8'
        )

        logging.info(f"Data berhasil disimpan di {filename}")

    except Exception as e:
        logging.error(f"Kesalahan saat menyimpan data: {e}")
        raise