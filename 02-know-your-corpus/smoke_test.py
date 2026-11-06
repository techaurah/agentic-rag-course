"""Smoke test for Lesson 02: Know your corpus: documents, metadata, and the manifest.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "corpus_audit.py")
    spec = importlib.util.spec_from_file_location("lesson_02_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['documents'] == 24, ('documents', result.get('documents'))
    assert result['public_documents'] == 21, ('public_documents', result.get('public_documents'))
    assert result['superseded_pairs'] == 2, ('superseded_pairs', result.get('superseded_pairs'))
    assert result['all_have_updated'] == True, ('all_have_updated', result.get('all_have_updated'))
    assert result['all_have_roles'] == True, ('all_have_roles', result.get('all_have_roles'))
    print("smoke ok: Lesson 02 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
