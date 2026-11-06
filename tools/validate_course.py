#!/usr/bin/env python3
"""Validate every JSON file in this repo.

Checks:
- Any .json file must parse as JSON.
- Golden set and gap set entries (recognised as a list of
  dicts carrying "question" and "gold_docs" keys) must each
  carry an id, a type, a role, and a facts list; entries with
  gold documents must carry at least one fact, and entries
  with no gold documents must be marked expect: refuse.
- The capstone config (recognised by a "capstone_system" key)
  must carry the four sections Lesson 28 fixes in advance:
  retrieval, generation, evaluation, and gates.
Exits nonzero on any failure, so CI can gate on it.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_SECTIONS = ["retrieval", "generation", "evaluation", "gates"]


def iter_json():
    for dirpath, _dirs, files in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in sorted(files):
            if name.endswith(".json"):
                yield os.path.join(dirpath, name)


def check(data):
    errors = []
    if isinstance(data, list) and data and isinstance(data[0], dict) \
            and "question" in data[0] and "gold_docs" in data[0]:
        for entry in data:
            label = entry.get("id", "<no id>")
            for field in ["id", "type", "role", "question", "gold_docs", "facts"]:
                if field not in entry:
                    errors.append(f"{label}: missing field {field}")
            if entry.get("gold_docs") and not entry.get("facts"):
                errors.append(f"{label}: answerable but carries no facts")
            if not entry.get("gold_docs") and entry.get("expect") != "refuse":
                errors.append(f"{label}: no gold documents but not marked expect: refuse")
    if isinstance(data, dict) and "capstone_system" in data:
        system = data["capstone_system"]
        for section in CONFIG_SECTIONS:
            if section not in system:
                errors.append(f"capstone_system missing section: {section}")
    return errors


def main():
    total, bad = 0, 0
    for path in iter_json():
        total += 1
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            bad += 1
            print(f"FAIL {rel}: does not parse: {exc}")
            continue
        errors = check(data)
        if errors:
            bad += 1
            for e in errors:
                print(f"FAIL {rel}: {e}")
        else:
            print(f"OK   {rel}")
    print(f"\n{total} JSON files checked, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
