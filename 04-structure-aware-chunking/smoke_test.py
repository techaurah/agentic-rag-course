"""Smoke test for Lesson 04: Structure aware chunking: sections and parent-child retrieval.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "structure_chunking.py")
    spec = importlib.util.spec_from_file_location("lesson_04_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['children'] == 84, ('children', result.get('children'))
    assert result['sections'] == 84, ('sections', result.get('sections'))
    assert result['child_fact_recall_at_5'] == 0.9615, ('child_fact_recall_at_5', result.get('child_fact_recall_at_5'))
    assert result['parent_fact_recall_at_5'] == 0.9615, ('parent_fact_recall_at_5', result.get('parent_fact_recall_at_5'))
    assert result['parent_avg_context_words'] == 118, ('parent_avg_context_words', result.get('parent_avg_context_words'))
    print("smoke ok: Lesson 04 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
