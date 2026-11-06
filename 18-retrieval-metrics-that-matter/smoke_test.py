"""Smoke test for Lesson 18: Retrieval metrics that matter.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "metrics_lab.py")
    spec = importlib.util.spec_from_file_location("lesson_18_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['hybrid_per_type_fact_recall'] == {'freshness': 1.0, 'multihop': 0.9, 'paraphrase': 1.0, 'permission': 1.0, 'single': 1.0}, ('hybrid_per_type_fact_recall', result.get('hybrid_per_type_fact_recall'))
    assert result['metrics_defined'] == ['doc_recall_at_5', 'fact_recall_at_5', 'mrr', 'worst_fact_recall', 'questions_below_perfect'], ('metrics_defined', result.get('metrics_defined'))
    print("smoke ok: Lesson 18 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
