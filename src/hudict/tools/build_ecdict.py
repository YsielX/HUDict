import argparse
import csv
import os
import pickle
import re
from collections import defaultdict

from hudict.paths import paths

WORD_RE = re.compile(r"^[a-z][a-z0-9'’-]*(?:[ -][a-z0-9'’-]+)*$")


def clean_word(value):
    value = (value or "").strip().replace("’", "'").lower()
    if not value or not WORD_RE.match(value):
        return None
    return value


def split_translation(value):
    lines = []
    for line in (value or "").replace("\\n", "\n").splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return lines[:6]


def parse_exchange(value):
    forms = set()
    for part in (value or "").split("/"):
        if ":" not in part:
            continue
        _, raw_forms = part.split(":", 1)
        for raw_form in re.split(r"[,;]", raw_forms):
            form = clean_word(raw_form)
            if form:
                forms.add(form)
    return forms


def build(csv_path):
    entries = {}
    lookup_map = defaultdict(list)
    skipped = 0

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for entry_id, row in enumerate(reader, start=1):
            word = clean_word(row.get("word"))
            glosses = split_translation(row.get("translation"))
            if not word or not glosses:
                skipped += 1
                continue
            entries[entry_id] = {
                "word": word,
                "phonetic": (row.get("phonetic") or "").strip(),
                "glosses": glosses,
            }
            surfaces = {word}
            surfaces.update(parse_exchange(row.get("exchange")))
            for surface in surfaces:
                lookup_map[surface].append(entry_id)

    return {"entries": entries, "lookup_map": dict(lookup_map)}, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build HUDict dictionary from ECDICT csv.")
    parser.add_argument("csv_path")
    parser.add_argument("-o", "--output", default=paths.dictionary_path)
    args = parser.parse_args(argv)

    payload, skipped = build(args.csv_path)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
    refs = sum(len(v) for v in payload["lookup_map"].values())
    size_mb = os.path.getsize(args.output) / 1_048_576
    print(f"Saved {args.output}")
    print(f"Entries: {len(payload['entries'])}; lookup refs: {refs}; skipped rows: {skipped}; size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
