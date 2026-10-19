# tiny-lisp

A small Scheme-flavoured Lisp interpreter in one Python file.

## Features

- Integers, floats, strings, booleans (`#t`, `#f`) and symbols
- `define`, `lambda`, `if`, `cond`, `let`, `begin`, `set!`, `quote` / `'x`
- Lexical closures
- Proper tail calls, so deep recursion in tail position doesn't blow the stack
- Lists: `cons`, `car`, `cdr`, `list`, `null?`, `length`, `map`, `filter`
- A REPL with multi-line input

## Usage

```
python lisp.py              # start the REPL
python lisp.py examples.scm # run a file
```

```scheme
> (define (fact n) (if (< n 2) 1 (* n (fact (- n 1)))))
> (fact 20)
2432902008176640000
```

## How it works

1. **Tokenize**: split the source into parentheses, quotes, strings and atoms.
2. **Read**: turn tokens into nested Python lists (the program is data).
3. **Evaluate**: walk the lists. Special forms like `if` and `lambda` are
   handled in `evaluate`; everything else is a function call.

Tail calls are implemented by looping inside `evaluate` instead of recursing
when the last expression of a body or branch is evaluated.

## Tests

```
python -m pytest
```
