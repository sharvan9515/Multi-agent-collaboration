import importlib
import sys
import types

import pytest


@pytest.fixture(autouse=True)
def stub_modules(monkeypatch):
    """Stub heavy dependencies for rag_implementation tests."""
    import os
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    embedding = types.ModuleType("embedding")
    embedder = types.ModuleType("embedding.embedder")
    embedder.embed_text = lambda text: [0.1, 0.2]
    embedding.embedder = embedder
    monkeypatch.setitem(sys.modules, "embedding", embedding)
    monkeypatch.setitem(sys.modules, "embedding.embedder", embedder)

    vector_store = types.ModuleType("vector_store")
    base = types.ModuleType("vector_store.base")
    class DummyResult:
        def __init__(self, payload):
            self.payload = payload
    base.DummyResult = DummyResult
    base.query_vector = lambda vec, top_k=5, filters=None: [DummyResult({"text": "ctx"})]
    vector_store.base = base
    monkeypatch.setitem(sys.modules, "vector_store", vector_store)
    monkeypatch.setitem(sys.modules, "vector_store.base", base)

    language_model = types.ModuleType("language_model")
    lm_mod = types.ModuleType("language_model.language_model")
    lm_mod.generate_answer = lambda messages: "assistant response"
    language_model.language_model = lm_mod
    monkeypatch.setitem(sys.modules, "language_model", language_model)
    monkeypatch.setitem(sys.modules, "language_model.language_model", lm_mod)

    yield


def test_answer_query_returns_llm_output():
    mod = importlib.import_module("question_answering.rag_implementation")
    result = mod.answer_query("hello")
    assert result == "assistant response"
