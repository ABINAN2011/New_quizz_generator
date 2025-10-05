# 🤖 AI Quiz Generator

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-red?logo=streamlit" />
  <img src="https://img.shields.io/badge/LangChain-Enabled-blue?logo=python" />
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-green" />
  <img src="https://img.shields.io/badge/Groq-LLM-yellow" />
</p>

## 🧠 Overview

The **AI Quiz Generator** is a smart, interactive web application that automatically generates **multiple-choice quizzes** from uploaded **PDF documents**.  
It uses **LangChain**, **FAISS**, and **Groq’s Llama 3.3 model** to analyze lecture materials or study notes, and create topic-focused, difficulty-adjusted quizzes.

---

## 🚀 Features

✅ Upload and process **PDF lecture notes**  
✅ Extract text and create **vector embeddings**  
✅ Generate **AI-powered MCQs** using **Groq Llama 3.3**  
✅ Choose quiz **difficulty levels** (Easy / Medium / Hard)  
✅ Specify a **custom topic** (optional)  
✅ Take the quiz directly in the Streamlit app  
✅ Download the quiz as **TXT or PDF**  

---

## 🏗️ Project Architecture

graph TD
    A[Upload PDF] --> B[Extract & Split Text]
    B --> C[Build FAISS Vector Store]
    C --> D[Query Groq LLM (Llama 3.3)]
    D --> E[Generate MCQs]
    E --> F[Display & Download Quiz]

⚙️ Tech Stack

| Component           | Technology Used                |
| ------------------- | ------------------------------ |
| **Frontend**        | Streamlit                      |
| **Backend**         | LangChain                      |
| **Embeddings**      | Ollama (nomic-embed-text)      |
| **Vector Database** | FAISS                          |
| **LLM**             | Groq – Llama 3.3 70B Versatile |
| **PDF Handling**    | LangChain PyPDFLoader          |
| **PDF Export**      | ReportLab                      |

1) 🧩 Installation
Clone this repository and install dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/ai-quiz-generator.git
cd ai-quiz-generator
pip install -r requirements.txt
```
2) 🔐 Configure Environment Variables
Create a .env file and add your Groq API key:
```bash
GROQ_API_KEY=your_api_key_here
```

3) 
