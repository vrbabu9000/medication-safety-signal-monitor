"""Print the field tree of a sample JSON file and how often each field is filled.

Usage:
    python3 -I prototypes/explore/describe_structure.py prototypes/data/oxycodone/faers_sample_reports.json
    python3 -I prototypes/explore/describe_structure.py <file.json> --records results   # path to the record list

Read-only. Paths use dots; [] means "inside a list".
"""
import json
import sys
from collections import Counter


def walk(node, path, seen, types):
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            if v not in (None, "", [], {}):
                seen[p] += 1
            types[p].add(type(v).__name__)
            walk(v, p, seen, types)
    elif isinstance(node, list):
        for item in node:
            walk(item, path + "[]", seen, types)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1]))
    key = sys.argv[sys.argv.index("--records") + 1] if "--records" in sys.argv else None
    if key is None:  # guess the record list
        key = next((k for k in ("results", "studies", "data") if isinstance(data.get(k), list)), None)
    records = data[key] if key else [data]
    seen, types = Counter(), {}
    from collections import defaultdict
    types = defaultdict(set)
    for r in records:
        rec_seen = Counter()
        walk(r, "", rec_seen, types)
        for p in rec_seen:  # count once per record
            seen[p] += 1
    n = len(records)
    print(f"{sys.argv[1]}  ({n} records, list key = {key!r})\n")
    print(f"{'filled':>7}  {'type':<10} field")
    for p in sorted(types):
        depth = p.count(".") + p.count("[]")
        if depth > 4:
            continue
        pct = 100 * seen[p] / n if n else 0
        print(f"{pct:6.0f}%  {'/'.join(sorted(types[p])):<10} {p}")


if __name__ == "__main__":
    main()
