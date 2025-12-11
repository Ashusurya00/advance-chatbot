from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

st.title("Gemini Chatbot")
user_input = st.text_input("Ask something")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

chain = prompt | llm | StrOutputParser()

if user_input:
    st.write(chain.invoke({"question": user_input}))
