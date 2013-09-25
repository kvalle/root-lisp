#!/usr/bin/env python

from sys import argv
from rootlisp.lisp import repl, interpret_file

if len(argv) < 2:
    repl()
else:
    result = interpret_file(argv[1], [])
    print unparse(result)
