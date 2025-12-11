from langchain_core.embeddings import Embeddings
from transformers import AutoTokenizer, AutoModel
import torch

# Custom embedding class
class E5Embeddings(Embeddings):
    def __init__(self, model_name="intfloat/e5-small-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_query(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state[:, 0]
        return embeddings[0].tolist()

    def embed_documents(self, texts):
        vectors = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                embeddings = self.model(**inputs).last_hidden_state[:, 0]
            vectors.append(embeddings[0].tolist())
        return vectors


# ⬇️ Use it like a normal LangChain embedding
embedding = E5Embeddings()

# Single query
vector = embedding.embed_query("Delhi is the capital of India")
print("Vector length:", len(vector))
print(vector)

# Multiple documents
docs = ["Mumbai is a city", "Cricket is a sport"]
vectors = embedding.embed_documents(docs)

print("Number of doc embeddings:", len(vectors))
