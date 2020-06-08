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

    ;;
    ;; Linearly recursive list reversal, makes use of tail call opt.
    ;; At runtime, this is ran within a while loop and the recursive
    ;; call is treated as a 'goto' of sorts, and symbols are rebinded.
    ;;
    (define reverse-aux (lambda (l a)
        (if (null? l) a
        (reverse-aux (cdr l) (cons (car l) a)))))
    (define reverse (lambda (l) (reverse-aux l nil)))

    ;; 
    ;; copy-list and member functions (note: member? is a primitive)
    ;;
    (define mem (lambda (e l)
        (if (null? l) #f 
            (if (eq? (car l) e) #t 
                (mem e (cdr l))))))
    (eq? (member? 1 (list 1 2 3)) (mem 1 (list 1 2 3)))
    ;;expect True

    (define copy-list (lambda (l)
        (if (null? l) nil 
        (cons (car l) (copy-list (cdr l))))))
)

