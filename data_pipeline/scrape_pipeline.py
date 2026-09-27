import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ---------------------------------
# 1. Website URL
# ---------------------------------

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

books = []


# ---------------------------------
# 2. Scrape first 5 pages
# ---------------------------------

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

        # Get individual book page
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

        # Get category
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


# ---------------------------------
# 3. Create DataFrame
# ---------------------------------

df = pd.DataFrame(books)

print("\nScraping completed!")
print("Number of books:", len(df))
print("Number of categories:", df["category"].nunique())


# ---------------------------------
# 4. Clean the data
# ---------------------------------

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Remove £ and convert price to float
df["price_gbp"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .astype(float)
)

# Convert rating text to number
df["rating"] = df["star_rating"].map(rating_map)

# Convert availability to True/False
df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)


# ---------------------------------
# 5. Convert GBP to INR
# ---------------------------------

GBP_TO_INR = 105.50

df["price_inr"] = df["price_gbp"] * GBP_TO_INR


# ---------------------------------
# 6. Handle invalid values
# ---------------------------------

df = df.dropna(
    subset=["price_gbp", "rating"]
)


# ---------------------------------
# 7. Display final data
# ---------------------------------

print("\nFinal cleaned data:")

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

print("\nFinal shape:")
print(df.shape)

print("\nCategories:")
print(df["category"].unique())
