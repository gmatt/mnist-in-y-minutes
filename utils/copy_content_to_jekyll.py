import config
from constants import PROJECT_ROOT


def copy_content_to_jekyll():
    input_dir = PROJECT_ROOT / "content"
    output_dir = PROJECT_ROOT / config.JEKYLL_ROOT / "libraries"

    output_dir.mkdir(exist_ok=True)

    for python_file in input_dir.glob("*.py"):
        python_content = python_file.read_text()
        result = f"""---
title: {python_file.stem}
layout: page
---

```python
{python_content}
```
"""
        (output_dir / f"{python_file.stem}.markdown").write_text(result)


if __name__ == "__main__":
    copy_content_to_jekyll()
