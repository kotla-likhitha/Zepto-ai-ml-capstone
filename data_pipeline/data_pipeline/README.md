# Data Pipeline

## Overview

This module implements an end-to-end data engineering pipeline using Books to Scrape.

The pipeline follows:

Scrape → Clean → Convert → Store → Query → Analyze

## Data Source

Books to Scrape:
http://books.toscrape.com/

## Requirements

- Scrape at least 60 books.
- Collect books from at least 3 categories.
- Clean price, rating, and availability.
- Convert GBP to INR.
- Store the data in a normalized SQLite database.
- Execute at least 5 SQL queries.
- Use pandas `read_sql()`.
- Reproduce the JOIN using pandas `merge()`.

## Currency Conversion

The required fixed project rate is:

**1 GBP = 105.50 INR**

This is a project-defined fixed rate and does not require an external API.

## Pipeline

Scraping
→ Cleaning
→ Currency Conversion
→ SQLite Database
→ SQL Queries
→ Pandas Analysis
