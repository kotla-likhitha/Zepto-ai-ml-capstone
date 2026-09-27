import sqlite3
import pandas as pd


# ---------------------------------
# 1. Connect to database
# ---------------------------------

DB_NAME = "books.db"

connection = sqlite3.connect(DB_NAME)


# ---------------------------------
# 2. SQL Queries
# ---------------------------------

queries = {

    "Query 1 - WHERE": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4
    """,

    "Query 2 - ORDER BY and LIMIT": """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10
    """,

    "Query 3 - DISTINCT": """
        SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name
    """,

    "Query 4 - BETWEEN": """
        SELECT title, price_gbp
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
    """,

    "Query 5 - IN": """
        SELECT title, rating, category_id
        FROM books
        WHERE rating IN (4, 5)
    """,

    "Query 6 - JOIN": """
        SELECT
            b.book_id,
            b.title,
            b.price_gbp,
            b.rating,
            c.category_name
        FROM books b
        JOIN categories c
            ON b.category_id = c.category_id
        ORDER BY b.rating DESC, b.price_gbp DESC
        LIMIT 10
    """
}


# ---------------------------------
# 3. Execute queries and save output
# ---------------------------------

output_file = open(
    "query_outputs.txt",
    "w",
    encoding="utf-8"
)

results = {}

for query_name, query in queries.items():

    print("\n" + "=" * 60)
    print(query_name)
    print("=" * 60)

    print("SQL:")
    print(query.strip())

    result = pd.read_sql(query, connection)

    results[query_name] = result

    print("\nOutput:")
    print(result.to_string(index=False))

    output_file.write("\n" + "=" * 60 + "\n")
    output_file.write(query_name + "\n")
    output_file.write("=" * 60 + "\n")

    output_file.write("\nSQL:\n")
    output_file.write(query.strip())

    output_file.write("\n\nOutput:\n")
    output_file.write(result.to_string(index=False))
    output_file.write("\n")


# ---------------------------------
# 4. Read two SQL results with pandas
# ---------------------------------

high_rated_df = pd.read_sql(
    queries["Query 1 - WHERE"],
    connection
)

top_books_df = pd.read_sql(
    queries["Query 2 - ORDER BY and LIMIT"],
    connection
)

print("\n\nPandas DataFrame from Query 1:")
print(high_rated_df.head())

print("\nPandas DataFrame from Query 2:")
print(top_books_df.head())


# ---------------------------------
# 5. Reproduce JOIN using pd.merge
# ---------------------------------

books_df = pd.read_sql(
    "SELECT * FROM books",
    connection
)

categories_df = pd.read_sql(
    "SELECT * FROM categories",
    connection
)

merge_result = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

merge_result = merge_result[
    [
        "book_id",
        "title",
        "price_gbp",
        "rating",
        "category_name"
    ]
]

merge_result = merge_result.sort_values(
    by=["rating", "price_gbp"],
    ascending=[False, False]
).head(10)


# ---------------------------------
# 6. Compare SQL JOIN and pd.merge
# ---------------------------------

sql_join_result = results["Query 6 - JOIN"]

sql_join_result = sql_join_result.reset_index(drop=True)
merge_result = merge_result.reset_index(drop=True)

print("\n\nSQL JOIN result:")
print(sql_join_result)

print("\n\npd.merge result:")
print(merge_result)

print(
    "\nDo SQL JOIN and pd.merge match?",
    sql_join_result.equals(merge_result)
)


# Save comparison to output file
output_file.write("\n\n" + "=" * 60 + "\n")
output_file.write("SQL JOIN vs pd.merge\n")
output_file.write("=" * 60 + "\n")

output_file.write("\nSQL JOIN result:\n")
output_file.write(sql_join_result.to_string(index=False))

output_file.write("\n\npd.merge result:\n")
output_file.write(merge_result.to_string(index=False))

output_file.write(
    "\n\nDo SQL JOIN and pd.merge match? "
    + str(sql_join_result.equals(merge_result))
)

output_file.close()

connection.close()

print("\n\nAll SQL queries completed.")
print("Query outputs saved to query_outputs.txt")
