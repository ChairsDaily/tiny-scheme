(begin 
    (define nth (lambda (n l)
        (if (null? l) nil
        (if (eq? n 0) (car l) (nth (- n 1) (cdr l))))))
    
    (define combine (lambda (proc)
        (lambda (x y)
            (if (null? x) (quote ())
                (proc (list (car x) (car y))
                    ((combine proc) (cdr x) (cdr y)))))))
    (define zip (combine cons))

    (define inter (lambda (l1 l2)
        (cond ((null? l1) nil) 
              ((member? (car l1) l2) 
                (cons (car l1) (inter (cdr l1) l2)))
              (inter (cdr l1) l2) )))

    ;; linear recursion, quite slow and will grow the stack 
    ;; arbitrarily if you do not use tail calls
    (define slow-reverse (lambda (l)
        (if (null? l) nil 
        (+ (slow-reverse (cdr l)) (cons (car l) nil)))))



    ;; much faster implementation using an accumulator
    ;; and a tail recursive procedure call
    ;; (with tail call, we do not have to wait for the child routines)
    (define fast-reverse (lambda (l a)
        (if (null? l) a
        (fast-reverse (cdr l) (cons (car l) a)))))

    (fast-reverse (list 1 2 3 4 5 6 7 8 9 1 2 4 5 6 7) nil)
)



