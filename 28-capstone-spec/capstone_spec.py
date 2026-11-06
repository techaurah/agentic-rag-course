"""Lesson 28 artifact: capstone spec checker.

Loads capstone/system.json, validates its shape against the
spec, and prints the acceptance gates the build must pass.
Offline, standard library only. Run: python3 capstone_spec.py
"""

import json
import os

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capstone", "system.json")


def load_spec():
    with open(SPEC_PATH) as f:
        return json.load(f)["capstone_system"]


def evaluate():
    spec = load_spec()
    sections = sorted(spec.keys())
    gates = spec["gates"]
    return {
        "sections": sections,
        "chunk_target_words": spec["retrieval"]["chunk_target_words"],
        "top_k": spec["retrieval"]["top_k"],
        "composer": spec["generation"]["composer"],
        "unseen_min": spec["generation"]["unseen_min"],
        "gates": gates,
        "gate_count": len(gates),
        "spec_valid": sections == ["evaluation", "gates", "generation", "retrieval"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
