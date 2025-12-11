import os
import uuid
import streamlit as st
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# =====================================================
# 🔐 API KEYS (TEMPORARY – MOVE TO SECRETS LATER)
# =====================================================
GEMINI_API_KEY = ""
LANGSMITH_API_KEY = ""

# =====================================================
# 🔍 LangSmith Tracing (LLMOps)
# =====================================================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Gemini-ChatGPT-Style-App"
os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY

# =====================================================
# 🎨 Streamlit Page Config
# =====================================================
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# 🎨 Background Image + Styling
# =====================================================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1526378722484-d9ab4f2c3f62");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 15, 0.85);
    }
    .chat-message {
        background: rgba(0,0,0,0.55);
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 🧠 Sidebar – Chat Manager
# =====================================================
st.sidebar.title("💬 Chats")

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": []
    }
    st.session_state.current_chat_id = chat_id

# ➕ New Chat
if st.sidebar.button("➕ New Chat"):
    create_new_chat()
    st.rerun()

# 📂 Existing Chats
for chat_id, chat in st.session_state.chats.items():
    if st.sidebar.button(chat["title"], key=chat_id):
        st.session_state.current_chat_id = chat_id
        st.rerun()

# =====================================================
# 🚫 No Chat Selected
# =====================================================
if st.session_state.current_chat_id is None:
    st.title("🤖 Gemini AI Chatbot")
    st.info("👈 Start a new chat from the sidebar")
    st.stop()

current_chat = st.session_state.chats[st.session_state.current_chat_id]

# =====================================================
# 🖥️ Main Chat UI
# =====================================================
st.title("🤖 Gemini AI")
st.caption("Streaming • Thinking State • Sidebar Chat Resume • LangSmith")

# =====================================================
# 💬 Display Messages
# =====================================================
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================================
# 🧠 Prompt
# =====================================================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

# =====================================================
# 🤖 Gemini LLM (Streaming Enabled)
# =====================================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=GEMINI_API_KEY,
    streaming=True
)

chain = prompt | llm | StrOutputParser()

# =====================================================
# 🧑 User Input
# =====================================================
user_input = st.chat_input("Ask something...")

if user_input:
    # Auto rename chat from first prompt
    if current_chat["title"] == "New Chat":
        current_chat["title"] = user_input[:35]

    # Save user message
    current_chat["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # =================================================
    # 🤔 Thinking + Streaming Response
    # =================================================
    with st.chat_message("assistant"):
        placeholder = st.empty()

        # Step 1: Thinking state
        placeholder.markdown("🤔 **Thinking...**")

        full_response = ""

        # Step 2: Stream tokens
        for chunk in chain.stream({
            "question": user_input,
            "chat_history": [
                ("human" if m["role"] == "user" else "assistant", m["content"])
                for m in current_chat["messages"][:-1]
            ]
        }):
            full_response += chunk
            placeholder.markdown(full_response + "▌")

        # Step 3: Final render
        placeholder.markdown(full_response)

    # Save assistant message
    current_chat["messages"].append({
        "role": "assistant",
        "content": full_response
    })
