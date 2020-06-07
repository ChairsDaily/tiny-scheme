
from optparse import OptionParser
import os
from core import *

def repl ():
    print('TinyScheme, Copyleft (C) 2020 Kaleb Horvath')
    while True:
        try:
            scheme = input('(eval) ')
        except KeyboardInterrupt:
            sys.exit('quitting tiny scheme')

        result = eval(parse(tokenize(scheme)))
        if result is not None: 
            print(ts_string(result))

if __name__ == '__main__':
    repl()

