import unittest
import pandas as pd
import os
import tempfile
from utils.load_data.load_csv import load_csv

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Setup temporary files for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        # Delete files after testing is complete
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_data_success(self):
        # Testing whether the data was successfully saved to a CSV file
        data = {
            "Title": ["Product A"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        load_csv(df, self.filename)
        
        self.assertTrue(os.path.exists(self.filename))

        df_loaded = pd.read_csv(self.filename)
        pd.testing.assert_frame_equal(df, df_loaded, check_dtype=False)

    def test_load_data_failure(self):
        # Test whether exceptions are handled correctly if the path is invalid.
        data = {
            "Title": ["Product A"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        invalid_filename = "/invalid_path/test_fashion_data.csv"

        with self.assertRaises(Exception):
            load_csv(df, invalid_filename)

if __name__ == "__main__":
    unittest.main()