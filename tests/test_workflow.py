import importlib
import sys
import types

import pytest


@pytest.fixture(autouse=True)
def stub_modules(monkeypatch):
    """Stub heavy dependencies for workflow tests."""
    import os
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    # Reuse stubs from test_chat_engine
    embedding = types.ModuleType("core.embedding")
    embedder = types.ModuleType("core.embedding.embedder")
    embedder.embed_text = lambda text: [0.1, 0.2]
    embedding.embedder = embedder
    monkeypatch.setitem(sys.modules, "core.embedding", embedding)
    monkeypatch.setitem(sys.modules, "core.embedding.embedder", embedder)

    vector_store = types.ModuleType("core.vector_store")
    base = types.ModuleType("core.vector_store.base")
    class DummyResult:
        def __init__(self, payload):
            self.payload = payload
    base.DummyResult = DummyResult
    base.query_vector = lambda vec, top_k=5, filters=None: [DummyResult({"text": "ctx"})]
    vector_store.base = base
    monkeypatch.setitem(sys.modules, "core.vector_store", vector_store)
    monkeypatch.setitem(sys.modules, "core.vector_store.base", base)

    language_model = types.ModuleType("core.language_model")
    lm_mod = types.ModuleType("core.language_model.language_model")
    lm_mod.generate_answer = lambda messages: "assistant response"
    language_model.language_model = lm_mod
    monkeypatch.setitem(sys.modules, "core.language_model", language_model)
    monkeypatch.setitem(sys.modules, "core.language_model.language_model", lm_mod)

    yield


def test_workflow_runs_with_rag_agent():
    workflow_module = importlib.import_module("core.workflow")
    rag_mod = importlib.import_module("core.agents.rag_agent")

    wf = workflow_module.Workflow([rag_mod.RAGAgent()])
    output = wf.run("hello")
    assert output == "assistant response"

