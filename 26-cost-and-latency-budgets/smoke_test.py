"""Smoke test for Lesson 26: Cost and latency budgets.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "budgets.py")
    spec = importlib.util.spec_from_file_location("lesson_26_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['latency_gate_ms'] == 50, ('latency_gate_ms', result.get('latency_gate_ms'))
    assert result['end_to_end_within_gate'] == True, ('end_to_end_within_gate', result.get('end_to_end_within_gate'))
    assert result['questions_timed'] == 26, ('questions_timed', result.get('questions_timed'))
    print("smoke ok: Lesson 26 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
