import streamlit as st
from chat_engine.chat_engine import ChatEngine
from chat_engine.modules.retriever import default_retriever
from chat_engine.modules.prompt_assembler import default_prompt_assembler
from embedding.embedder import embed_text
from language_model.language_model import generate_answer
from vector_store.base import init_collection
from agents.nlp_agent import NLPAgent

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
    st.session_state.nlp_agent = NLPAgent()
    st.session_state.history = []

st.title("RAG_HEITAA Health Assistant")

agent_choice = st.selectbox(
    "Choose agent",
    ["RAG", "NLP"],
)

user_input = st.text_input("Ask a question about your claim:", key="input")
if st.button("Send") and user_input:
    if agent_choice == "RAG":
        engine = st.session_state.engine
        answer = engine.answer_query(user_input)
    else:
        agent = st.session_state.nlp_agent
        answer, _ = agent.act(user_input, {})
    st.session_state.history.append((user_input, answer))

for i, (q, a) in enumerate(reversed(st.session_state.history)):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Assistant:** {a}")
