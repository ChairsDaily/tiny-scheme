# tiny-scheme
Fast and minimal interpreted runtime for a dialect of Scheme. Aims to eliminate things that
I find inconvenient in most implementations. 
- dynamic type casting at runtime
- cache aware parser
- tail call optimizations for linear recursions
- referenced based memory management
The tiny-scheme core was compiled down from Python 3.6 to C using Cython. It should
be included by a gateway script that calls the evaluation routines in a REPL
or over a file stream. Such a gateway is included. Alternatively, an object
code version of the core is provided and can be called directly over a file. This allows
tiny-scheme to outperform Python in most cases. 
<br>
Slower operations are optimized using bitwise arithmetic, and user defined procedures
are automatically memoized. The tiny-scheme runtime defaults to a maximum value
for the number of bindings allowed before a garbage collection cycle is triggered. 
The garbage collector can be disabled or size extended using the provided interface.
Due to memory allocation reasons, this extension cannot exceed 10^8. This is because
of the Python virtual machines own limitations. It is also not advised
to disable the gc because the environment will eat up user space memory 
very quickly if not cleaned every so often at runtime. This is a consequence of a 
dynamically typed language with automatic memory management routines. 
Deep recursions will not grow the environment as the child frames are created
and never referenced, automatically destroyed by Python. These calls do however
grow the Python call stack if not implemented properly.
<br>
Tail recursion is supported, and optimized. A normal recursion 
