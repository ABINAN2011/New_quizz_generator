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

3) ▶️ Run the Application
```bash
streamlit run app.py
```

📘 Example Workflow

1) Upload a PDF containing lecture notes

2) Click “Process PDF” to extract and chunk text

3) Choose the number of questions, difficulty, and topic

4) Click “Generate Quiz”

5) Take the quiz, submit answers, and download it as PDF or TXT

📂 Project Structure
```bash
📦 ai-quiz-generator
├── app.py                 # Streamlit frontend
├── backend.py             # Core logic for extraction, embeddings, and quiz generation
├── requirements.txt       # Dependencies
├── .env                   # Groq API key
└── README.md              # Project documentation
```

🤝 Contributing
Contributions are welcome!

If you’d like to add features or improve this project:

1) Fork this repository
2) Create a new branch
3) Make your changes
4) Submit a pull request 

   
## ❤️ Acknowledgments

- **[LangChain](https://www.langchain.com/)** – for document processing pipelines  
- **[FAISS](https://github.com/facebookresearch/faiss)** – for efficient vector similarity search  
- **[Groq](https://groq.com/)** – for fast inference and LLM access  
- **[Streamlit](https://streamlit.io/)** – for building the web app  
- **[ReportLab](https://www.reportlab.com/)** – for PDF generation


📜 License

This project is licensed under the MIT License – feel free to use and modify.

<p align="center"> Built with ❤️ by <b>Abinan Ketheeswaran</b> <br> <a href="mailto:k.abinan20@gmail.com">k.abinan20@gmail.com</a> · <a href="https://github.com/ABINAN201">GitHub</a> </p> ```
  


