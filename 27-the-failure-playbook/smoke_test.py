"""Smoke test for Lesson 27: The failure playbook: classifying what breaks.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "failure_playbook.py")
    spec = importlib.util.spec_from_file_location("lesson_27_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['retrieval_partial'] == ['q11'], ('retrieval_partial', result.get('retrieval_partial'))
    assert result['composition_incomplete'] == ['q01', 'q05', 'q10', 'q29'], ('composition_incomplete', result.get('composition_incomplete'))
    assert result['false_answer'] == ['q24'], ('false_answer', result.get('false_answer'))
    assert result['false_refusal'] == [], ('false_refusal', result.get('false_refusal'))
    assert result['clean'] == 26, ('clean', result.get('clean'))
    assert result['total_questions'] == 32, ('total_questions', result.get('total_questions'))
    print("smoke ok: Lesson 27 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
