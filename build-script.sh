#!/bin/bash
SHARE="/usr/include/python3.6"
LIB="/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu"
cython tiny/core.py --embed
mkdir bin
gcc -Os -I$SHARE -L$LIB -o bin/core tiny/core.c -lpython3.6

