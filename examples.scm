; Example programs for tiny-lisp. Run with: python lisp.py examples.scm

(define (fact n)
  (if (< n 2) 1 (* n (fact (- n 1)))))

(display "20! = ") (display (fact 20)) (newline)

(define (fib-iter n a b)
  (if (= n 0) a (fib-iter (- n 1) b (+ a b))))

(display "fib(50) = ") (display (fib-iter 50 0 1)) (newline)

(define (range a b)
  (if (>= a b) '() (cons a (range (+ a 1) b))))
