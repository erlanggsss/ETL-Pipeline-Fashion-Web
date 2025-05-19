import logging
import pandas as pd
from utils.extract_data.extract import scrape_main
from utils.transform_data.transform import transform_data
from utils.load_data.load_csv import load_csv
from utils.load_data.load_postgre import load_postgre
from utils.load_data.load_sheet import load_sheets

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main(max_retries=3):
    """
    Menjalankan proses Extract, Transform, dan Load (ETL) untuk data produk.

    Args:
    max_retries (int, optional): Jumlah maksimal percobaan ulang jika terjadi kegagalan. 
    efaults to 3.

    Returns:
    pd.DataFrame: DataFrame terakhir setelah proses ETL
    """
    for attempt in range(max_retries):
        try:
            print("\n----------------------------------------------------------------------------------------------------")
            print("Memulai proses ETL")
            print("----------------------------------------------------------------------------------------------------\n")

            # Proses Extract data
            print("----------------------------------------------------------------------------------------------------")
            print("Menjalankan proses Extract")
            print("----------------------------------------------------------------------------------------------------")
            raw_data = scrape_main()
            if not raw_data:
                raise ValueError("Data tidak ditemukan")

            # Proses Transform data
            print("----------------------------------------------------------------------------------------------------")
            print("Menjalankan proses Transformasi")
            print("----------------------------------------------------------------------------------------------------")
            transformed_df = transform_data(raw_data)
            if transformed_df.empty:
                raise ValueError("Data hasil transformasi kosong")

            # Proses Load data
            print("----------------------------------------------------------------------------------------------------")
            print("Menjalankan proses penyimpanan data")
            print("----------------------------------------------------------------------------------------------------")
            load_csv(transformed_df, "fashion_studio.csv")
            load_postgre(transformed_df)
            load_sheets(transformed_df)

            print(f"\nJumlah data setelah ETL: {len(transformed_df)}")
            print("\n----------------------------------------------------------------------------------------------------")
            print("Proses ETL selesai")
            print("----------------------------------------------------------------------------------------------------\n")
            
            return transformed_df

        except ValueError as ve:
            logging.error(f"Kesalahan dalam proses ETL (Percobaan {attempt + 1}): {ve}\n")
            if attempt == max_retries - 1:
                logging.error("Proses ETL gagal setelah semua percobaan\n")
                return pd.DataFrame()
        except Exception as e:
            logging.error(f"Kesalahan tak terduga dalam ETL (Percobaan {attempt + 1}): {e}\n")
            if attempt == max_retries - 1:
                logging.error("Proses ETL gagal setelah semua percobaan\n")
                return pd.DataFrame()

if __name__ == "__main__":
    main()