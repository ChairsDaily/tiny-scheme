# python3.6 makefile, system specific
# not for general use DEPENDS HEAVILY ON CYTHON AND GCC
# @author chairs

MAKEFLAGS += --silent
SHARE=/usr/include/python3.6
LIBS=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu
PYTHON=python3.6

C_PROG=tiny/core.c
PY_PROG=tiny/core.py

#CC=gcc
#CFLAGS=-Os -I -L

.PHONY: help sync build 
default: help
sync:
	chmod +x sync.sh
	./sync.sh "update"
build:
	cython $(PY_PROG) --embed
	mkdir bin/
	gcc -Os -I$(SHARE) -L$(LIBS) -o bin/tiny-scheme $(C_PROG) -l$(PYTHON)
help:
	@echo "build"
	@echo "   compile tiny scheme core"
	@echo "clean"
	@echo "   remove build files"
	@echo "test"
	@echo "   run unittests over tests/ folder"
	@echo "---------------------------------------------------"
	@echo "clean-build"
	@echo "	  clean up build files (bin/, __pycache__/, etc.)"
	@echo "clean-test"
	@echo "   clean up unittest files and configs"

.PHONY: clean-build clean-test
clean-build:
	# assumes build was ran already
	/bin/rm -rf bin
	/bin/rm tiny/*.c
	/bin/rm -rf tiny/__pycache__/
clean-test:
	# assumes test was ran already
	/bin/rm -rf tests/__pycache__/
	/bin/rm -rf tiny/__pycache__/

.PHONY: run test 
run: 
	#./bin/tiny-scheme
	# will spawn a REPL for tiny scheme
	python3 tiny
test:
	#python3 -m unittest discover
	python3 -m unittest tests.test_parser
