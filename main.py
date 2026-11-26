#!/usr/bin/env python3
"""Your AI Therapist's Diagnosis — make.fun entry.

Writes one original funny line to /output/entry.txt.

The entry is fully offline and deterministic: Python 3.13 stdlib only,
no network, no randomness, no secrets, no environment input.

How the line was picked: it won a 10-candidate local tournament, judged
pairwise by the Caffeine Inference router with the house judge brief
verbatim (40 calls, round-robin, each candidate played 4 games, each game
judged in both label orders). Every verdict is recorded in tournament.jsonl.

Revision: this file was rewritten by hand (see the Revision section in
README.md) so the build transcript accounts for every line of code here.
The entry line itself is unchanged. The single validate() from round 1
is now four small checks (_require_string, _require_length,
_require_single_line, _require_printable) composed by encode_entry(),
and the write/verify steps live in their own helpers, write_entry()
and verify_written(), so each gate check is visible on its own.
"""

import os
import sys

# Tournament winner: 3/4 games, 2.85 points of 4. 121 characters.
LINE = 'Diagnosis: inbox zero obsession, stage four. You archive emails you have not read to feel the brief peace of a clean lie.'

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def _require_string(line):
    """Reject anything that is not a plain string."""
    if not isinstance(line, str):
        raise ValueError("entry line must be a string")


def _require_length(line):
    """Enforce the bounty gate's 1..MAX_CHARS character limit."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, gate requires 1-{MAX_CHARS}")
    if not line.strip():
        raise ValueError("line must not be only whitespace")


def _require_single_line(line):
    """The entry must be exactly one line with no surrounding whitespace."""
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")


def _require_printable(line):
    """Reject control characters; the gate requires plain UTF-8 text."""
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")


def encode_entry(line: str) -> bytes:
    """Validate the line against the bounty gate; return its UTF-8 bytes."""
    _require_string(line)
    _require_length(line)
    _require_single_line(line)
    _require_printable(line)
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("line is not valid UTF-8 round-trip text")
    return data


def write_entry(path: str, data: bytes) -> None:
    """Write exactly the entry bytes to path, no trailing newline."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def verify_written(path: str, data: bytes) -> None:
    """Read the file back and compare it byte for byte with the entry."""
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError(
            f"verification failed: {path} differs from the entry line"
        )


def main() -> int:
    data = encode_entry(LINE)
    write_entry(OUTPUT_PATH, data)
    verify_written(OUTPUT_PATH, data)
    print(f"Wrote {len(LINE)} chars ({len(data)} bytes) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
