import os
from typing import TypedDict

import chromadb
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# --------------------------------------------------
# Pydantic schemas
# --------------------------------------------------

class AskRequest(BaseModel):
    query: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


# --------------------------------------------------
# LangGraph state
# --------------------------------------------------

class AssistantState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


# --------------------------------------------------
# Embedding model + ChromaDB
# --------------------------------------------------

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = chroma_client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)


# --------------------------------------------------
# Document ingestion
# --------------------------------------------------

def load_documents():
    documents = []
    ids = []
    metadatas = []

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DOCS_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read().strip()

        if text:
            documents.append(text)
            ids.append(filename.replace(".txt", ""))
            metadatas.append({"source": filename})

    return documents, ids, metadatas


def build_vector_store():
    documents, ids, metadatas = load_documents()

    if len(documents) != 8:
        raise RuntimeError(
            f"Expected 8 corpus documents, but found {len(documents)}."
        )

    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    existing = collection.get()
    existing_ids = set(existing.get("ids", []))

    new_documents = []
    new_ids = []
    new_metadatas = []
    new_embeddings = []

    for document, doc_id, metadata, embedding in zip(
        documents,
        ids,
        metadatas,
        embeddings
    ):
        if doc_id not in existing_ids:
            new_documents.append(document)
            new_ids.append(doc_id)
            new_metadatas.append(metadata)
            new_embeddings.append(embedding)

    if new_documents:
        collection.add(
            ids=new_ids,
            documents=new_documents,
            metadatas=new_metadatas,
            embeddings=new_embeddings
        )

    print(f"Corpus documents loaded: {len(documents)}")
    print(f"ChromaDB documents available: {collection.count()}")


# --------------------------------------------------
# Structured prompt
# --------------------------------------------------

PROMPT_TEMPLATE = """
ROLE:
You are a Zepto customer-support assistant.

CONTEXT:
Use only the policy information supplied in the retrieved context.

TASK:
Answer the customer's question using the retrieved Zepto policy.

FORMAT:
Return a concise and direct answer.

LENGTH:
Keep the answer within 2-4 sentences.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the provided context.

FEW-SHOT EXAMPLE:
Question: What are the delivery charges?
Context: Standard delivery is free on orders over INR 149.
Answer: Standard delivery is free on orders over INR 149.

Customer Question:
{question}

Retrieved Context:
{context}
"""


# --------------------------------------------------
# Intent classification
# --------------------------------------------------

POLICY_KEYWORDS = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours"
]


def classify_intent(state: AssistantState):
    query = state["query"].lower()

    if any(keyword in query for keyword in POLICY_KEYWORDS):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {"intent": intent}


# --------------------------------------------------
# Retrieval
# --------------------------------------------------

def retrieve_documents(query: str):
    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    documents = results["documents"][0]
    ids = results["ids"][0]

    return documents, ids


# --------------------------------------------------
# Retrieval + answer node
# --------------------------------------------------

def retrieve_and_answer(state: AssistantState):
    documents, ids = retrieve_documents(state["query"])

    top_chunk = documents[0]
    top_chunk_snippet = top_chunk[:200]

    if MOCK_LLM:
        answer = (
            f"Based on the retrieved context: "
            f"{top_chunk_snippet}"
        )

        return {
            "answer": answer,
            "sources": ids,
            "confidence": 1.0
        }

    # Optional real-LLM path.
    # The structured prompt is prepared here for a real LLM.
    context = "\n\n".join(documents)

    prompt = PROMPT_TEMPLATE.format(
        question=state["query"],
        context=context
    )

    # Optional extension placeholder.
    answer = (
        "Real LLM mode is optional. "
        "Use the structured prompt below with your chosen free-tier LLM:\n"
        + prompt
    )

    return {
        "answer": answer,
        "sources": ids,
        "confidence": 1.0
    }


# --------------------------------------------------
# General-question node
# --------------------------------------------------

def direct_answer(state: AssistantState):

    if MOCK_LLM:
        answer = (
            "I can only answer questions about Zepto policies right now."
        )

        return {
            "answer": answer,
            "sources": [],
            "confidence": 1.0
        }

    # Optional real-LLM path.
    return {
        "answer": (
            "I can only answer questions about Zepto policies right now."
        ),
        "sources": [],
        "confidence": 1.0
    }


# --------------------------------------------------
# Conditional routing
# --------------------------------------------------

def route_intent(state: AssistantState):

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------

graph_builder = StateGraph(AssistantState)

graph_builder.add_node(
    "classify_intent",
    classify_intent
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

graph_builder.add_node(
    "direct_answer",
    direct_answer
)

graph_builder.add_edge(
    START,
    "classify_intent"
)

graph_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph_builder.add_edge(
    "retrieve_and_answer",
    END
)

graph_builder.add_edge(
    "direct_answer",
    END
)

graph = graph_builder.compile()


# --------------------------------------------------
# Build vector store
# --------------------------------------------------

build_vector_store()


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline RAG-based Zepto policy support assistant"
)


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):

    result = graph.invoke(
        {
            "query": request.query
        }
    )

    response = AnswerResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 1.0)
    )

    return response
