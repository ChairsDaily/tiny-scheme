# tiny-scheme
Fast and minimal interpreted runtime for a dialect of Scheme. Aims to eliminate things that
I find inconvenient in most implementations. 
- dynamic type casting at runtime
- cache aware parser
- tail call optimizations for linear recursions
- referenced based memory management
<br>
The tiny-scheme core was compiled down from Python 3.6 to C using Cython. It should
be included by a gateway script that calls the evaluation routines in a REPL
or over a file stream. Such a gateway is included. Alternatively, an object
code version of the core is provided and can be called directly over a file. This allows
tiny-scheme to outperform Python in most cases. 

## memory management
tiny scheme stays true to most LISP dialects and opts to maintain a hash map rather
than a stack. this environment grows as new bindings are created for symbols. when
procedures are called, a new child frame is created within the global environment
and is destroyed on return. garbage collection routines check the reference count
of symbol bindings if the environment reaches a certain size and free up space
accordingly. the recursive descent parser grows the python call stack very quickly
during lexical analysis, therefor programs are limited to 10^8 lines. 

## tail calls
a recursive call can be defined using the recurrence relation. lets use
factorial as an example - 
```
T(N) = N              if N = 1
T(N) = N * T(N - 1)   if N >= 1

function fact (n)
  return n if n = 1
  return n * fact ( n - 1 )
function main 
  fact ( 5 )
```
