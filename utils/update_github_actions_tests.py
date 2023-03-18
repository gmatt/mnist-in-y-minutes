from constants import PROJECT_ROOT
from copy_content_to_jekyll import slugify


def update_github_actions_tests():
    input_dir = PROJECT_ROOT / "content"
    output_dir = PROJECT_ROOT / ".github" / "workflows"

    for python_file in input_dir.glob("*.py"):
        result = f"""name: "doctest-{slugify(python_file.stem)}"

env:
  FILE: "content/{python_file.name}"

on:
  push:
    paths:
      - "content/{python_file.name}"
  workflow_dispatch:

jobs:
  test:

    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version:
          - "3.7"
          - "3.8"
          - "3.9"
          - "3.10"

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Convert .py file to doctest
        run: |
          mkdir temp
          python utils/convert_py_to_doctest.py "$FILE" temp/test_doctest.py
      - name: Set up Python ${{{{ matrix.python-version }}}}
        uses: actions/setup-python@v4
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
      - name: Test with pytest
        run: |
          SHELL_COMMAND_MARKER="$(python -c "from utils import config; print(config.SHELL_COMMAND_MARKER)")"

          while read -r line; do
            echo "$line"
            eval "$line"
          done < <(grep "$SHELL_COMMAND_MARKER" "$FILE" | sed "s/$SHELL_COMMAND_MARKER//")

          cat temp/test_doctest.py

          pytest temp --doctest-modules --doctest-continue-on-failure --color=yes
"""

        output_file = output_dir / f"doctest-{slugify(python_file.stem)}.yml"
        output_file.write_text(result)
        print(f"Written to '{output_file}'.")


if __name__ == "__main__":
    update_github_actions_tests()
