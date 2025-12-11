import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 🔴 TEMPORARY: Paste your API key here
GEMINI_API_KEY = ""

st.set_page_config(page_title="Gemini AI Chatbot")
st.title("Gemini AI Chatbot")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "{question}")
])

user_input = st.text_input("Ask something")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=GEMINI_API_KEY
)

chain = prompt | llm | StrOutputParser()

if user_input:
    st.write(chain.invoke({"question": user_input}))
