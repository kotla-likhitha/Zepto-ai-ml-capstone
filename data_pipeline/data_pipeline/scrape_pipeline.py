import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

books = []

for page in range(1, 6):
    url = BASE_URL.format(page)

    print(f"Scraping page {page}...")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for article in soup.select("article.product_pod"):

        title = article.h3.a["title"]

        price = article.select_one(
            ".price_color"
        ).get_text(strip=True)

        star_rating = article.select_one(
            "p.star-rating"
        )["class"][1]

        availability = article.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        # Open individual book page to get category
        book_url = urljoin(
            url,
            article.h3.a["href"]
        )

        book_response = requests.get(
            book_url,
            timeout=10
        )

        book_response.raise_for_status()

        book_soup = BeautifulSoup(
            book_response.text,
            "html.parser"
        )

        category = book_soup.select(
            "ul.breadcrumb li"
        )[-2].get_text(strip=True)

        books.append({
            "title": title,
            "price": price,
            "star_rating": star_rating,
            "availability": availability,
            "category": category
        })


# Convert scraped data to DataFrame
df = pd.DataFrame(books)

print("\nScraping completed!")
print("Number of books:", len(df))

print(
    "Number of categories:",
    df["category"].nunique()
)

print("\nCategories:")
print(df["category"].unique())

print("\nFirst 5 rows:")
print(df.head())

print("\nDataFrame shape:")
print(df.shape)
# -----------------------------
# Data Cleaning
# -----------------------------

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Convert price from £ text to float
df["price_gbp"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .astype(float)
)

# Convert star rating text to integer
df["rating"] = df["star_rating"].map(rating_map)

# Convert availability text to Boolean
df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)

# Convert GBP to INR using fixed exchange rate
GBP_TO_INR = 105.50

df["price_inr"] = df["price_gbp"] * GBP_TO_INR

# Remove rows where important numeric values could not be parsed
df = df.dropna(
    subset=["price_gbp", "rating"]
)

print("\nCleaned Data:")
print(
    df[
        [
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category"
        ]
    ].head()
)

print("\nData types:")
print(df.dtypes)
