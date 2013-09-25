# -*- coding: utf-8 -*-

from parser import parse, parse_multiple, unparse
from core import eval_axiom

def interpret(exp, env=None):
    """Interpret a single Lisp expression"""
    ast = parse(exp)
    exp = eval_axiom(ast, env if env is not None else [])
    return unparse(exp)

def interpret_file(filename, env):
    """Interpret a list source file, returning value of last expression"""
    with open(filename, 'r') as f:
        source = f.read()
    asts = parse_multiple(source)
    results = [eval_axiom(ast, env) for ast in asts]
    return results[-1]

def repl():
    """A very simple REPL"""
    env = []
    while True:
        try:
            print interpret(raw_input("> "), env)
        except (EOFError, KeyboardInterrupt):
            return
        except Exception, e:
            print "! %s" % e

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        repl()
    else:
        result = interpret_file(argv[1], [])
        print unparse(result)
