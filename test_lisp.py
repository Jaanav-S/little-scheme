import pytest

from lisp import LispError, Symbol, parse_all, run, to_string, tokenize


def test_tokenize_skips_comments():
    assert tokenize("(+ 1 2) ; add") == ["(", "+", "1", "2", ")"]
