from langchain_openai import ChatOpenAI
import os
import httpx
import requests
import certifi

# -------------------------------
# Step 1: Force tiktoken to use a local cache folder
# -------------------------------
os.makedirs("./tiktoken_cache", exist_ok=True)
os.environ["TIKTOKEN_CACHE_DIR"] = "./tiktoken_cache"

# -------------------------------
# Step 2: Monkey-patch requests globally to skip SSL verification
# This makes tiktoken downloads work without SSL errors
# -------------------------------
original_requests_get = requests.get
def unsafe_requests_get(*args, **kwargs):
    kwargs["verify"] = False
    return original_requests_get(*args, **kwargs)

requests.get = unsafe_requests_get

# -------------------------------
# Step 3: Create an httpx client with SSL disabled
# -------------------------------
client = httpx.Client(verify=False)

# -------------------------------
# Step 4: Initialize ChatOpenAI
# -------------------------------
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o",
    api_key="sk-If1PJAnGI-GpKJfyY4qVyw",
    http_client=client
)

# -------------------------------
# Step 5: Test LLM
# -------------------------------
response = llm.invoke("Hi")
print(response)
