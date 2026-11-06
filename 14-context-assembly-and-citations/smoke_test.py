"""Smoke test for Lesson 14: Context assembly and citations: what the model actually sees.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "context_pack.py")
    spec = importlib.util.spec_from_file_location("lesson_14_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['budget_words'] == 400, ('budget_words', result.get('budget_words'))
    assert result['avg_pack_words'] == 161, ('avg_pack_words', result.get('avg_pack_words'))
    assert result['citation_ready_pct'] == 1.0, ('citation_ready_pct', result.get('citation_ready_pct'))
    assert result['packs_within_budget'] == 26, ('packs_within_budget', result.get('packs_within_budget'))
    assert result['labelled_items'] == 122, ('labelled_items', result.get('labelled_items'))
    print("smoke ok: Lesson 14 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
