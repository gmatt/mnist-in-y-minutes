import argparse
import ast
import sys
from pathlib import Path

import config


def convert_py_to_doctest(
    py_source_code: str,
    *,
    header: str = 'r"""\n',
    footer: str = '''
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
''',
) -> str:
    assert sys.version_info >= (3, 8), (
        "This script only works with Python 3.8 or newer since it uses"
        "ast.AST.end_lineno."
    )

    tree = ast.parse(py_source_code)
    lines = py_source_code.splitlines()
    lineno_to_node: dict[int, ast.stmt] = {node.lineno - 1: node for node in tree.body}

    result = []
    if config.DOCTEST_ELLIPSIS_MARKER != "...":
        result.append(">>> import doctest")
        result.append(
            f">>> doctest.ELLIPSIS_MARKER = {config.DOCTEST_ELLIPSIS_MARKER!r}"
        )
    i = 0
    while i < len(lines):
        if lines[i].startswith(config.OUTPUT_MARKER):
            if result[-1][:4] in {">>> ", "... "}:
                result[-1] += "  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE"
            result.append(lines[i][6:])
        elif lines[i] == "":
            result.append("")
        else:
            result.append(">>> " + lines[i])
            if i in lineno_to_node:
                for j in range(i + 1, lineno_to_node[i].end_lineno):
                    result.append("... " + lines[j])
                    i += 1
        i += 1

    result = "\n".join(result)
    return header + result + footer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="A python file.")
    parser.add_argument("target", help="Where to save the file with the doctest.")
    args = parser.parse_args()

    Path(args.target).write_text(convert_py_to_doctest(Path(args.source).read_text()))
    print(f"Written output to '{args.target}'.")
