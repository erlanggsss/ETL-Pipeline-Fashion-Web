import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_postgre import load_postgre

class TestLoadPostgre(unittest.TestCase):
    @patch("utils.load_data.load_postgre.psycopg2.connect")
    def test_load_postgre_success(self, mock_connect):
        """Test successfully saved to PostgreSQL."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        df = pd.DataFrame({
            "title": ["Item A"],
            "price": [100],
            "rating": [4.5],
            "colors": [2],
            "size": ["M"],
            "gender": ["Unisex"],
            "timestamp": ["2024-01-01 10:00:00"]
        })

        load_postgre(df, table_name="test_products")

        mock_cursor.execute.assert_called()  
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()