[![Build Status](https://travis-ci.com/ChairsDaily/tiny-scheme.svg?branch=master)](https://travis-ci.com/ChairsDaily/tiny-scheme)
# tiny-scheme
Fast and minimal interpreted runtime for a dialect of Scheme. Aims to eliminate things that
I find inconvenient in most implementations. 
- dynamic type casting at runtime
- cache aware parser
- tail call optimizations for linear recursions
- referenced based memory management
- mostly R5RS compliant
- entirely CS61A compliant
- verbose standard library of complex procedures
- bitwise optimizations for math

```scheme
(define combine (lambda (proc)
  (lambda (x y)
    (if (null? x) (quote ())
      (proc (list (car x) (car y))
        ((combine proc) (cdr x) (cdr y)))))))
        
(define zip (combine cons))
```
*One of Peter Norvig's many Scheme test programs* 

<br>
The tiny-scheme core was compiled down from Python 3.6 to C using Cython. It should
be included by a gateway script that calls the evaluation routines in a REPL
or over a file stream. Such a gateway is included. Alternatively, an object
code version of the core is provided and can be called directly over a file. This allows
tiny-scheme to outperform Python in most cases. 

**compiling the tiny scheme core**
```
$ make build
$ ./bin/tiny-scheme --file <your_tiny_scheme_code>
```
If youd rather run tiny scheme as a REPL, you won't get the same speed :(
```
$ python3 tiny

Copyleft (C) Kaleb Horvath, TinyScheme
(eval)
```
