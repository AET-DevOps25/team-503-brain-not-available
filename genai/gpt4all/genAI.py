from gpt4all import GPT4All
from fastapi import Body, FastAPI
import requests
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
import weaviate
import weaviate.classes.config as wc
import logging

BACKEND_URL = "http://server:1111"
WEAVIATE_HOST = "weaviate"
AI_BACKEND = {"mode": "cloud"}  # or "cloud"
OLLAMA_API_URL = "https://gpu.aet.cit.tum.de/api/chat/completions"
OLLAMA_API_KEY = "sk-741cb60afc8d499da35726c28be3e054"
OLLAMA_MODEL = "llama3.3:latest"

app = FastAPI()
Instrumentator().instrument(app).expose(app)

model = None

class ChatRequest(BaseModel):
    prompt: str
    page_id: int

def connect_to_weaviate():
    try:
        client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=8081,
            http_secure=False,
            grpc_host=WEAVIATE_HOST,
            grpc_port=50051,
            grpc_secure=False,
        )
        return client
    except Exception as e:
        print(f"Failed to connect to Weaviate: {e}")
        return None

def get_weaviate_collection():
    client = connect_to_weaviate()
    if not client:
        return None
    try:
        # List all collections and check if "WikiPage" exists
        collections = client.collections.list_all()
        collection_names = collections.keys()
        if "WikiPage" in collection_names:
            return client.collections.get("WikiPage")
        else:
            print(f"Collection 'WikiPage' not found, creating new one.")
            client.collections.create(
                name="WikiPage",
                properties=[
                    wc.Property(name="title", data_type=wc.DataType.TEXT),
                    wc.Property(name="content", data_type=wc.DataType.TEXT),
                    wc.Property(name="pageId", data_type=wc.DataType.NUMBER),
                ],
                vector_config=wc.Configure.Vectors.text2vec_gpt4all(
                    name="default",
                    source_properties=["title", "content"],
                ),
            )
            return client.collections.get("WikiPage")
    except Exception as e:
        print(f"Error accessing Weaviate collections: {e}")
        return None

@app.post("/update_weaviate")
async def update_weaviate():
    wiki_collection = get_weaviate_collection()
    if wiki_collection is None:
        return JSONResponse(
            status_code=503,
            content={"status": "Weaviate unavailable, not updated"}
        )
    try:
        wiki_collection.data.delete_many(where=weaviate.classes.query.Filter.by_property("pageId").greater_or_equal(0))
        resp = requests.get(f"{BACKEND_URL}/pages", timeout=5)
        resp.raise_for_status()
        pages = resp.json()
        for page in pages:
            data_object = {
                "title": page["title"],
                "content": page["content"],
                "pageId": page["pageId"]
            }
            wiki_collection.data.insert(data_object)
        return {"status": "Weaviate updated with wiki pages"}
    except requests.RequestException as e:
        return JSONResponse(
            status_code=503,
            content={"status": "Backend unavailable, Weaviate not updated", "error": str(e)}
        )

def get_context_from_weaviate(query):
    """
    Retrieves relevant wiki pages from Weaviate based on the query.
    Returns a list of dicts: [{"title": ..., "content": ..., "pageId": ...}, ...]
    """
    wiki_collection = get_weaviate_collection()
    if not wiki_collection:
        return []  # No context if collection is unavailable
    response = wiki_collection.query.near_text(query=query, limit=15)
    context_list = []
    for obj in response.objects:
        title = obj.properties.get("title", "")
        content = obj.properties.get("content", "")
        page_id = obj.properties.get("pageId", None)
        context_list.append({
            "title": title,
            "content": content,
            "pageId": page_id
        })
    return context_list

def get_page_content(page_id):
    """
    Queries the backend for the content of the page with the given page_id.
    Returns a string with the page's title and content, or an empty string if not found.
    """
    try:
        resp = requests.get(f"{BACKEND_URL}/page/{page_id}", timeout=5)
        if resp.status_code == 200:
            page = resp.json()
            title = page.get("title", "")
            content = page.get("content", "")
            return f"Current Page [{page_id}]: {title}\n{content}\n"
        else:
            logging.warning(f"Page {page_id} not found in backend.")
            return ""
    except Exception as e:
        logging.error(f"Error fetching page {page_id}: {e}")
        return ""

@app.post("/set_backend")
async def set_backend(mode: str = Body(..., embed=True)):
    global model
    if mode not in ("local", "cloud"):
        return JSONResponse(status_code=400, content={"error": "Invalid mode"})
    AI_BACKEND["mode"] = mode
    if mode == "local" and model is None:
        model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    return {"status": f"AI backend set to {mode}"}

@app.get("/get_backend")
async def get_backend():
    return {"mode": AI_BACKEND["mode"]}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Get context from Weaviate based on prompt
    context = get_context_from_weaviate(request.prompt)
    # Get current page context
    page_context = get_page_content(request.page_id)
    # Combine both contexts
    full_context = f"{page_context}\n{context}".strip()
    if AI_BACKEND["mode"] == "local":
        full_prompt = f"Context:\n{full_context}\n\nUser: {request.prompt}"
        with model.chat_session():
            response = model.generate(full_prompt, max_tokens=1024)
        return JSONResponse(content={"response": response, "page_id": request.page_id})
    else:
        # Cloud AI via Ollama API Proxy, include context in prompt
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        prompt_with_context = f"Context:\n{full_context}\n\nUser: {request.prompt}"
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt_with_context}]
        }
        try:
            resp = requests.post(OLLAMA_API_URL, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return JSONResponse(content={"response": response_text, "page_id": request.page_id})
        except Exception as e:
            return JSONResponse(status_code=503, content={"error": str(e), "page_id": request.page_id})

if __name__ == "__main__":
    update_weaviate()
    uvicorn.run("genAI:app", host="0.0.0.0", port=5000, reload=True)