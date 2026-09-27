import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of Books to Scrape
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# List to store all scraped books
books = []

# Scrape the first 5 pages
for page in range(1, 6):

    url = BASE_URL.format(page)

    print(f"Scraping page {page}...")

    # Send request to the website
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all books on the page
    for article in soup.select("article.product_pod"):

        # Get book title
        title = article.h3.a["title"]

        # Get price
        price = article.select_one(".price_color").get_text(strip=True)

        # Get star rating
        star_rating = article.select_one(
            "p.star-rating"
        )["class"][1]

        # Get availability
        availability = article.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        # Get the individual book URL
        book_url = urljoin(
            url,
            article.h3.a["href"]
        )

        # Request the individual book page
        book_response = requests.get(
            book_url,
            timeout=10
        )
        book_response.raise_for_status()

        # Parse individual book page
        book_soup = BeautifulSoup(
            book_response.text,
            "html.parser"
        )

        # Get category
        category = book_soup.select(
            "ul.breadcrumb li"
        )[-2].get_text(strip=True)

        # Store book information
        books.append({
            "title": title,
            "price": price,
            "star_rating": star_rating,
            "availability": availability,
            "category": category
        })


# Convert scraped data into a pandas DataFrame
df = pd.DataFrame(books)

# Display results
print("\nScraping completed!")
print("Number of books:", len(df))
print("Number of categories:", df["category"].nunique())

print("\nCategories:")
print(df["category"].unique())

print("\nFirst 5 rows:")
print(df.head())

print("\nDataFrame shape:")
print(df.shape)
