# Data Pipeline

## Objective

Build an end-to-end data pipeline using books.toscrape.com.

The pipeline follows:

Scrape → Clean → Convert → Store → Query → Analyze

## Data Source

The data is collected from:

http://books.toscrape.com/

The first 5 catalogue pages are scraped.

The final dataset contains at least 60 books across at least 3 categories.

## Scraping

The pipeline uses:

- Python
- Requests
- BeautifulSoup

For each book, the following fields are collected:

- title
- price
- star_rating
- availability
- category

## Data Cleaning

The pound currency symbol and other non-numeric characters are removed from the price.

The cleaned price is stored as `price_gbp` with float type.

Star ratings are converted as follows:

- One = 1
- Two = 2
- Three = 3
- Four = 4
- Five = 5

Availability is converted into the Boolean column `in_stock`.

Rows with invalid required numeric values are dropped so that the pipeline does not crash.

## Currency Conversion

The required fixed project rate is:

`1 GBP = 105.50 INR`

The converted value is stored in `price_inr`.

No live currency API is used.

## SQLite Database

The database contains two normalized tables.

### categories

- category_id - Primary Key
- category_name - Unique

### books

- book_id - Primary Key
- title
- price_gbp
- price_inr
- rating
- in_stock
- category_id - Foreign Key

The relationship is:

`categories.category_id → books.category_id`

One category can contain many books.

## SQL Queries

Six SQL queries are executed demonstrating:

1. SELECT and WHERE
2. ORDER BY and LIMIT
3. DISTINCT
4. BETWEEN
5. IN
6. JOIN

The SQL queries and their outputs are saved in:

`query_outputs.txt`

## Pandas Analysis

SQL results are read using `pd.read_sql()`.

The JOIN result is independently reproduced using `pd.merge()`.

The SQL JOIN and pandas merge results are compared for equivalence.

## Installation

Install the required libraries:

```bash
pip install requests beautifulsoup4 pandas
