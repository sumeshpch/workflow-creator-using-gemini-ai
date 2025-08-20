from fastapi import FastAPI, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import json
import uvicorn

app = FastAPI()

# Load JSON Magento data
def load_json():
    with open("magento_dump.json", "r", encoding="utf-8") as f:
        return json.load(f)

json_data = load_json()

# Chunking
def chunk_json_data(json_data, table, chunk_size=5):
    rows = json_data.get(table, [])
    chunks = []
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i+chunk_size]
        chunk_text = f"Table: {table}\n" + "\n".join(json.dumps(r) for r in chunk)
        chunks.append(chunk_text)
    return chunks

all_chunks = []
for table in ["sales_order", "customer_entity", "sales_order_item", "catalog_product_entity"]:
    all_chunks.extend(chunk_json_data(json_data, table))

# Embeddings + FAISS
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(all_chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
chunk_lookup = {i: all_chunks[i] for i in range(len(all_chunks))}

# Pydantic model for request
class QueryRequest(BaseModel):
    question: str

# Gemini mock (replace with real Gemini call)
def call_gemini(prompt: str):
    return {
        "response": "(Gemini would respond here)",
        "details": {
            "source_data": prompt.splitlines()[:3],
            "explanation": "Simulated Gemini response"
        }
    }

# Retrieve + respond
@app.post("/ask")
def ask_rag(query: QueryRequest):
    question = query.question
    query_embedding = model.encode([question])
    distances, indices = index.search(query_embedding, 5)
    context = "\n\n".join([chunk_lookup[i] for i in indices[0]])

    # Create Gemini-style prompt
    prompt = f"""
Use the following Magento data to answer the question:

Context:
{context}

Question:
{question}

Respond in JSON format with fields: response, details, source_data.
    """

    gemini_result = call_gemini(prompt)
    return gemini_result

# Run with: uvicorn magento_rag_api:app --reload
if __name__ == "__main__":
    uvicorn.run("magento_rag_api:app", host="0.0.0.0", port=8000, reload=True)
