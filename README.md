🚀 Gemini ChatGPT-Style GenAI Application

A production-grade GenAI chat application built using Google Gemini, LangChain, Streamlit, and LangSmith — featuring ChatGPT-like UI, streaming responses, persistent multi-chat history, and LLMOps observability.

🌟 Features
💬 ChatGPT-Like Experience

Real-time streaming LLM responses

Chat history stored in a sidebar, just like ChatGPT

Automatic chat session naming

Smooth typing cursor + “Thinking…” animations

Elegant glassmorphism UI with background image

🔁 Persistent Multi-Chat Memory

Chats are saved locally in chats.json

Sessions survive app restarts

Search, open, or create chats anytime

⚙️ LLMOps with LangSmith

Built with production standards:

Request tracing

Error visibility

Latency & token monitoring

Debugging & evaluation

🧠 Modern GenAI Stack

Google Gemini 2.5 Flash as the LLM

LangChain for orchestration

Streamlit for frontend

LangSmith for observability

🖼️ UI Preview (Concept)
┌─────────────────────────────── Sidebar ────────────────────────────────┐
│  ➕ New Chat                                                             │
│  🔍 Search chats…                                                       │
│  • First project idea                                                   │
│  • Gemini streaming test                                                │
│  • RAG experiment                                                       │
└──────────────────────────────────────────────────────────────────────────┘

Chat Window:
🤖 Gemini AI v2  
Streaming • Persistent Memory • LLMOps

User: Explain LangSmith  
Assistant: 🤔 Thinking...  
Assistant: LangSmith is an LLMOps platform that enables...▌

🛠️ Tech Stack
Component	Technology
LLM	Google Gemini 2.5 Flash
Framework	LangChain
Frontend	Streamlit
Observability	LangSmith
Persistence	JSON storage (chats.json)
UI	Custom CSS + Glassmorphism
📦 Installation & Setup
1️⃣ Clone the repo
git clone https://github.com/Ashusurya00/advance-chatbot/tree/main
cd advance-chatbot

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add your API keys

Open app.py and update:

GEMINI_API_KEY = "your-key"
LANGSMITH_API_KEY = "your-key"

4️⃣ Run the application
streamlit run app.py

📁 Project Structure
📦 genai-chat-app
 ┣ 📜 app.py              # Main application
 ┣ 📜 chats.json          # Stored sessions (auto-generated)
 ┣ 📜 requirements.txt    # Dependencies
 ┗ 📜 README.md           # Project documentation

🔥 Key Concepts Demonstrated
✔ Streaming LLM responses

Real-time token-by-token rendering for smooth UX.

✔ Persistent chat sessions

Multi-chat memory like ChatGPT.

✔ LLMOps observability

End-to-end tracing, debugging, and monitoring with LangSmith.

✔ Clean architecture

Proper state management & safe UI patterns.

✔ Production UI/UX

Background images, glass effects, animations.

📈 Future Enhancements (Planned)

 Add RAG (PDF / Docs upload)

 Cloud deployment (AWS / GCP / Streamlit Cloud)

 User authentication (login-based chat history)

 Model switcher (Gemini Flash / Pro)

 Chat export to PDF/Markdown

 Voice input + TTS responses


⭐ Support This Project

If you found this project useful, please consider giving it a ⭐ star on GitHub — it helps a lot!

📬 Contact

Feel free to reach out for collaborations, improvements, or discussions on GenAI & LLMOps!

LinkedIn: www.linkedin.com/in/ashutosh-suryawanshi-26aa46378

Email: ashusurya00@gmail.com
