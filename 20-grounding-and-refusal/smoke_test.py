"""Smoke test for Lesson 20: Grounding and refusal: answers that know their limits.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "grounded_answers.py")
    spec = importlib.util.spec_from_file_location("lesson_20_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['refused_correctly'] == 5, ('refused_correctly', result.get('refused_correctly'))
    assert result['refuse_total'] == 6, ('refuse_total', result.get('refuse_total'))
    assert result['false_answers'] == ['q24'], ('false_answers', result.get('false_answers'))
    assert result['false_refusals'] == 0, ('false_refusals', result.get('false_refusals'))
    assert result['answered'] == 26, ('answered', result.get('answered'))
    assert result['citation_coverage'] == 26, ('citation_coverage', result.get('citation_coverage'))
    assert result['grounded_sentences'] == 26, ('grounded_sentences', result.get('grounded_sentences'))
    assert result['full_fact_answers'] == 21, ('full_fact_answers', result.get('full_fact_answers'))
    assert result['strict_refused_correctly'] == 6, ('strict_refused_correctly', result.get('strict_refused_correctly'))
    assert result['strict_false_refusals'] == 9, ('strict_false_refusals', result.get('strict_false_refusals'))
    assert result['lax_refused_correctly'] == 4, ('lax_refused_correctly', result.get('lax_refused_correctly'))
    print("smoke ok: Lesson 20 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
