#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Copyleft (C) 2020 Kaleb Horvath

This program is free software: you can redistribute it and/or
modify it freely under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 or (at your option) any later version.

Reproduction and distribution of this program or derivative 
works thereof in any medium physical or digital, with or 
without modification, in source or compiled form, free of 
charge or with a price is granted provided that 
you meet the following requirements:

        (a) You must give any other recipients of the above
            a copy of the GNU GPLv3; and
        (b) You must cause any modified files to carry a prominent
            notice stating clearly that You modifed the changed files; and
        (c) The full name associated with the Copyleft header must be
            carried prominently in your distribution of this program.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PURPOSE. See the GNU
General Public License for more details regarding permissions.
Be it known serious violations will be reported and that all 
developers associated with the original creation of this program 
have the dedicated legal support of the GNU FSF.

You should have received a copy of the GNU General Public License
(version 3) along with this program. If not, visit
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""
"""
TODO:
- LRU cache for the parser
- pre-compiled Cython integrations
- bitwise optimizations
- evenop? zerop? oddop? procedures
- copy-list, zip, filter, range, splice, 
  reverse, sort, etc. procedures
- garbage collected environment
- gc API for the user
- memoization API for the user
"""
import traceback 
import operator as op
import math  
import sys, gc, os
from functools import wraps 
from optparse import OptionParser

# tiny scheme types
ts_symbol = str
ts_number = (int, float)
ts_list = list 

# tiny scheme primitive procedures
# (will add list processing later in file)
ts_procs = {
    '+': op.add, '-': op.sub, '*': op.mul, 
    '/': op.truediv, '>': op.gt, '<': op.lt,
    '>=': op.ge, '<=': op.le, '=': op.eq,
    'not': op.not_, 'or': op.or_, 'mod': lambda a,b: a % b,
    'and': op.and_, 'eq?': op.is_, 'abs': abs, 'sum': sum,

    # type predicates
    'list?': lambda a: isinstance(a, list),
    'symbol?': lambda a: isinstance(a, ts_symbol),
    'null?': lambda a: a == [],
    'boolean?': lambda a: isinstance(a, bool),
    'number?': lambda a: isinstance(a, ts_number)
}


# some classic list processing primitives (regular forms)
# should be private bound to this module alone
# dont want them being imported
def __cons (car_atom, cdr_atom) -> ts_list:
    """
    Takes a first and rest and builds a tiny scheme list.
    """
    islist = (isinstance(car_atom, list), isinstance(cdr_atom, list))
    if not any(islist): return [car_atom, cdr_atom]
    else:
        if all(islist): return car_atom + cdr_atom 
        try: 
            return [car_atom] + cdr_atom 
        except ValueError: return car_atom + [cdr_atom]

def __car (cons_list: list):
    """
    Get first from a cons or list
    """
    if not isinstance(cons_list, list): 
        ts_error('[!] invalid argument for primitive', exit=1)()
    else:
        return cons_list[0]

def __cdr (cons_list: list):
    """
    Get rest from a cons or a list
    """
    if not isinstance(cons_list, list): 
        ts_error('[!] invalid argument for primitive', exit=1)()
    else:
        return cons_list[1:]
def __nil () -> ts_list: return [] 
def __objid (obj) -> int: return id(obj)
def __list (*atoms) -> ts_list: return list(atoms)
def __length (cons_list): 
    """
    Get the length from a cons or list
    """
    if not isinstance(cons_list, list): 
        ts_error('[!] invalid argument for primitive', exit=1)()
    else:
        return len(cons_list)

def __map (procedure, cons_list: ts_list) -> ts_list:
    """
    Return transformed copy (per the procedure) of cons_list
    """
    if not isinstance(cons_list, list) or not callable(procedure): 
        ts_error(' [!] invalid argument for primitive', exit=1)()
    else:
        return [
            procedure(atom) for atom in cons_list
        ]

