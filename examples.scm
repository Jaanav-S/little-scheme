; Example programs for tiny-lisp. Run with: python lisp.py examples.scm

(define (fact n)
  (if (< n 2) 1 (* n (fact (- n 1)))))
