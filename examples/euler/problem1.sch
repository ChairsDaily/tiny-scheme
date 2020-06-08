
;; Project Euler #1
;; multiples of 3 and 5 below 1000
;; @author kaleb horvath
;; @license gplv3

(begin
    (define enumer-aux (lambda (n m l)
        (cond ((or (eq? m 0) (eq? n 0)) nil)
              ((eq? (length l) n) l)
              (enumer-aux n (- m 1) (cons m l)))))

    ;; enumerate a range into a list for processing
    ;; @param n the upperbound for range
    ;; @return list containing all i such that 0 < i < (n - 1)
    (define enumer (lambda (n)
        (filter (lambda (x) (not (eq? x n))) (enumer-aux n n nil))))

    (define final-solution
        (sum (filter (lambda (x) 
            (or (eq? (mod x 3) 0) (eq? (mod x 5) 0))) (enumer 200))))

   final-solution
)