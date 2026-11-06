"""Smoke test for Lesson 23: Multi-hop retrieval: questions that need two documents.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "multi_hop.py")
    spec = importlib.util.spec_from_file_location("lesson_23_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['doc_recall_single'] == 0.9, ('doc_recall_single', result.get('doc_recall_single'))
    assert result['doc_recall_union'] == 1.0, ('doc_recall_union', result.get('doc_recall_union'))
    assert result['coverage_single'] == 0.5, ('coverage_single', result.get('coverage_single'))
    assert result['coverage_union'] == 0.3, ('coverage_union', result.get('coverage_union'))
    print("smoke ok: Lesson 23 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
