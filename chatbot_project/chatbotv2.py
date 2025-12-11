import os
import json
import uuid
import time
import streamlit as st
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# =======================
# 🔐 API KEYS
# =======================
GEMINI_API_KEY = ""
LANGCHAIN_API_KEY = ""

# =======================
# 🔍 LangSmith (LLMOps)
# =======================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Gemini-Chat-v2"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# =======================
# 📦 Storage
# =======================
DB_FILE = "chats.json"

def load_chats():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chats(chats):
    with open(DB_FILE, "w") as f:
        json.dump(chats, f, indent=2)

# =======================
# 🎨 Streamlit Config
# =======================
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🤖",
    layout="wide"
)

# =======================
# 🎨 Glassmorphism UI
# =======================
st.markdown("""
<style>
.stApp {
  background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}
[data-testid="stSidebar"] {
  background: rgba(15,15,15,0.85);
}
.chat-message {
  background: rgba(255,255,255,0.07);
  border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# 🧠 Session Init
# =======================
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# =======================
# 🧠 Sidebar
# =======================
st.sidebar.title("💬 Chats")

def new_chat():
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "created": datetime.now().isoformat(),
        "messages": []
    }
    st.session_state.current_chat = cid
    save_chats(st.session_state.chats)

if st.sidebar.button("➕ New Chat"):
    new_chat()
    st.rerun()

search = st.sidebar.text_input("🔍 Search chats")

for cid, chat in st.session_state.chats.items():
    if search.lower() in chat["title"].lower():
        if st.sidebar.button(chat["title"], key=cid):
            st.session_state.current_chat = cid
            st.rerun()

# =======================
# 🚫 No chat selected
# =======================
if not st.session_state.current_chat:
    st.title("🤖 Gemini AI v2")
    st.info("Start a new chat from sidebar")
    st.stop()

chat = st.session_state.chats[st.session_state.current_chat]

# =======================
# 🖥 Main UI
# =======================
st.title(chat["title"])
st.caption("Streaming • Persistent Memory • LLMOps")

# =======================
# 💬 Show Messages
# =======================
for m in chat["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# =======================
# 🧠 Prompt
# =======================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_API_KEY,
    streaming=True,
    temperature=0.2
)

chain = prompt | llm | StrOutputParser()

# =======================
# 🧑 Input
# =======================
user_input = st.chat_input("Ask anything...")

if user_input:
    if chat["title"] == "New Chat":
        chat["title"] = user_input[:40]

    chat["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        box = st.empty()

        # Animated thinking
        for dots in ["Thinking.", "Thinking..", "Thinking..."]:
            box.markdown(f"🤔 **{dots}**")
            time.sleep(0.3)

        answer = ""
        for chunk in chain.stream({
            "question": user_input,
            "chat_history": [
                ("human" if m["role"] == "user" else "assistant", m["content"])
                for m in chat["messages"][:-1]
            ]
        }):
            answer += chunk
            box.markdown(answer + "▌")

        box.markdown(answer)

    chat["messages"].append({"role": "assistant", "content": answer})
    save_chats(st.session_state.chats)

