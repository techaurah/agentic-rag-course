"""Smoke test for Lesson 24: Self-correction: grade, rewrite, retry.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "self_correction.py")
    spec = importlib.util.spec_from_file_location("lesson_24_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['failing_at_3'] == ['q11'], ('failing_at_3', result.get('failing_at_3'))
    assert result['recovered_at_10'] == {'q11': 1.0}, ('recovered_at_10', result.get('recovered_at_10'))
    assert result['all_recovered'] == True, ('all_recovered', result.get('all_recovered'))
    assert result['surface_grader_false_passes'] == 1, ('surface_grader_false_passes', result.get('surface_grader_false_passes'))
    assert result['retry_rate'] == 0.0385, ('retry_rate', result.get('retry_rate'))
    print("smoke ok: Lesson 24 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
