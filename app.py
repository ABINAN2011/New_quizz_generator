import streamlit as st
import tempfile
import os
import re
from backend import extract_text_from_pdf, split_into_chunks, build_vectorstore, generate_quizz, save_quizz_to_pdf


st.set_page_config(
    page_title="AI Quiz Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin: -1rem -1rem  2rem -1rem;
    border-radius: 10px;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: bold;
}
.quiz-container {
    background-color: black;
    padding: 1.5rem;
    border-radius: 10
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1> AI Quiz Generator</h1>
    
</div>
""", unsafe_allow_html=True)



if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
if 'quiz_content' not in st.session_state:
    st.session_state.quiz_content = ""
if 'quiz_parsed' not in st.session_state:
    st.session_state.quiz_parsed = []
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False



with st.sidebar:
    st.header(" Quiz Features...")
    num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)
    difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])
    topic = st.text_input("Specific Topic (optional)", placeholder="e.g. AI, Machine Learning, History")



col1, col2 = st.columns([1, 1])

with col1:
    st.header(" Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.success(f" File uploaded: {uploaded_file.name}")
        st.info(f" File size: {uploaded_file.size / 1024:.2f} KB")

        if st.button(" Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        temp_pdf_path = tmp_file.name

                    extracted_text = extract_text_from_pdf(temp_pdf_path)

                    if not extracted_text.strip():
                        st.error(" No text could be extracted. Maybe it's a scanned image?")
                    else:
                        chunks = split_into_chunks(extracted_text)
                        st.session_state.vectorstore = build_vectorstore(chunks)
                        st.success(f" PDF processed successfully! Created {len(chunks)} text chunks.")

                        with st.expander(" Preview Extracted Text"):
                            st.text_area("First 1000 characters:", extracted_text[:1000], height=150)

                    os.unlink(temp_pdf_path)

                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")



with col2:
    st.header(" Generate Quiz")

    if st.session_state.vectorstore is not None:
        if st.button(" Generate Quiz"):
            if not topic.strip():
                topic = "general knowledge from the uploaded material"

            with st.spinner(f"Generating {num_questions} questions about '{topic}'..."):
                try:
                    quiz_result = generate_quizz(st.session_state.vectorstore, topic, num_questions, difficulty)

                    if isinstance(quiz_result, dict) and 'result' in quiz_result:
                        st.session_state.quiz_content = quiz_result['result']
                    else:
                        st.session_state.quiz_content = str(quiz_result)

                  
                    parsed = []
                    q_blocks = re.split(r"Q\d+\.", st.session_state.quiz_content)
                    for block in q_blocks:
                        if block.strip():
                            lines = block.strip().splitlines()
                            question = lines[0]
                            options = [line for line in lines[1:5] if line]
                            answer_line = [line for line in lines if "Answer:" in line]
                            answer = answer_line[0].split(":")[-1].strip() if answer_line else None
                            parsed.append({
                                "question": question,
                                "options": options,
                                "answer": answer
                            })
                    st.session_state.quiz_parsed = parsed

                    st.session_state.quiz_generated = True
                    st.success(" Quiz generated successfully!")

                except Exception as e:
                    st.error(f" Error generating quiz: {str(e)}")
    else:
        st.warning(" Please upload and process a PDF first before generating a quiz.")


if st.session_state.quiz_generated and st.session_state.quiz_parsed:
    st.header(" Attend the Quiz...")

    answers = {}
    for i, q in enumerate(st.session_state.quiz_parsed, start=1):
        st.subheader(f"Q{i}. {q['question']}")
        answers[i] = st.radio(
            "Choose an option:",
            options=q["options"],
            key=f"q_{i}"
        )
        st.markdown("---")

    if st.button(" Submit Answers"):
        score = 0
        result_details = []
        for i, q in enumerate(st.session_state.quiz_parsed, start=1):
            correct_opt = q["answer"]
            user_ans = answers[i][0] if answers[i] else None 
            if user_ans == correct_opt:
                score += 1
                result_details.append(f"Q{i}: ✅ Correct")
            else:
                result_details.append(f"Q{i}: ❌ Wrong (Correct: {correct_opt})")

        st.session_state.quiz_submitted = True
        st.success(f"Your Score: {score}/{len(st.session_state.quiz_parsed)}")
        st.write("\n".join(result_details))



if st.session_state.quiz_generated and st.session_state.quiz_content:
    st.header("  Download Quiz")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            label=" Download as TXT",
            data=st.session_state.quiz_content,
            file_name=f"quiz_{topic.replace(' ', '_') if topic else 'general'}.txt",
            mime="text/plain"
        )

    with col2:
        if st.button(" Save as PDF"):
            try:
                pdf_filename = f"quiz_{topic.replace(' ', '_') if topic else 'general'}.pdf"
                save_quizz_to_pdf(st.session_state.quiz_content, pdf_filename)
                st.success(f" Quiz saved as {pdf_filename}")

                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label=" Download PDF",
                        data=pdf_file.read(),
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f" Error saving PDF: {str(e)}")