# some classic primitives (special forms)
# should be private bound to this module alone
# dont want them being imported
def __cond (x, env):
    (_, *conds, alt) = x 
    tests = [eval(pair[0], env) for pair in conds]
    sat = False 
    for i in range(len(conds)):
        if tests[i]:
            x = conds[i][1]; sat = True 
    if not sat: x = alt
    return x 

def __if (x, env):
    (_, test, conseq, alt) = x
    x = (conseq if eval(test, env) else alt) 
    return x 

def __set (x, env):
    (_, var, exp) = x
    env.find(var)[var][0] = eval(exp, env)
    return None 

def __display (x, env):
    (_, exps) = x
    print('%s' % ' '.join(exps))
                
def __define (x, env):
    (_, var, exp) = x
    env[var] = [eval(exp, env), 0]
    return None

def __lambda (x, env):
    (_, vars, exp) = x
    return ts_lambda(vars, exp, env)

def __begin (x, env):
    for expression in x[1:]:
        eval(expression, env)
    x = x[-1]
    return x 

def __lookup (x, env):
    if x[0] == 'if': pass
    if x in ts_procs:
        return env.find(x)[x]
    frame = env.find(x)
    frame[x][1] += 1
    return frame[x][0]

def __member (x, env):
    (_, var, lst) = x
    return (eval(var, env) in eval(lst, env))

# primitive procedures
ts_procs.update({'cons': __cons, 'car': __car, 'cdr': __cdr,
    'nil': [], 'list': __list, 'length': len,
    'map': __map, '&': __objid, 'filter': lambda c,l: list(filter(c, l)),

    # exposing some system calls for our UNIX shell project
    #'readline': __ts_readline,
    #'fork': __ts_fork, 'waitpid': __ts_waitpid, 
    #'exec': __ts_execvp, 'shlex': __ts_shlex,   
    })


def ts_cache (function):
    """
    Caches a procedure using least recently used policy.
    (this one sucks donkey dick fix it)
    """
    Cache = dict()
    @wraps(function)
    def wrapper (*arguments):

        # hash the procedure arguments
        flat = [i for j in arguments for i in j]
        flat = ''.join((i for i in flat))

        if flat in Cache: return Cache[flat]
        else:
            result = function(*arguments)
            Cache[flat] = result 

            return result 
    return wrapper


class ts_error (object):
    """
    Raised when any scheme operation fails.
    Should be called on failure.

    Arguments:
        message (str) will be displayed on call
        exit (int) if greater than 0 TS will terminate
        exception (Exception) the real Python exception

    Example:
        >>> ts_error('unbound symbol', exit=1)
    
    """
    def __init__ (self, message, exit=0, trace=None):
        self.message = str(message)
        self.exc = trace
        self.exit = int(exit) 

    
    def __call__ (self):
        sys.stdout.write('[!] %s\n' % self.message)
        if self.exc != None:

            return ''.join(traceback.format_exception(
                etype=type(self.exc),
                value=self.exc,
                tb=self.exc.__traceback__
            ))
        if self.exit > 0: 
            sys.exit(self.exit)

class ts_env (dict):
    """
    An environment frame to hold symbol bindings. Adjustment
    of the native dictionary object.

    Has some special arguments for creating a child frame
    specifically for user defined procedures. Scoping
    is handled this way.

    Arguments:
        params (tuple) the parameters for the user defined procedure
        args (tuple) the real args that are passed
        outer (ts_env) the parent environment frame (global scope)

    Examples:
        >>> # for the global env
        >>> global_env = add_primitives(ts_env())

        >>> # for a user defined procedure
        >>> (_, vars, exp) = x
        >>> ts_env(vars, *args, outer=env)
    """
    def __init__ (self, params=(), args=(), outer=None):
        self.outer = outer 
        if isinstance(params, ts_number):
            self.update(self.__formatsymbol__(params, args))
        else:
            if len(args) != len(params):
                ts_error('[!] bad arguments given to procedure', exit=1)()
            self.update(self.__formatprocedure__(params, args))
    
    def __formatsymbol__ (self, params, args):
        """
        Format a normal symbol: value binding with a ref count.
        """
        return {params: list(args)}

    
    def __formatprocedure__ (self, params, args):
        """
        Format the special symbol: procedure binding with a ref count.
        """
        params = [list(pair) for pair in list(zip(params, args))]
        proc = []
        for pair in params:
            proc.append([pair[0], [pair[1], 0]])
        # acceptable nested list format for dict.update
        return proc

    
    def find (self, binding):
        """
        Locate a binding within this frame or its parent.
        """
        if binding in self: return self
        try:
            return self.outer.find(binding)
        except Exception as e:
            # no need to do a full trace for an environment error
            ts_error('unbound symbol %s' % binding, exit=1)()

