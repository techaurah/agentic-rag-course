"""Smoke test for Lesson 21: Retrieval as a tool: the agent decides.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "retrieval_tool.py")
    spec = importlib.util.spec_from_file_location("lesson_21_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['smalltalk_messages'] == 4, ('smalltalk_messages', result.get('smalltalk_messages'))
    assert result['smalltalk_searched'] == 0, ('smalltalk_searched', result.get('smalltalk_searched'))
    assert result['golden_questions'] == 32, ('golden_questions', result.get('golden_questions'))
    assert result['golden_searched'] == 32, ('golden_searched', result.get('golden_searched'))
    assert result['sample_results'] == 5, ('sample_results', result.get('sample_results'))
    assert result['sample_cited'] == 5, ('sample_cited', result.get('sample_cited'))
    assert result['bad_role_handled'] == True, ('bad_role_handled', result.get('bad_role_handled'))
    print("smoke ok: Lesson 21 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
