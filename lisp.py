"""A small Scheme-like Lisp interpreter."""

import math
import operator
import re
import sys


class Symbol(str):
    pass


class LispError(Exception):
    pass
