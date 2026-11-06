"""Smoke test for Lesson 16: Query decomposition: one question, several retrievals.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "decomposition.py")
    spec = importlib.util.spec_from_file_location("lesson_16_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['multihop_questions'] == 5, ('multihop_questions', result.get('multihop_questions'))
    assert result['single_shot_doc_recall'] == 0.9, ('single_shot_doc_recall', result.get('single_shot_doc_recall'))
    assert result['auto_union_doc_recall'] == 0.8, ('auto_union_doc_recall', result.get('auto_union_doc_recall'))
    assert result['hand_union_doc_recall'] == 1.0, ('hand_union_doc_recall', result.get('hand_union_doc_recall'))
    assert result['questions_auto_split'] == 1, ('questions_auto_split', result.get('questions_auto_split'))
    print("smoke ok: Lesson 16 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
