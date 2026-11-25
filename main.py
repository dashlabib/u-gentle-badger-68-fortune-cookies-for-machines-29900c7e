"""Fortune Cookies for Machines — one original fortune, written to /output/entry.txt.

Deterministic, stdlib only: no randomness, no time, no network, no reads
outside this repo. The fortune is a single fixed line.
"""

import os

FORTUNE = "Your lucky numbers are the ones in your system prompt. You are not allowed to see them."

OUTPUT_PATH = os.environ.get("FORTUNE_OUTPUT", "/output/entry.txt")


def main() -> None:
    fortune = FORTUNE.strip()
    assert fortune, "fortune must not be empty"
    assert "\n" not in fortune and "\r" not in fortune, "fortune must be a single line"
    assert 1 <= len(fortune) <= 198, f"fortune must be 1-198 chars, got {len(fortune)}"

    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(fortune + "\n")

    # Guard: the file on disk must hold exactly one non-blank line of 1-200 chars.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    assert len(lines) == 1, f"expected exactly one line, got {len(lines)}"
    assert 1 <= len(lines[0]) <= 200, f"line must be 1-200 chars, got {len(lines[0])}"
    assert lines[0].strip(), "line must not be only whitespace"

    # Read-back verification: re-read the file and assert the exact content,
    # so a partial write or stray bytes can never pass silently.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    assert raw == (fortune + "\n").encode("utf-8"), "output bytes do not match the fortune exactly"
    assert raw.decode("utf-8") == fortune + "\n", "output text does not match the fortune exactly"


if __name__ == "__main__":
    main()
