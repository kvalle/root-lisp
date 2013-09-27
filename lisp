#!/usr/bin/env python

from sys import argv
from os.path import dirname, join
from rootlisp.lisp import interpret_file, repl
from rootlisp.parser import unparse

env = []
interpret_file(join(dirname(__file__), "stdlib.lisp"), env)

if len(argv) < 2:
    repl(env)
else:
    print unparse(interpret_file(argv[1], env))
