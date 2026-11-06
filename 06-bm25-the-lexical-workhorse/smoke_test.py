"""Smoke test for Lesson 06: BM25: the lexical workhorse.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "bm25.py")
    spec = importlib.util.spec_from_file_location("lesson_06_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_at_5'] == 0.9615, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 0.9615, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['mrr'] == 0.9359, ('mrr', result.get('mrr'))
    assert result['sensitivity'] == {'k1=1.2,b=0.75': 0.9615, 'k1=1.5,b=0.75': 0.9615, 'k1=2.0,b=0.75': 0.9615, 'k1=1.5,b=0.5': 0.9615, 'k1=1.5,b=1.0': 0.9615}, ('sensitivity', result.get('sensitivity'))
    print("smoke ok: Lesson 06 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
