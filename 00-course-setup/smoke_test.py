"""Smoke test for Lesson 00: Course setup: what you need, and how this course works.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "check_environment.py")
    spec = importlib.util.spec_from_file_location("lesson_00_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['python_ok'] == True, ('python_ok', result.get('python_ok'))
    assert result['documents'] == 24, ('documents', result.get('documents'))
    assert result['golden_questions'] == 32, ('golden_questions', result.get('golden_questions'))
    assert result['answerable'] == 26, ('answerable', result.get('answerable'))
    assert result['refuse_expected'] == 6, ('refuse_expected', result.get('refuse_expected'))
    assert result['roles'] == ['manager', 'public', 'staff'], ('roles', result.get('roles'))
    print("smoke ok: Lesson 00 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
