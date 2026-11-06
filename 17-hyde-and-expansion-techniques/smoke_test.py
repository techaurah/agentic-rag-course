"""Smoke test for Lesson 17: HyDE and expansion techniques: promise and caveats.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "hyde_expansion.py")
    spec = importlib.util.spec_from_file_location("lesson_17_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['paraphrase_bm25_before'] == 1.0, ('paraphrase_bm25_before', result.get('paraphrase_bm25_before'))
    assert result['paraphrase_bm25_hyde'] == 0.8889, ('paraphrase_bm25_hyde', result.get('paraphrase_bm25_hyde'))
    assert result['gap_bm25_before'] == 0.6667, ('gap_bm25_before', result.get('gap_bm25_before'))
    assert result['gap_bm25_prf'] == 0.5, ('gap_bm25_prf', result.get('gap_bm25_prf'))
    assert result['gap_prf_per_question'] == [0.0, 1.0, 0.0, 1.0, 0.0, 1.0], ('gap_prf_per_question', result.get('gap_prf_per_question'))
    print("smoke ok: Lesson 17 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
