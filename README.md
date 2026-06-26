# 🤖 Project J.A.R.V.I.S.

**J.A.R.V.I.S. (Just A Rather Very Intelligent System)** is a locally-hosted AI personal assistant inspired by Iron Man's J.A.R.V.I.S., built using Python, Ollama, and open-source Large Language Models.

The project aims to provide an intelligent, privacy-focused assistant capable of conversation, memory, reasoning, voice interaction, and real-time information retrieval — all running locally.

---

## ✨ Features

* Local LLM integration using Ollama
* Conversational memory
* Persistent long-term memory using SQLite
* Custom Jarvis personality layer
* Streamlit-based user interface
* Real-time web search integration
* Context augmentation using web results
* Adaptive reasoning (`think=True/False`)
* Voice input and text-to-speech support
* Fully local execution

---

## 🛠️ Tech Stack

* Python
* Ollama
* Qwen3 8B
* SQLite
* Streamlit
* Git
* VS Code

---

## 📂 Project Structure

```text
Project Jarvis/
│
├── automation/
├── data/
├── database/
├── docs/
├── llm/
├── memory/
├── rag/
├── tools/
├── ui/
├── voice/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Running the Project

### Clone the repository

```bash
git clone https://github.com/yourusername/project-jarvis.git
cd project-jarvis
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start Ollama

```bash
ollama serve
```

### Pull the model

```bash
ollama pull qwen3:8b
```

### Launch Jarvis

```bash
streamlit run ui/app_ui.py
```
