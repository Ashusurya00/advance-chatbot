from transformers import AutoTokenizer, AutoModel
import torch

model_name = "intfloat/e5-small-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

text = "Delhi is the capital of India"
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state[:, 0]

vector = embeddings[0].tolist()

print("Length:", len(vector))
print(vector)
