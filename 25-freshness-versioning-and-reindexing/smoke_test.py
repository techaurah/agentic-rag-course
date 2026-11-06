"""Smoke test for Lesson 25: Freshness, versioning, and reindexing.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "freshness.py")
    spec = importlib.util.spec_from_file_location("lesson_25_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['stale_chunks_before'] == 10, ('stale_chunks_before', result.get('stale_chunks_before'))
    assert result['stale_chunks_after'] == 3, ('stale_chunks_after', result.get('stale_chunks_after'))
    assert result['chunks_changed_by_edit'] == ['delivery#1'], ('chunks_changed_by_edit', result.get('chunks_changed_by_edit'))
    assert result['chunks_total'] == 84, ('chunks_total', result.get('chunks_total'))
    print("smoke ok: Lesson 25 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
