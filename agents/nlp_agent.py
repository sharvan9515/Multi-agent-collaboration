from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import numpy as np

from .base import Agent


class NLPAgent(Agent):
    """Agent that extracts simple NLP features from the message."""

    def __init__(self, corpus: list[str] | None = None):
        # Small default corpus for vectorizer and Word2Vec
        self.corpus = corpus or [
            "Simplilearn offers courses in AI and is also located in the US",
            "AI is becoming part of everyday life and AI is super important",
            "Simplilearn and AI are integral part of everyday life",
        ]
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.corpus)

        tokenized = [sent.lower().split() for sent in self.corpus]
        self.w2v = Word2Vec(sentences=tokenized, vector_size=50, window=5, min_count=1, sg=0)

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        # Compute top keywords with TF-IDF
        tfidf = self.vectorizer.transform([message]).toarray()[0]
        feats = self.vectorizer.get_feature_names_out()
        if tfidf.size:
            top_idx = np.argsort(tfidf)[::-1][:3]
            keywords = [feats[i] for i in top_idx if tfidf[i] > 0]
        else:
            keywords = []
        context["keywords"] = keywords

        # Average Word2Vec embedding for known words
        tokens = [t for t in message.lower().split() if t in self.w2v.wv]
        if tokens:
            vec = np.mean([self.w2v.wv[t] for t in tokens], axis=0)
            preview = np.array2string(vec[:5], precision=3, separator=", ")
        else:
            preview = "no known words"
        response = f"Keywords: {', '.join(keywords)} | w2v[:5]: {preview}"
        return response, context
