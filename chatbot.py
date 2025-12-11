import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# =========================
# 🔐 API KEYS (TEMPORARY)
# =========================
GEMINI_API_KEY = ""
LANGCHAIN_API_KEY = ""

# =========================
# 🔍 LangSmith Tracing
# =========================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Gemini-Streamlit-Chatbot"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# =========================
# 🎨 Streamlit Page Config
# =========================
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini + LangChain + LangSmith")

# =========================
# 💬 Chat History
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# 🧠 Prompt Template
# =========================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# =========================
# 🤖 LLM
# =========================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=GEMINI_API_KEY
)

chain = prompt | llm | StrOutputParser()

# =========================
# 🧑 User Input
# =========================
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = chain.invoke({
                "question": user_input,
                "chat_history": [
                    ("human" if m["role"] == "user" else "assistant", m["content"])
                    for m in st.session_state.messages[:-1]
                ]
            })
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
