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


def parse_all(source):
    tokens = tokenize(source)
    exprs = []
    while tokens:
        exprs.append(read(tokens))
    return exprs


class Env(dict):
    """A scope: a dict of bindings plus a link to the enclosing scope."""

    def __init__(self, names=(), values=(), outer=None):
        super().__init__(zip(names, values))
        self.outer = outer

    def find(self, name):
        env = self
        while env is not None:
            if name in env:
                return env
            env = env.outer
        raise LispError(f"undefined symbol: {name}")


class Procedure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return evaluate(self.body, self.bind(args))

    def bind(self, args):
        if len(args) != len(self.params):
            raise LispError(f"expected {len(self.params)} argument(s), got {len(args)}")
        return Env(self.params, args, self.env)


def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        "+": lambda *a: sum(a), "-": lambda a, *b: a - sum(b) if b else -a,
        "*": lambda *a: math.prod(a), "/": operator.truediv, "quotient": operator.floordiv,
        "remainder": operator.mod, "<": operator.lt, ">": operator.gt, "<=": operator.le,
        ">=": operator.ge, "=": operator.eq, "eq?": operator.is_, "equal?": operator.eq,
        "not": operator.not_, "abs": abs, "min": min, "max": max,
        "cons": lambda x, y: [x] + list(y), "car": lambda x: x[0], "cdr": lambda x: x[1:],
        "list": lambda *x: list(x), "null?": lambda x: x == [], "length": len,
        "list?": lambda x: isinstance(x, list), "number?": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "symbol?": lambda x: isinstance(x, Symbol), "procedure?": callable,
        "map": lambda f, xs: [f(x) for x in xs], "filter": lambda f, xs: [x for x in xs if f(x)],
        "apply": lambda f, args: f(*args), "display": display, "newline": lambda: print(),
    })
    return env
