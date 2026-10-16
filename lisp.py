"""A small Scheme-like Lisp interpreter."""

import math
import operator
import re
import sys


class Symbol(str):
    pass


class LispError(Exception):
    pass


TOKEN = re.compile(r"""\s*(?:(;[^\n]*)|([()'])|("(?:\\.|[^"\\])*")|([^\s()'";]+))""")


def tokenize(source):
    """Split source code into a list of tokens, dropping comments."""
    tokens, pos = [], 0
    source = source.rstrip()
    while pos < len(source):
        match = TOKEN.match(source, pos)
        if not match or match.end() == pos:
            raise LispError(f"unexpected character at {pos}: {source[pos]!r}")
        comment, paren, string, atom = match.groups()
        if not comment:
            tokens.append(paren or string or atom)
        pos = match.end()
    return tokens


def atom(token):
    if token.startswith('"'):
        return token[1:-1].encode().decode("unicode_escape")
    if token == "#t":
        return True
    if token == "#f":
        return False
    for kind in (int, float):
        try:
            return kind(token)
        except ValueError:
            pass
    return Symbol(token)
