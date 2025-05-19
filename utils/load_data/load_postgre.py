import psycopg2
import pandas as pd
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Konfigurasi database
DB_CONFIG = {
    "dbname": "fashiondb",
    "user": "fashionsdb",
    "password": "inipassword",
    "host": "localhost",
    "port": "5432"
}

def load_postgre(df, table_name="products"):
    """
    Menyimpan DataFrame kedalam PostgreSQL
    
    Args:
    df (pd.DataFrame): DataFrame yang akan dimuat
    table_name (str, optional): Nama tabel. Defaults to "products"
    
    Returns:
    None
    """
    if df.empty:
        logging.warning("Tidak terdapat data untuk dimasukkan ke PostgreSQL.")
        return 
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            price FLOAT,
            rating FLOAT,
            colors INT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
        );
        """
        cursor.execute(create_table_query)

        insert_query = f"""
        INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (title) DO UPDATE 
        SET price = EXCLUDED.price,
            rating = EXCLUDED.rating,
            colors = EXCLUDED.colors,
            size = EXCLUDED.size,
            gender = EXCLUDED.gender,
            timestamp = EXCLUDED.timestamp;
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Data berhasil ditambahkan kedalam database postgre pada tabel {table_name}.")
    
    except Exception as e:
        logging.error(f"Kesalahan saat menyimpan ke PostgreSQL: {e}")