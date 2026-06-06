import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

books_data = []

current_url = "http://books.toscrape.com/"

while current_url:

    print(f"Scraping: {current_url}")

    try:
        response = requests.get(current_url, timeout=10)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        books = soup.find_all(
            "article",
            class_="product_pod"
        )

        for book in books:

            title = (
                book.h3.a["title"]
                if book.h3.a
                else "No Title"
            )

            price_tag = book.find(
                "p",
                class_="price_color"
            )

            price = (
                price_tag.text.strip()
                if price_tag
                else "No Price"
            )

            stock_tag = book.find(
                "p",
                class_="instock availability"
            )

            availability = (
                stock_tag.text.strip()
                if stock_tag
                else "Unknown"
            )

            rating_tag = book.find(
                "p",
                class_="star-rating"
            )

            rating = (
                rating_tag["class"][1]
                if rating_tag
                else "No Rating"
            )

            product_url = urljoin(
                current_url,
                book.h3.a["href"]
            )

            books_data.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating,
                "Product_URL": product_url
            })

        next_button = soup.find(
            "li",
            class_="next"
        )

        if next_button:
            next_page = next_button.a["href"]
            current_url = urljoin(
                current_url,
                next_page
            )
        else:
            current_url = None

    except Exception as e:
        print("Error:", e)
        break

df = pd.DataFrame(books_data)

df.drop_duplicates(inplace=True)

df.fillna("N/A", inplace=True)

df.to_csv(
    "data/books_dataset.csv",
    index=False,
    encoding="utf-8"
)

print("\nTotal Books:", len(df))
print("Dataset Saved Successfully")
