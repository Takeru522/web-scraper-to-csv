
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# Step 1: Scrape product data
def fetch_product_data(url):
    print("Fetching data from:", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []

    for product in soup.select(".product_pod"):
        title = product.h3.a["title"]
        price = product.select_one(".price_color").text.strip()
        rating = product.p["class"][1]  # e.g. "Three"
        availability = product.select_one(".availability").text.strip()

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return products

# Step 2: Save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)
    df.to_csv(path, index=False)
    print(f"Saved {len(data)} products to {path}")

if __name__ == "__main__":
    URL = "https://books.toscrape.com/"
    scraped_data = fetch_product_data(URL)
    save_to_csv(scraped_data, "products.csv")