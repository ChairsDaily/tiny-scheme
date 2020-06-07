MAKEFLAGS += --silent

# change by system
SHARE=/usr/include/python3.6
LIBS=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu
PYTHON=python3.6
PROGRAM=tiny/core.py
CC=gcc

.PHONY: help build clean test

default: help
build:
  - mkdir bin
  - $(CC) -Os -I$(SHARE) -L$(LIBS) -o bin/tinyscheme $(PROGRAM) -l$(PYTHON)
 
 help:
  @echo "build"
  @echo "   compile tiny scheme core"
  @echo "clean"
  @echo "   remove build files"
 
 clean:
  - rm -rf bin/
 
 test:
  - ./bin/tinyscheme
