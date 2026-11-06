"""Smoke test for Lesson 12: Metadata filtering and permissions: never retrieve what you may not show.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "filtering.py")
    spec = importlib.util.spec_from_file_location("lesson_12_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['public_questions'] == 30, ('public_questions', result.get('public_questions'))
    assert result['leaks_unfiltered'] == 6, ('leaks_unfiltered', result.get('leaks_unfiltered'))
    assert result['leaks_filtered'] == 0, ('leaks_filtered', result.get('leaks_filtered'))
    assert result['q19_manager_fact_recall'] == 1.0, ('q19_manager_fact_recall', result.get('q19_manager_fact_recall'))
    assert result['q19_public_fact_recall'] == 0.0, ('q19_public_fact_recall', result.get('q19_public_fact_recall'))
    assert result['q32_manager_fact_recall'] == 1.0, ('q32_manager_fact_recall', result.get('q32_manager_fact_recall'))
    assert result['q32_public_fact_recall'] == 0.0, ('q32_public_fact_recall', result.get('q32_public_fact_recall'))
    print("smoke ok: Lesson 12 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
