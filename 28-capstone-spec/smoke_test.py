"""Smoke test for Lesson 28: Capstone spec: the evaluated Fernhill assistant.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "capstone_spec.py")
    spec = importlib.util.spec_from_file_location("lesson_28_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['spec_valid'] == True, ('spec_valid', result.get('spec_valid'))
    assert result['gate_count'] == 8, ('gate_count', result.get('gate_count'))
    assert result['chunk_target_words'] == 90, ('chunk_target_words', result.get('chunk_target_words'))
    assert result['top_k'] == 5, ('top_k', result.get('top_k'))
    assert result['composer'] == 'extractive-single-sentence', ('composer', result.get('composer'))
    assert result['unseen_min'] == 2, ('unseen_min', result.get('unseen_min'))
    print("smoke ok: Lesson 28 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
