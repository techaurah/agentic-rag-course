"""Smoke test for Lesson 09: The hashing embedder: a deterministic stand-in.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "hashing_embedder.py")
    spec = importlib.util.spec_from_file_location("lesson_09_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_at_5'] == 1.0, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 0.9615, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['mrr'] == 0.9423, ('mrr', result.get('mrr'))
    assert result['worst_fact_recall'] == 0.0, ('worst_fact_recall', result.get('worst_fact_recall'))
    assert result['dimensions'] == 256, ('dimensions', result.get('dimensions'))
    assert result['deterministic'] == True, ('deterministic', result.get('deterministic'))
    assert result['word_order_blind'] == True, ('word_order_blind', result.get('word_order_blind'))
    assert result['unit_norm'] == 1.0, ('unit_norm', result.get('unit_norm'))
    print("smoke ok: Lesson 09 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
