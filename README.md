# 🧮 MathsGPT: Text-to-Math Problem Solver & Search Assistant

MathsGPT is an interactive Streamlit-based web application powered by **Llama 3.3** (via Groq) and **LangChain**. It functions as a smart agent capable of solving complex word problems, performing mathematical computations, and searching the web to answer reasoning questions.

---

## 🚀 Features

- **Llama 3.3 Engine**: Fast, state-of-the-art reasoning powered by Groq.
- **LangChain Agent (Zero-Shot React)**: Dynamically decides whether to use a calculator, query Wikipedia, or use logic/reasoning tools.
- **Streamlit Chat Interface**: Interactive chat session with live thought-process tracking.
- **Automatic .env Loading**: Seamless setup using environment variables.

---

## 🛠️ Built-in Tools

1. **Wikipedia Search**: For retrieving background information and general knowledge.
2. **Calculator (LLMMathChain)**: For executing precise mathematical expressions and equations.
3. **Reasoning Engine**: For explaining complex logic and step-by-step word problem solutions.

---

## 💻 Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/rijulthakur34-glitch/MathsGPT.git
cd MathsGPT
```

### 2. Set up a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create a `.env` file in the root directory and add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the App
```bash
streamlit run app.py
```

---


