"""Smoke test for Lesson 07: Lexical failure modes: the vocabulary gap.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "vocab_gap.py")
    spec = importlib.util.spec_from_file_location("lesson_07_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['gap_fact_recall_at_5'] == 0.6667, ('gap_fact_recall_at_5', result.get('gap_fact_recall_at_5'))
    assert result['gap_scores'] == [0.0, 1.0, 0.0, 1.0, 1.0, 1.0], ('gap_scores', result.get('gap_scores'))
    assert result['gap_failing'] == ['g1', 'g3'], ('gap_failing', result.get('gap_failing'))
    print("smoke ok: Lesson 07 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
