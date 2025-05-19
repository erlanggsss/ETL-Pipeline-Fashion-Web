import unittest
import pandas as pd
from utils.transform_data.transform import transform_data

class TestTransformData(unittest.TestCase):
    """Unit test for transform_data function."""

    def setUp(self):
        """Preparing data test."""
        self.valid_data = [
            {"Title": "Product A", "Price": "10", "Rating": "4.5⭐", "Colors": "3"},
            {"Title": "Product B", "Price": "20", "Rating": "3.0⭐", "Colors": "2"},
        ]
        self.invalid_data = [
            {"Title": "Unknown Product", "Price": "10", "Rating": "4.5⭐", "Colors": "3"},
            {"Title": "Product C", "Price": None, "Rating": None, "Colors": None},
        ]

    def test_transform_valid_data(self):
        """The valid data transformation test produces a valid DataFrame."""
        df = transform_data(self.valid_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("Price", df.columns)
        self.assertIn("Rating", df.columns)

    def test_transform_invalid_data(self):
        """Test data is invalid or empty resulting in an empty DataFrame."""
        df = transform_data([])
        self.assertTrue(df.empty)

        df_invalid = transform_data(self.invalid_data)
        self.assertTrue(df_invalid.empty)

if __name__ == "__main__":
    unittest.main()
