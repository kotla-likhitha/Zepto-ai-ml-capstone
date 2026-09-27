# Zepto Support Assistant

An offline RAG-based customer support assistant for Zepto policies.

## Overview

This module uses Zepto policy documents as a local knowledge base and retrieves relevant information using embeddings and ChromaDB.

The system uses LangGraph to classify questions and route them to either policy retrieval or a direct response.

## Architecture

```text
Zepto Policy Documents
        ↓
Document Loading
        ↓
Sentence Transformers
(all-MiniLM-L6-v2)
        ↓
ChromaDB Vector Store
        ↓
User Query
        ↓
Intent Classification
        ↓
 ┌───────────────┐
 │               │
Policy        General
Question      Question
 │               │
 ↓               ↓
Retrieve       Direct
Top-3 Docs     Answer
 │
 ↓
Response
Corpus

The knowledge base contains exactly 8 Zepto policy documents:

doc_01.txt - Delivery
doc_02.txt - Returns and refunds
doc_03.txt - Membership
doc_04.txt - Order tracking
doc_05.txt - Cancellation
doc_06.txt - Damaged or missing items
doc_07.txt - Gift cards
doc_08.txt - Customer support
Embeddings and Retrieval

The system uses the local all-MiniLM-L6-v2 Sentence Transformers model.

ChromaDB stores the document embeddings and performs cosine-similarity retrieval.

For every policy question, the system retrieves the top 3 relevant documents.

LangGraph Workflow

The graph contains three nodes:

classify_intent
retrieve_and_answer
direct_answer

A conditional edge routes policy questions to retrieve_and_answer.

General questions are routed to direct_answer.

Intent Classification

The mock baseline uses keyword-based intent classification.

Supported policy keywords include:

delivery
return
refund
membership
tracking
cancel
gift card
support hours
Mock LLM Mode

The default configuration uses:

MOCK_LLM=1

No external LLM API key is required.

For policy questions, the mock response starts with:

Based on the retrieved context:

For unsupported questions, the assistant returns:

I can only answer questions about Zepto policies right now.
Pydantic Response

The API returns a structured response containing:

answer
sources
confidence

Validation is performed using a Pydantic model with retry logic.

FastAPI

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn main:app --host 0.0.0.0 --port 7860

The API endpoint is:

POST /ask
Example Request 1
{
  "query": "What are the delivery charges?"
}
Example Request 2
{
  "query": "What is the capital of India?"
}

The API returns JSON containing the answer, retrieved sources, and confidence score.

Docker

Build the Docker image:

docker build -t zepto-support-assistant .

Run the container:

docker run -p 7860:7860 zepto-support-assistant
Files
support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
