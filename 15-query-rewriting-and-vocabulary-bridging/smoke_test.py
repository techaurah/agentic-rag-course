"""Smoke test for Lesson 15: Query rewriting and vocabulary bridging.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "rewriting.py")
    spec = importlib.util.spec_from_file_location("lesson_15_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['gap_bm25_before'] == 0.6667, ('gap_bm25_before', result.get('gap_bm25_before'))
    assert result['gap_bm25_after'] == 1.0, ('gap_bm25_after', result.get('gap_bm25_after'))
    assert result['gap_hybrid_before'] == 0.8333, ('gap_hybrid_before', result.get('gap_hybrid_before'))
    assert result['gap_hybrid_after'] == 1.0, ('gap_hybrid_after', result.get('gap_hybrid_after'))
    assert result['golden_bm25_before'] == 0.9615, ('golden_bm25_before', result.get('golden_bm25_before'))
    assert result['golden_bm25_after'] == 0.9615, ('golden_bm25_after', result.get('golden_bm25_after'))
    assert result['synonym_rows'] == 7, ('synonym_rows', result.get('synonym_rows'))
    print("smoke ok: Lesson 15 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
