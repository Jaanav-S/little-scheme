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


def read(tokens):
    """Read one expression from the front of a token list (consuming it)."""
    if not tokens:
        raise LispError("unexpected end of input")
    token = tokens.pop(0)
    if token == "(":
        expr = []
        while tokens and tokens[0] != ")":
            expr.append(read(tokens))
        if not tokens:
            raise LispError("missing )")
        tokens.pop(0)
        return expr
    if token == ")":
        raise LispError("unexpected )")
    if token == "'":
        return [Symbol("quote"), read(tokens)]
    return atom(token)
