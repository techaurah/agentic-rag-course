"""Smoke test for Lesson 29: Build the capstone system.

Imports the lesson artifact, calls its evaluate(), and checks the
values the lesson text quotes. Offline, standard library only.
Run: python3 smoke_test.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    path = os.path.join(HERE, "capstone_system.py")
    spec = importlib.util.spec_from_file_location("lesson_29_artifact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    result = load().evaluate()
    assert result['all_checks_pass'] == True, ('all_checks_pass', result.get('all_checks_pass'))
    assert result['config_top_k'] == 5, ('config_top_k', result.get('config_top_k'))
    assert result['chunks'] == 84, ('chunks', result.get('chunks'))
    assert result['delivery_answered'] == True, ('delivery_answered', result.get('delivery_answered'))
    assert result['shrub_answered'] == True, ('shrub_answered', result.get('shrub_answered'))
    assert result['wifi_refused'] == True, ('wifi_refused', result.get('wifi_refused'))
    assert result['margin_manager_answered'] == True, ('margin_manager_answered', result.get('margin_manager_answered'))
    assert result['margin_public_refused'] == True, ('margin_public_refused', result.get('margin_public_refused'))
    print("smoke ok: Lesson 29 evaluate() matches the lesson text")


if __name__ == "__main__":
    main()
