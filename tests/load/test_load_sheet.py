import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_sheet import load_sheets

class TestLoadSheet(unittest.TestCase):
    @patch("utils.load_data.load_sheet.service_account.Credentials")
    @patch("utils.load_data.load_sheet.build")
    def test_load_sheet_success(self, mock_build, mock_credentials):
        """Test berhasil unggah ke Google Sheets."""
        df = pd.DataFrame({
            "title": ["Item A"],
            "price": [100],
            "rating": [4.5],
            "colors": [2],
            "size": ["M"],
            "gender": ["Unisex"],
            "timestamp": ["2024-01-01 10:00:00"]
        })

        mock_creds_instance = MagicMock()
        mock_credentials.from_service_account_file.return_value = mock_creds_instance

        mock_service = MagicMock()
        mock_request = MagicMock()
        mock_request.execute.return_value = {"updatedCells": 14}

        mock_service.spreadsheets.return_value.values.return_value.update.return_value = mock_request
        mock_build.return_value = mock_service

        response = load_sheets(df)

        assert response == {"updatedCells": 14}
        mock_build.assert_called_once()