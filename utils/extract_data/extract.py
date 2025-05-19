import time
import logging
import requests
import datetime
import concurrent.futures
from typing import List, Dict
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_PAGES_LIMIT = 50
MAX_WORKERS = 10 

def scrape_page(url: str) -> List[Dict[str, str]]:
    """
    Fetch product data from one website page concurrently.

    Args:
    url (str): URL of the web page to be scraped.

    Returns:
    List[Dict[str, str]]: List of products with their respective details.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Gagal mengambil {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for product in soup.find_all("div", class_="collection-card"):
        try:
            title = product.find("h3", class_="product-title")
            title = title.text.strip() if title else "Produk Tidak Dikenal"

            price = product.find("span", class_="price")
            price = price.text.strip().replace("$", "") if price else "Tidak Tersedia"

            rating_elem = product.find("p", string=lambda text: text and "Rating" in text)
            rating = rating_elem.text.replace("Rating:", "").replace("⭐", "").strip() if rating_elem else "Tidak Valid"

            colors_elem = product.find("p", string=lambda text: text and "Colors" in text)
            colors = colors_elem.text.replace("Colors:", "").strip().split()[0] if colors_elem else "Tidak Tersedia"

            size_elem = product.find("p", string=lambda text: text and "Size" in text)
            size = size_elem.text.replace("Size:", "").strip() if size_elem else "Tidak Tersedia"

            gender_elem = product.find("p", string=lambda text: text and "Gender" in text)
            gender = gender_elem.text.replace("Gender:", "").strip() if gender_elem else "Tidak Tersedia"

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            products.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "Timestamp": timestamp
            })
        except Exception as e:
            logging.warning(f"Gagal mengekstrak produk: {e}")

    return products

def generate_urls(max_pages: int = MAX_PAGES_LIMIT) -> List[str]:
    """
    Returns a list of URLs to scrape.

    Args:
    max_pages (int, optional): Maximum number of pages. Defaults to MAX_PAGES_LIMIT.

    Returns:
    List[str]: List of URLs to scrape.
    """
    urls = [BASE_URL]
    urls.extend([f"{BASE_URL}page{page}" for page in range(2, max_pages + 1)])
    return urls

def scrape_main(max_pages: int = MAX_PAGES_LIMIT) -> List[Dict[str, str]]:
    """
    Scrapes products from all pages of a website concurrently.

    Args:
    max_pages (int, optional): The maximum number of pages to scrape.

    Defaults to MAX_PAGES_LIMIT.

    Returns
    List[Dict[str, str]]: List of all products that were successfully scraped.
    """
    start_time = time.time()
    urls = generate_urls(max_pages)
    all_products = []

    # Use ThreadPoolExecutor for concurrent scraping 
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
      
        # Map URLs into scrape_page function
        future_to_url = {executor.submit(scrape_page, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                page_products = future.result()
                if page_products:
                    all_products.extend(page_products)
                    logging.info(f"Berhasil scrape {len(page_products)} produk dari {url}")
            except Exception as e:
                logging.error(f"Kesalahan saat scraping {url}: {e}")

    # Logging execution time
    execution_time = time.time() - start_time
    print(f"\nTotal waktu scraping: {execution_time:.2f} detik")
    print(f"Total produk yang di-scrape: {len(all_products)}\n")
    return all_products