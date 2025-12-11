from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",   # 🔥 Your working Groq model
    temperature=1.5,
    max_tokens=50  # same purpose as max_completion_tokens
)

result = model.invoke("Write a 5 line poem on cricket")

print(result.content)
