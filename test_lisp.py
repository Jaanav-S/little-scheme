import pytest

from lisp import LispError, Symbol, parse_all, run, to_string, tokenize


def test_tokenize_skips_comments():
    assert tokenize("(+ 1 2) ; add") == ["(", "+", "1", "2", ")"]


def test_parse_nested():
    assert parse_all("(a (b 1) \"s\")") == [[Symbol("a"), [Symbol("b"), 1], "s"]]


def test_arithmetic():
    assert run("(+ 1 2 (* 3 4))") == 15
    assert run("(- 10)") == -10


def test_define_and_call():
    assert run("(define (square x) (* x x)) (square 7)") == 49


def test_closures():
    src = """
    (define (make-counter)
      (let ((n 0))
        (lambda () (set! n (+ n 1)) n)))
    (define c (make-counter))
    (c) (c) (c)
    """
    assert run(src) == 3


def test_cond():
    src = "(define (sign x) (cond ((< x 0) -1) ((= x 0) 0) (else 1))) (list (sign -5) (sign 0) (sign 9))"
    assert run(src) == [-1, 0, 1]


def test_quote_and_lists():
    assert run("(car (cdr '(1 2 3)))") == 2
    assert run("(cons 0 (list 1 2))") == [0, 1, 2]


def test_map_and_filter():
    assert run("(map (lambda (x) (* x 2)) (filter (lambda (x) (> x 1)) '(1 2 3)))") == [4, 6]


def test_tail_calls_do_not_overflow():
    src = "(define (loop n acc) (if (= n 0) acc (loop (- n 1) (+ acc 1)))) (loop 100000 0)"
    assert run(src) == 100000


def test_undefined_symbol():
    with pytest.raises(LispError):
        run("(nope 1)")


def test_unbalanced_parens():
    with pytest.raises(LispError):
        run("(+ 1 2")


def test_to_string():
    assert to_string([1, True, "hi"]) == '(1 #t "hi")'
