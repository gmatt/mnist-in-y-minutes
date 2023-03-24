import doctest
import types
from textwrap import dedent

import pytest

from convert_py_to_doctest import convert_py_to_doctest

kwargs = {
    "header": "",
    "footer": "",
}


def run_doctest_from_string(py_source: str) -> None:
    module = types.ModuleType("module")
    exec(py_source, module.__dict__)
    doctest.testmod(module, raise_on_error=True)


def test_full():
    py = dedent(
        """\
        1 + 2
        # <<< 3
        """
    )
    expected = dedent(
        '''\
        r"""
        >>> 1 + 2  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        3
        """

        if __name__ == "__main__":
            import doctest
            doctest.testmod()
        '''
    )

    assert convert_py_to_doctest(py) == expected


def test_simple():
    assert convert_py_to_doctest("1 + 2", **kwargs) == ">>> 1 + 2"


def test_empty_line():
    assert convert_py_to_doctest("", **kwargs) == ""


def test_assert():
    py = dedent(
        """\
        1 + 2
        # <<< 3
        """
    )
    expected = dedent(
        """\
        >>> 1 + 2  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        3"""
    )

    assert convert_py_to_doctest(py, **kwargs) == expected


def test_multiline_statement():
    py = dedent(
        """\
        (
            1 +
            2
        )
        # <<< 3
        """
    )
    expected = dedent(
        """\
        >>> (
        ...     1 +
        ...     2
        ... )  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        3"""
    )

    assert convert_py_to_doctest(py, **kwargs) == expected


def test_assert_works_passing():
    run_doctest_from_string(
        convert_py_to_doctest(
            dedent(
                """\
                1 + 2
                # <<< 3
                """
            ),
        )
    )


def test_assert_works_failing():
    with pytest.raises(doctest.DocTestFailure):
        run_doctest_from_string(
            convert_py_to_doctest(
                dedent(
                    """\
                    1 + 2
                    # <<< 42
                    """
                ),
            )
        )


def test_function_works():
    run_doctest_from_string(
        convert_py_to_doctest(
            dedent(
                """\
                def fun():
                    pass
                """
            )
        )
    )


@pytest.mark.skip(reason="not implemented")
def test_decorator_works():
    run_doctest_from_string(
        convert_py_to_doctest(
            dedent(
                """\
                dec = lambda x: x

                @dec
                def fun():
                    pass
                """
            )
        )
    )


@pytest.mark.skip(reason="not implemented")
def test_decorator():
    py = dedent(
        """\
        dec = lambda x: x

        @dec
        def fun():
            pass
        """
    )
    expected = dedent(
        """\
        >>> dec = lambda x: x

        >>> @dec
        ... def fun():
        ...     pass"""
    )

    assert convert_py_to_doctest(py, **kwargs) == expected
