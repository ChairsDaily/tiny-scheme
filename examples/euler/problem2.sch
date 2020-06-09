(begin
    (define nth-fibonacii-number (lambda (n)
        (if (or (eq? n 0) (eq? n 1)) 1
            (+ (nth-fibonacii-number (- n 1)) 
            (nth-fibonacii-number (- n 2))))))

    (define step (lambda (result x y limit)
        (if (<= limit 0) result
            (if (eq? (mod (+ x y) 2) 0) 
                (step (+ result (+ x y)) y (+ x y) (- limit 1))
            (step result y (+ x y) limit)))))

    (step 0 1 1 4)
)