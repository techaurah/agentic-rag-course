"""Smoke test for Lesson 13: Reranking: the second pass, and when it does not pay.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "reranking.py")
    spec = importlib.util.spec_from_file_location("lesson_13_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['raw'] == {'fact_recall_at_5': 0.9808, 'doc_recall_at_5': 0.9808, 'precision_at_3': 0.6026, 'precision_at_5': 0.5231, 'fact_at_1': 0.75}, ('raw', result.get('raw'))
    assert result['reranked'] == {'fact_recall_at_5': 0.9808, 'doc_recall_at_5': 0.9615, 'precision_at_3': 0.4615, 'precision_at_5': 0.4154, 'fact_at_1': 0.7885}, ('reranked', result.get('reranked'))
    assert result['num_rerank_fact_at_1'] == 0.7692, ('num_rerank_fact_at_1', result.get('num_rerank_fact_at_1'))
    print("smoke ok: Lesson 13 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
