"""Smoke test for Lesson 05: TF-IDF from scratch: tokenisation and term statistics.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "tfidf.py")
    spec = importlib.util.spec_from_file_location("lesson_05_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_at_5'] == 0.9808, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 0.9808, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['mrr'] == 0.8731, ('mrr', result.get('mrr'))
    assert result['worst_fact_recall'] == 0.5, ('worst_fact_recall', result.get('worst_fact_recall'))
    assert result['chunks'] == 84, ('chunks', result.get('chunks'))
    print("smoke ok: Lesson 05 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
