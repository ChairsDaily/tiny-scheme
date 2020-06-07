(begin
    (define _abs (lambda (x)
        (cond ((> x 0) x)
              ((= x 0) 0)
              ((< x 0) (* -1 x)) #f)))

    (define square (lambda (x) (* x x)))
    (define sum-of-squares (lambda (x y)
        (+ (square x) (square y))))

    (_abs 19)
)

