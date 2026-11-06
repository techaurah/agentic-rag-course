"""Smoke test for Lesson 19: Building a golden set: questions that can fail you.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "golden_audit.py")
    spec = importlib.util.spec_from_file_location("lesson_19_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['questions'] == 32, ('questions', result.get('questions'))
    assert result['unique_ids'] == True, ('unique_ids', result.get('unique_ids'))
    assert result['missing_facts'] == 0, ('missing_facts', result.get('missing_facts'))
    assert result['refuse_questions'] == 6, ('refuse_questions', result.get('refuse_questions'))
    assert result['refuse_with_gold_docs'] == 0, ('refuse_with_gold_docs', result.get('refuse_with_gold_docs'))
    assert result['answerable_without_facts'] == 0, ('answerable_without_facts', result.get('answerable_without_facts'))
    assert result['documents_covered_as_gold'] == 14, ('documents_covered_as_gold', result.get('documents_covered_as_gold'))
    assert result['all_answerable_have_gold'] == True, ('all_answerable_have_gold', result.get('all_answerable_have_gold'))
    print("smoke ok: Lesson 19 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
