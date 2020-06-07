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

**compiling the tiny scheme core**
```
$ bash build-script.sh
$ ./bin/core --file <your_tiny_scheme_code>
```
If youd rather run tiny scheme as a REPL, you won't get the same speed :(
```
$ python3 tiny/repl.py

Copyleft (C) Kaleb Horvath, TinyScheme
(eval)
```

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
When `main` is called, an entry storing its state (parameters and return address) is pushed
onto the stack. `main` will remain here until the program terminates and control is returned back
to our pseudocode runtime ;) each call to `fact` will push to the stack containing the 
return address, or the address of the frame 'below' it and its parameters. this is so that
when a call converges, it knows where to hand off program control to. 
```
fact(1) <- base case (recursion terminates here)
fact(2)
fact(3)
fact(4)
fact(5) <- initial push
main( )
```
At base case, each call is popped off the stack **after** it terminates. This takes time. The result
is accumulated down the stack until program control returns to `main` along with the result. In recursion,
this stack portion of the programs memory grows very quickly, often times before the runtime has a chance
to pop off calls, freeing the space. There are two popular solutions to stack overflow in deep recursions.
- raise the stack limit by allocating it more of the programs memory
- tail call recursion for linear cases
<br>
Tail calls themself do not actually solve the problem of stack overflow, rather they greatly reduce
the amount of time it takes for a recursive routine to return program control by accumulating the final
result, whatever it may be, on the way up the stack which eliminates the waiting time before each routine
is popped off and control returned. 

```
function fact (n, a)
  return a if n = 1
  return fact ( n - 1, a * n )
function main 
  fact ( 5 )
```

At base-case termination, `fact` orders a return of `a` and directs program control to the address of the call
'below' it. because `a` is being returned as an accumulator instead of `n` itself, you do not have to wait
to evaluate `n`. `a` is already pointing to the result in memory. The good news is, most functional programming languages
that rely on recursion to reduce state and mutability (like tiny-scheme) optimize these faster tail call recursions into control flow jumps. What does this mean? Because there is no work left to be done after `return fact ( n - 1, a * n )` in that recursive call (e.g. `n * fact (...)`), the interpreter will not push a new call onto the stack. Instead, it re-binds `n` and `a` to their new values and jumps to the beginning of the same routine. The stack does not grow. This is handled
using a while loop in tiny-scheme, and allows your recursive functions to recurse deeply without concern of overflow and without having to allocate more memory.  

