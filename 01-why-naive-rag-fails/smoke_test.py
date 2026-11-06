"""Smoke test for Lesson 01: Why naive RAG fails: the five failure modes.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "naive_rag.py")
    spec = importlib.util.spec_from_file_location("lesson_01_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_at_5'] == 1.0, ('doc_recall_at_5', result.get('doc_recall_at_5'))
    assert result['fact_recall_at_5'] == 1.0, ('fact_recall_at_5', result.get('fact_recall_at_5'))
    assert result['mrr'] == 0.9295, ('mrr', result.get('mrr'))
    assert result['public_questions'] == 30, ('public_questions', result.get('public_questions'))
    assert result['leaking_questions'] == 11, ('leaking_questions', result.get('leaking_questions'))
    assert result['refuse_questions_answered'] == 6, ('refuse_questions_answered', result.get('refuse_questions_answered'))
    assert result['avg_context_words'] == 420, ('avg_context_words', result.get('avg_context_words'))
    print("smoke ok: Lesson 01 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
