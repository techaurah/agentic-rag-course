"""Smoke test for Lesson 30: Evaluate and harden the capstone.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "evaluate_capstone.py")
    spec = importlib.util.spec_from_file_location("lesson_30_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['all_gates_pass'] == True, ('all_gates_pass', result.get('all_gates_pass'))
    assert result['doc_recall_at_5'] == 0.9808, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 0.9808, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['refusal_correct'] == 5, ('refusal_correct', result.get('refusal_correct'))
    assert result['false_refusals'] == 0, ('false_refusals', result.get('false_refusals'))
    assert result['restricted_leaks'] == 0, ('restricted_leaks', result.get('restricted_leaks'))
    assert result['gates_pass'] == {'doc_recall_at_5': True, 'fact_recall_at_5': True, 'citation_coverage': True, 'grounded': True, 'refusal_correct': True, 'false_refusals': True, 'restricted_leaks': True, 'mean_latency_ms': True}, ('gates_pass', result.get('gates_pass'))
    print("smoke ok: Lesson 30 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
