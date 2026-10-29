"""Parse crontab lines and describe each schedule in plain English.

Usage: python3 main.py crontab.txt
Environment lines (VAR=value) and comments are skipped.
"""
import argparse
import sys

RANGES = {"minute": (0, 59), "hour": (0, 23), "day_of_month": (1, 31),
          "month": (1, 12), "day_of_week": (0, 7)}
NAMES = ["minute", "hour", "day_of_month", "month", "day_of_week"]


def describe_field(field, name):
    lo, hi = RANGES[name]
    if field == "*":
        return f"every {name.replace('_', ' ')}"
    if field.startswith("*/"):
        return f"every {field[2:]} {name.replace('_', ' ')}s"
    if "," in field:
        return f"{name.replace('_', ' ')}s {field}"
    if "-" in field:
        return f"{name.replace('_', ' ')}s {field}"
    return f"{name.replace('_', ' ')} {field}"


def parse_line(line):
    """Return a dict for a schedule line, or None for non-schedule lines."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" in stripped.split()[0]:
        return None
    parts = stripped.split(None, 5)
    if len(parts) < 6:
        raise ValueError(f"Invalid crontab line: {line!r}")
    fields = parts[:5]
    for field, name in zip(fields, NAMES):
        lo, hi = RANGES[name]
        for piece in field.replace("*/", "").replace(",", " ").replace("-", " ").split():
            if piece == "*":
                continue
            value = int(piece)
            if not (lo <= value <= hi or (name == "day_of_week" and value == 7)):
                raise ValueError(f"{name} value {value} out of range in {line!r}")
    description = "; ".join(describe_field(f, n) for f, n in zip(fields, NAMES))
    return {"schedule": " ".join(fields), "command": parts[5],
            "description": description}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to a crontab-style file")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        for line in f:
            try:
                parsed = parse_line(line)
            except ValueError as exc:
                print(f"ERROR: {exc}")
                continue
            if parsed:
                print(f"{parsed['schedule']} -> {parsed['description']} :: {parsed['command']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
