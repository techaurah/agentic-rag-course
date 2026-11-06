"""Smoke test for Lesson 03: Chunking from first principles: size, overlap, and boundaries.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "chunking.py")
    spec = importlib.util.spec_from_file_location("lesson_03_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['whole_chunks'] == 24, ('whole_chunks', result.get('whole_chunks'))
    assert result['paragraph_chunks'] == 84, ('paragraph_chunks', result.get('paragraph_chunks'))
    assert result['section_chunks'] == 84, ('section_chunks', result.get('section_chunks'))
    assert result['whole_fact_recall_at_5'] == 1.0, ('whole_fact_recall_at_5', result.get('whole_fact_recall_at_5'))
    assert result['paragraph_fact_recall_at_5'] == 0.9808, ('paragraph_fact_recall_at_5', result.get('paragraph_fact_recall_at_5'))
    print("smoke ok: Lesson 03 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
