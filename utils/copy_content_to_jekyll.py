import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import config
from constants import PROJECT_ROOT


# From:
# https://github.com/django/django/blob/4b1bfea2846f66f504265cec46ee1fe94ee9c98b/django/utils/text.py#L420
def slugify(value: str) -> str:
    value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def check_if_filenames_cause_duplicates():
    input_dir = PROJECT_ROOT / "content"

    counter = defaultdict(list)
    for python_file in input_dir.glob("*.py"):
        stem = python_file.stem
        slug = slugify(stem)
        counter[slug].append(python_file.name)
        assert len(counter[slug]) < 2, (
            f"Duplicate names found, {counter[slug]} all map to '{slug}'. Please "
            f"change a filename."
        )


def copy_content_to_jekyll():
    input_dir = PROJECT_ROOT / "content"
    output_dir = PROJECT_ROOT / config.JEKYLL_ROOT / "libraries"

    check_if_filenames_cause_duplicates()

    output_dir.mkdir(exist_ok=True)
    for markdown_file in output_dir.glob("*.markdown"):
        markdown_file.unlink()
    print(f"Cleared '{output_dir}'.")

    for python_file in input_dir.glob("*.py"):
        python_content = python_file.read_text()
        result = f"""---
title: {python_file.stem}
layout: library
---

```python
{python_content}
```
"""
        output_file = output_dir / f"{slugify(python_file.stem)}.markdown"
        output_file.write_text(result)
        print(f"Written to '{output_file}'.")

    input_file = Path(config.__file__)
    output_file = PROJECT_ROOT / config.JEKYLL_ROOT / "assets" / "config.js"
    output_file.write_text(input_file.read_text())
    print(f"Written to '{output_file}'.")


if __name__ == "__main__":
    copy_content_to_jekyll()
