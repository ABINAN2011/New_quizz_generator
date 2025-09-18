from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


def extract_text_from_pdf(pdf_file: str) -> str:
    """Extracts all text from a PDF file."""
    loader = PyPDFLoader(pdf_file)
    texts = ""
    for page in loader.load_and_split():
        if page.page_content:
            texts += page.page_content + "\n"
    return texts


def split_into_chunks(texts: str) -> list:
    """
    Splits large text into smaller chunks for embedding.
    Fixed values: chunk_size=800, chunk_overlap=100
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100
    )
    chunks = splitter.split_text(texts)
    return chunks


def build_vectorstore(chunks: list) -> FAISS:
    """Builds a FAISS vector store from text chunks using Ollama embeddings."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    faiss_index = FAISS.from_texts(chunks, embeddings)
    return faiss_index


def generate_quizz(faiss_index: FAISS, topic: str, num_questions: int = 5, difficulty: str = "medium"):
    """Generates a multiple-choice quiz for a given topic using FAISS retrieval and Ollama LLM."""
    retriever = faiss_index.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=1500)

    prompt_template = f"""
You are a quiz generator. Based on the following lecture material, create exactly {num_questions} multiple-choice questions (MCQs) with 4 options each. 

Difficulty level: {difficulty}
Topic focus: {topic if topic else "general content from the material"}

Lecture Material:
{{context}}

Query: {{question}}

Format your response as:
Q1. <question>
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <correct option letter>
"""
    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt, "document_variable_name": "context"}
    )

    if topic:
        query = f"Generate a {difficulty} difficulty quiz with {num_questions} questions about {topic}"
    else:
        query = f"Generate a {difficulty} difficulty quiz with {num_questions} questions from the provided material"

    qa_output = qa_chain.invoke({"query": query})
    return qa_output


def save_quizz_to_pdf(quizz_text: str, output_file: str = "quizz_output.pdf"):
    """Saves the generated quiz text into a PDF file."""
    doc = SimpleDocTemplate(output_file)
    styles = getSampleStyleSheet()
    story = []

    for line in quizz_text.split('\n'):
        if line.strip():
            paragraph = Paragraph(line, styles['Normal'])
            story.append(paragraph)
            story.append(Spacer(1, 12))

    doc.build(story)
    print(f" Quiz saved to {output_file}")