class ts_lambda (object):
    def __init__ (self, params, exp, env):
        self.params, self.exp, self.env = params, exp, env 

    def __call__ (self, *args):
        return eval(self.exp, ts_env(self.params, args, self.env))



# some more type definitions and conversion functions
def ts_string (native_object):
    """
    Convert one of the valid native objects into a scheme
    readable string.
    """
    if isinstance(native_object, list):
        return '(' + ' '.join(map(ts_string, native_object)) + ')'
    else:
        return str(native_object)

@ts_cache
def ts_atom (token):
    """
    Convert a scheme atom to a native object for evaluation.
    """
    if token == '#t': return True 
    if token == '#f': return False 
    
    # should be noted that 1 and 0 can be treated as false 
    else:
        try: return ts_number[0](token)
        except ValueError: 
            try: return ts_number[1](token)
            except ValueError: return ts_symbol(token)

def add_primitives (env) -> ts_env:
    """
    Store primitive bindings within an environment frame
    """
    env.update(ts_procs); return env


global_env = add_primitives(ts_env())
isa = isinstance

#working on this part
#@ts_cache
def eval (x, env=global_env):

    while True:
        if isa(x, ts_symbol): return __lookup(x, env)
        elif not isa(x, list): return x 

        if x[0] in ['quote']: (_, exp) = x; return exp 
        elif x[0] in ['display']: __display(x, env); return None
        elif x[0] in ['if']: x = __if(x, env)
        elif x[0] in ['cond']: x = __cond(x, env)
        elif x[0] in ['set!']: return __set(x, env)
        elif x[0] in ['define']:return  __define(x, env)
        elif x[0] in ['lambda']: return __lambda(x, env)
        elif x[0] in  ['member?']: return __member(x, env)
        elif x[0] in ['begin']: x = __begin(x, env)
        else:
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, ts_lambda):
                x = proc.exp 
                env = ts_env(proc.params, exps, proc.env)
            else:
                return proc(*exps)




def tokenize (string):
    """
    Tokenize a scheme readable expression string
    """
    return string.replace('(', ' ( ').replace(')', ' ) ').split()


sys.setrecursionlimit(16000)
@ts_cache
def parse (tokens):
    """
    Convert token stream into abstract syntax tree ready for eval
    """
    try:
        if len(tokens) == 0: ts_error('early eof', exit=1)()
        token = tokens.pop(0)
        
        if token is '(':
            L = []
            while tokens[0] != ')':
                L.append(parse(tokens))
            tokens.pop(0)
            return L 

        elif token is ')': ts_error('early )', exit=1)()
        else:
            return ts_atom(token)
    except Exception:
        sys.exit('unknown parser failure')

from optparse import OptionParser

def load_source (file):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            return ' '.join([
                l for l in lines if ';' not in l
            ]).replace('\t','').replace('\n','')
    else:
        sys.exit('file not found')

if __name__ == '__main__':
    options = OptionParser()
    options.add_option('-f', '--file',
        dest='source', help='file with scheme source code')
    (options, args) = options.parse_args()

    try:
        result = eval(parse(tokenize(load_source(options.source))))
        print(ts_string(result))

    except Exception as e:
        sys.exit(e)

