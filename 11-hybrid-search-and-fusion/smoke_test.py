"""Smoke test for Lesson 11: Hybrid search and fusion: reciprocal rank fusion.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "hybrid.py")
    spec = importlib.util.spec_from_file_location("lesson_11_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_at_5'] == 0.9808, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 0.9808, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['mrr'] == 0.9231, ('mrr', result.get('mrr'))
    assert result['tfidf_worst'] == 0.5, ('tfidf_worst', result.get('tfidf_worst'))
    assert result['bm25_worst'] == 0.0, ('bm25_worst', result.get('bm25_worst'))
    assert result['vector_worst'] == 0.0, ('vector_worst', result.get('vector_worst'))
    assert result['hybrid_worst'] == 0.5, ('hybrid_worst', result.get('hybrid_worst'))
    assert result['below_perfect_counts'] == {'tfidf': 1, 'bm25': 1, 'vector': 1, 'hybrid': 1}, ('below_perfect_counts', result.get('below_perfect_counts'))
    print("smoke ok: Lesson 11 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
