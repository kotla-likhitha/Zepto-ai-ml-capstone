import sqlite3
from scrape_pipeline import df


# ---------------------------------
# 1. Database connection
# ---------------------------------

DB_NAME = "books.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


# ---------------------------------
# 2. Create categories table
# ---------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")


# ---------------------------------
# 3. Create books table
# ---------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")


# ---------------------------------
# 4. Insert categories
# ---------------------------------

for category in df["category"].unique():

    cursor.execute(
        """
        INSERT OR IGNORE INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )


# ---------------------------------
# 5. Insert books
# ---------------------------------

for _, row in df.iterrows():

    cursor.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (row["category"],)
    )

    category_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO books
        (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            int(row["in_stock"]),
            category_id
        )
    )


# ---------------------------------
# 6. Save database
# ---------------------------------

connection.commit()


# ---------------------------------
# 7. Verify database
# ---------------------------------

book_count = cursor.execute(
    "SELECT COUNT(*) FROM books"
).fetchone()[0]

category_count = cursor.execute(
    "SELECT COUNT(*) FROM categories"
).fetchone()[0]

print("SQLite database created successfully!")
print("Number of books:", book_count)
print("Number of categories:", category_count)


connection.close()
