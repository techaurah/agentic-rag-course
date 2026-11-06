"""Smoke test for Lesson 22: Routing and adaptive retrieval: the right effort per question.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "routing.py")
    spec = importlib.util.spec_from_file_location("lesson_22_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['avg_legs_routed'] == 1.6154, ('avg_legs_routed', result.get('avg_legs_routed'))
    assert result['avg_legs_always_hybrid'] == 2.0, ('avg_legs_always_hybrid', result.get('avg_legs_always_hybrid'))
    assert result['per_type_equal'] == True, ('per_type_equal', result.get('per_type_equal'))
    assert result['routed_per_type'] == {'freshness': 1.0, 'multihop': 0.9, 'paraphrase': 1.0, 'permission': 1.0, 'single': 1.0}, ('routed_per_type', result.get('routed_per_type'))
    print("smoke ok: Lesson 22 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
