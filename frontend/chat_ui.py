import streamlit as st
from core.chat_engine.chat_engine import ChatEngine
from core.chat_engine.modules.retriever import default_retriever
from core.chat_engine.modules.prompt_assembler import default_prompt_assembler
from core.embedding.embedder import embed_text
from core.language_model.language_model import generate_answer
from core.vector_store.base import init_collection

st.set_page_config(page_title="RAG_HEITAA Chat", page_icon="🩺")

# Initialize resources once per session
if "engine" not in st.session_state:
    init_collection()
    st.session_state.engine = ChatEngine(
        retriever=default_retriever,
        embedder=embed_text,
        llm=generate_answer,
        prompt_assembler=default_prompt_assembler,
    )
    st.session_state.history = []

st.title("RAG_HEITAA Health Assistant")

user_input = st.text_input("Ask a question about your claim:", key="input")
if st.button("Send") and user_input:
    engine = st.session_state.engine
    answer = engine.answer_query(user_input)
    st.session_state.history.append((user_input, answer))

for i, (q, a) in enumerate(reversed(st.session_state.history)):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Assistant:** {a}")
