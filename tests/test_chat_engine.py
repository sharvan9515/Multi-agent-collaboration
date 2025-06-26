import importlib
import sys
import types

import pytest


@pytest.fixture(autouse=True)
def stub_external_modules(monkeypatch):
    """Provide lightweight stand-ins for heavy external modules."""
    import os
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    # embedding.embedder
    embedding = types.ModuleType("embedding")
    embedder = types.ModuleType("embedding.embedder")
    embedder.embed_text = lambda text: [0.1, 0.2]
    embedding.embedder = embedder
    monkeypatch.setitem(sys.modules, "embedding", embedding)
    monkeypatch.setitem(sys.modules, "embedding.embedder", embedder)

    # vector_store.base
    vector_store = types.ModuleType("vector_store")
    base = types.ModuleType("vector_store.base")
    class DummyResult:
        def __init__(self, payload):
            self.payload = payload
    base.DummyResult = DummyResult
    base.query_vector = lambda vec, top_k=5: [DummyResult({"text": "ctx"})]
    vector_store.base = base
    monkeypatch.setitem(sys.modules, "vector_store", vector_store)
    monkeypatch.setitem(sys.modules, "vector_store.base", base)

    # language_model.language_model
    language_model = types.ModuleType("language_model")
    lm_mod = types.ModuleType("language_model.language_model")
    lm_mod.generate_answer = lambda messages: "assistant response"
    language_model.language_model = lm_mod
    monkeypatch.setitem(sys.modules, "language_model", language_model)
    monkeypatch.setitem(sys.modules, "language_model.language_model", lm_mod)

    yield


def test_answer_query_updates_history():
    ce_module = importlib.import_module("chat_engine.chat_engine")
    ChatEngine = ce_module.ChatEngine

    def fake_embedder(text):
        return [1, 1, 1]

    class DummyRes:
        def __init__(self, payload):
            self.payload = payload

    def fake_retriever(vec, top_k=3):
        return [DummyRes({"text": "retrieved"})]

    assistant_reply = "ok"
    def fake_llm(prompt):
        return assistant_reply

    def fake_prompt_assembler(user_query, context, history):
        return "prompt"

    engine = ChatEngine(
        retriever=fake_retriever,
        embedder=fake_embedder,
        llm=fake_llm,
        prompt_assembler=fake_prompt_assembler,
    )

    user_msg = "hello"
    result = engine.answer_query(user_msg)
    assert result == assistant_reply
    assert engine.session.history == [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": assistant_reply},
    ]
