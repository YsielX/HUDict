import pickle
import re
from dataclasses import dataclass

from hudict.paths import paths

WORD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9'’-]*$")


@dataclass(frozen=True)
class Entry:
    word: str
    phonetic: str
    glosses: list[str]


class Dictionary:
    def __init__(self, dictionary_path=None):
        self.dictionary_path = dictionary_path or paths.dictionary_path
        self.entries = {}
        self.lookup_map = {}
        self.load()

    def load(self):
        with open(self.dictionary_path, "rb") as f:
            data = pickle.load(f)
        self.entries = data["entries"]
        self.lookup_map = data["lookup_map"]

    def lookup(self, text):
        if not text:
            return []
        match = WORD_RE.match(text.strip())
        if not match:
            return []
        key = match.group(0).replace("’", "'").lower()
        ids = self.lookup_map.get(key, [])
        exact_ids = [entry_id for entry_id in ids if self.entries[entry_id]["word"].lower() == key]
        if exact_ids:
            ids = exact_ids
        results = []
        for entry_id in ids[:10]:
            raw = self.entries[entry_id]
            results.append(Entry(raw["word"], raw.get("phonetic", ""), raw.get("glosses", [])))
        return results
