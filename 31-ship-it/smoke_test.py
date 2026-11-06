"""Smoke test for Lesson 31: Ship it: your documents, your system.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "ship_check.py")
    spec = importlib.util.spec_from_file_location("lesson_31_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['demo_questions'] == 5, ('demo_questions', result.get('demo_questions'))
    assert result['answered'] == 4, ('answered', result.get('answered'))
    assert result['refused'] == 1, ('refused', result.get('refused'))
    assert result['citations_checked'] == 3, ('citations_checked', result.get('citations_checked'))
    assert result['citations_verified'] == 3, ('citations_verified', result.get('citations_verified'))
    assert result['known_miss_in_demo'] == True, ('known_miss_in_demo', result.get('known_miss_in_demo'))
    print("smoke ok: Lesson 31 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
