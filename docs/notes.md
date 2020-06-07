
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

## acknowledgements
Thanks to Prof. Peter Norvig for his wonderful articles on building a LISP in Python 3. I would not have been able
to implement tail call optimizations without [this article](http://norvig.com/lispy.html). Thanks to San Franciso
University for providing me with dozens of R5RS compliance tests and UC Berkley for providing CS61A compliance
tests generously. Finally, thanks to several GitHub users (noted specifically in LICENSE) for their Scheme standard
library source code. These were also used to test my interpreter.
