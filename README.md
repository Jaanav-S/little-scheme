# tiny-lisp

A small Scheme-flavoured Lisp interpreter in one Python file.

## Features

- Integers, floats, strings, booleans (`#t`, `#f`) and symbols
- `define`, `lambda`, `if`, `cond`, `let`, `begin`, `set!`, `quote` / `'x`
- Lexical closures
- Proper tail calls, so deep recursion in tail position doesn't blow the stack
- Lists: `cons`, `car`, `cdr`, `list`, `null?`, `length`, `map`, `filter`
- A REPL with multi-line input
