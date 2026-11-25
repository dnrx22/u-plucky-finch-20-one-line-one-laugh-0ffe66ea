"""One Line, One Laugh — make.fun entry.

Writes a single original funny line to ``entry.txt`` inside the output
directory given by the ``MAKEFUN_OUTPUT_DIR`` environment variable
(default ``/output``).

The program is deterministic: every run writes exactly the same bytes.
Only the Python standard library is used and no network access happens.
"""

import os

# The entry: one original funny line, written by the author of this repo.
LINE = (
    "I asked my AI assistant for dating advice, and it told me to try "
    "turning myself off and on again."
)

MAX_CHARS = 200
TERMINATORS = (".", "!", "?")


def validate(line: str) -> None:
    """Enforce the competition rules for the funny line.

    Raises ``ValueError`` if the line breaks any rule:
    - exactly one line (no embedded newlines)
    - non-empty, with no leading or trailing whitespace
    - at most 200 Unicode code points
    - ends with a sentence-terminating mark (``.``, ``!`` or ``?``)
    - every character printable (no control characters)
    """
    if not line:
        raise ValueError("line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if not line.isprintable():
        raise ValueError("line must contain only printable characters")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line.endswith(TERMINATORS):
        raise ValueError("line must end with '.', '!' or '?'")


def main() -> None:
    validate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Round-trip check: the file on disk must contain exactly the
    # validated line and nothing else.
    with open(path, "rb") as f:
        stored = f.read().decode("utf-8")
    if stored != LINE + "\n":
        raise RuntimeError("round-trip check failed: entry.txt mismatch")
    validate(stored.rstrip("\n"))

    print(f"wrote {len(data)} bytes to {path}")
    print(f"line character count: {len(LINE)}")


if __name__ == "__main__":
    main()
