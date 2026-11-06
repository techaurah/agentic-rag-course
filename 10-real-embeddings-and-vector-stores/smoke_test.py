"""Smoke test for Lesson 10: Real embeddings and vector stores (optional extras).

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "embeddings_extras.py")
    spec = importlib.util.spec_from_file_location("lesson_10_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['canonical_path'] == 'stdlib hashing stand-in (Lesson 09)', ('canonical_path', result.get('canonical_path'))
    assert result['standin_doc_recall_at_5'] == 1.0, ('standin_doc_recall_at_5', result.get('standin_doc_recall_at_5'))
    assert result['standin_fact_recall_at_5'] == 0.9615, ('standin_fact_recall_at_5', result.get('standin_fact_recall_at_5'))
    assert result['extras_required_for_course'] == False, ('extras_required_for_course', result.get('extras_required_for_course'))
    print("smoke ok: Lesson 10 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
