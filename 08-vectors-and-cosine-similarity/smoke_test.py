"""Smoke test for Lesson 08: Vectors and cosine similarity: the geometry of meaning (and its limits).

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "cosine.py")
    spec = importlib.util.spec_from_file_location("lesson_08_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['chunk_0'] == 0.7071, ('chunk_0', result.get('chunk_0'))
    assert result['chunk_1'] == 0.4082, ('chunk_1', result.get('chunk_1'))
    assert result['chunk_2'] == 0.0, ('chunk_2', result.get('chunk_2'))
    assert result['disjoint_question_score'] == 0.0, ('disjoint_question_score', result.get('disjoint_question_score'))
    assert result['doubled_chunk_score'] == 0.7071, ('doubled_chunk_score', result.get('doubled_chunk_score'))
    print("smoke ok: Lesson 08 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
