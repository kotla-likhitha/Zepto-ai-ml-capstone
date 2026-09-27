# Zepto AI/ML Capstone

An end-to-end AI/ML engineering capstone containing three connected modules:

1. Data Pipeline
2. Analytics
3. GenAI Support Assistant

## Project Structure

- `/data_pipeline` - Web scraping, cleaning, currency conversion, SQLite storage, and SQL/pandas analysis.
- `/analytics` - Customer-style dataset profiling, preprocessing, machine learning, and evaluation.
- `/support_assistant` - Grounded GenAI support assistant using Zepto policy documents.

## Modules

### Data Pipeline

Scrapes product-style data from Books to Scrape, cleans the data, converts GBP prices to INR using the required fixed rate, stores the data in SQLite, and performs SQL and pandas analysis.

### Analytics

Profiles a customer-style dataset, performs preprocessing, trains machine learning models, and evaluates their performance.

### GenAI Support Assistant

Builds a support assistant that answers policy questions using Zepto's own documents.
## Requirements

Python 3.10 or later is recommended.

Each module contains its own dependencies where required:

- `/data_pipeline` - Python libraries for web scraping, pandas, SQLite, and analysis.
- `/analytics` - Python libraries for data analysis and machine learning.
- `/support_assistant/requirements.txt` - FastAPI, Uvicorn, ChromaDB, Sentence Transformers, LangGraph, and Pydantic.

## Running the Project

### 1. Data Pipeline

Go to the data pipeline folder:

```bash
cd data_pipeline
Run the scraping pipeline:

python scrape_pipeline.py

Create the SQLite database and run the SQL/pandas analysis:

python database.py
python sql_queries.py

The pipeline scrapes Books to Scrape, cleans the data, converts GBP to INR using the fixed rate of:

1 GBP = 105.50 INR

It creates the SQLite database and produces SQL query outputs.

2. Analytics

Go to the analytics folder:

cd analytics

Run the notebooks in this order:

01_eda.ipynb
02_modelling.ipynb

01_eda.ipynb performs profiling, cleaning, visualization, and exploratory analysis.

02_modelling.ipynb performs preprocessing, classification, imbalance comparison, Random Forest tuning, regression, model comparison, and pipeline saving.

The committed titanic.csv provides an offline copy of the dataset for reproducibility.

3. Support Assistant

Go to the support assistant folder:

cd support_assistant

Install dependencies:

pip install -r requirements.txt

Run the FastAPI application:

uvicorn main:app --reload

The API provides:

POST /ask

Example request:

{
  "query": "What are the delivery charges?"
}

The required baseline uses deterministic mock mode. MOCK_LLM can be left unset or set to:

MOCK_LLM=1

The Support Assistant uses the eight Zepto policy documents in /support_assistant/docs, local all-MiniLM-L6-v2 embeddings, ChromaDB retrieval, and LangGraph routing.

Design Decisions
The project uses one GitHub repository containing all three modules.
The Data Pipeline uses a fixed GBP-to-INR conversion rate of 105.50 to keep results reproducible without requiring an external currency API.
SQLite is used for normalized relational storage in the Data Pipeline.
The Analytics module uses a saved titanic.csv fallback so the modeling stage does not need to download the raw dataset again.
The Support Assistant uses local embeddings and ChromaDB so the required mock baseline does not require an LLM API key.
LangGraph is used to route policy questions to retrieval and general questions to a direct response.
The Support Assistant is exposed through FastAPI and includes a Dockerfile for local container execution.

### Important

Do **not** delete the sections above `## Requirements`.

So your README will have:

```text
Project Structure
↓
Modules
↓
Requirements
↓
Running the Project
↓
Design Decisions
