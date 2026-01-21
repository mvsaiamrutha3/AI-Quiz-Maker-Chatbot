# 🧠 AI Quiz Maker Chatbot  
**Streamlit · OpenAI LLM · SerpAPI · DOCX/JSON Export**

An **AI-powered, conversational Quiz Maker Chatbot** built with **Python and Streamlit**, leveraging **OpenAI Large Language Model (LLMs)** together with **internet-enabled tools (SerpAPI)** to support **end-to-end quiz creation**.

The application allows users to **generate, modify, validate, reorder, and export quizzes** entirely through **natural language interaction**, with a modern and interactive user interface.

---

## 📸 Screenshots

### Main Chat Interface
<img width="957" height="443" alt="Intro1" src="https://github.com/user-attachments/assets/4b4912b9-34c2-4184-9d1c-98228cca1056" />


### Quiz Loaded & Interactive Editing
<img width="959" height="439" alt="Quiz_edit" src="https://github.com/user-attachments/assets/51765418-c3c3-4ee7-9d7c-5b5b20e467cb" />


---

## ✨ Features

### 🤖 Conversational Quiz Generation
- Generate complete quizzes by chatting with the AI
- Topic-based, category-based, and contextual question generation
- Internet-enabled generation ensures **accurate and up-to-date content**

### ✏️ Natural Language Quiz Editing
- Modify question text
- Update or rewrite answer options
- Change the correct answer
- Add new questions
- Delete existing questions
- Apply edits to a **selected question** using chat commands

### 🌐 Internet-Aware Question Creation & Validation (SerpAPI)
- Real-time web search for:
  - Accurate question generation
  - Answer verification
  - Content refinement
- Internet access is used for the **entire quiz creation pipeline**, not just validation

### 🧩 Interactive User Interface
- Split-screen layout:
  - Chatbot on the left
  - Quiz preview on the right
- Drag-and-drop:
  - Reorder questions
  - Reorder categories
- Inline editing of questions and options
- Visual highlights for:
  - Selected questions
  - Correct answers

### 📂 Import & Export
- Load quizzes from:
  - **JSON**
  - **DOCX**
- Export final quizzes to:
  - **JSON**
  - **DOCX**

---

## 🧠 How It Works

1. User sends a natural language command via the chat interface
2. The LLM interprets the command using a **strict system prompt**
3. The intent is converted into a **single structured JSON tool call**
4. The backend applies the requested quiz operation
5. The UI updates instantly
6. The quiz can be exported at any time

---

## 🧩 Tool-Based Command System

The application uses a **deterministic tool-based architecture** to safely modify quiz content.

Each user command maps to exactly one tool:

- `edit_question_text` – Modify a question
- `edit_option_text` – Modify an option
- `change_correct_answer` – Update the correct answer
- `add_new_question` – Add a new question
- `delete_question` – Remove a question

This approach prevents hallucinated edits and ensures predictable behavior.

---

🛠️ Tech Stack

Backend: Python (Streamlit)

LLM: OpenAI

Web Search: SerpAPI

Frontend: HTML, Tailwind CSS, JavaScript

UI Libraries: SortableJS, DOCX.js

Data Formats: JSON, DOCX

🚀 Setup & Usage
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-quiz-maker-chatbot.git
cd ai-quiz-maker-chatbot

2️⃣ Install Dependencies

Ensure Python 3.9+ is installed.

pip install -r requirements.txt

3️⃣ Configure API Keys

Create a cred.env (or .env) file in the project root and add:

OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key

4️⃣ Run the Streamlit Backend
streamlit run app.py

5️⃣ Open the Frontend UI

After the backend is running:

Open quiz_app.html directly in a browser
OR

Serve it locally (recommended):

python -m http.server 8000


Then open:

http://localhost:8000/quiz_app.html

6️⃣ Start Using the Application

You can now generate quizzes, edit questions via chat, validate answers using web search, and export quizzes to JSON or DOCX.

🎯 Use Cases

Educators creating quizzes quickly

Students generating practice assessments

Interview and exam preparation

AI-assisted learning platforms
