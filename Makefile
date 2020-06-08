
MAKEFLAGS += --silent
SHARE=/usr/include/python3.6
LIBS=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu
PYTHON=python3.6

C_PROG=tiny/core.c
PY_PROG=tiny/core.py

#CC=gcc
#CFLAGS=-Os -I -L

.PHONY: help build clean test dev

default: help
dev:
	chmod +x sync.sh
build:
	cython $(PY_PROG) --embed
	mkdir bin/
	gcc -Os -I$(SHARE) -L$(LIBS) -o bin/tiny-scheme $(C_PROG) -l$(PYTHON)
help:
	@echo "build"
	@echo "   compile tiny scheme core"
	@echo "clean"
	@echo "   remove build files"

clean: 
	/bin/rm -rf bin
	/bin/rm tiny/*.c

run: ./bin/tiny-scheme
test:
	python3 -m unittest discover
