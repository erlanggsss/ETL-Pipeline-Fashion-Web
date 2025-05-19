import unittest
from unittest.mock import patch, Mock
from utils.extract_data.extract import scrape_page, generate_urls, scrape_main


class TestScrapePage(unittest.TestCase):
    """Unit test untuk fungsi scrape_page."""

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_success(self, mock_get):
        """Menguji hasil scrape_page ketika response sukses dan struktur HTML sesuai."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html><body>
            <div class="collection-card">
                <h3 class="product-title">Baju</h3>
                <span class="price">$100</span>
                <p>Rating: ⭐4.5</p>
                <p>Colors: Merah</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
        </body></html>
        '''
        mock_get.return_value = mock_response

        result = scrape_page("http://example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Baju")
        self.assertEqual(result[0]["Price"], "100")
        self.assertEqual(result[0]["Rating"], "4.5")
        self.assertEqual(result[0]["Colors"], "Merah")
        self.assertEqual(result[0]["Size"], "M")
        self.assertEqual(result[0]["Gender"], "Unisex")


class TestGenerateUrls(unittest.TestCase):
    """Unit test untuk fungsi generate_urls."""

    def test_generate_urls_multiple_pages(self):
        """Menguji generate_urls menghasilkan daftar URL sesuai jumlah halaman."""
        urls = generate_urls(3)
        expected_urls = [
            "https://fashion-studio.dicoding.dev/",
            "https://fashion-studio.dicoding.dev/page2",
            "https://fashion-studio.dicoding.dev/page3"
        ]
        self.assertEqual(urls, expected_urls)


class TestScrapeMain(unittest.TestCase):
    """Unit test untuk fungsi scrape_main."""

    @patch("utils.extract_data.extract.scrape_page", return_value=[{"Title": "Mock"}])
    def test_scrape_main_returns_data(self, mock_scrape):
        """Menguji scrape_main dapat mengembalikan hasil dari beberapa halaman mock."""
        result = scrape_main(2)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
