# -*- coding: utf-8 -*-

from parser import parse, parse_multiple, unparse
from core import eval

def interpret(exp, env=None):
    """Interpret a single Lisp expression"""
    ast = parse(exp)
    exp = eval(ast, env if env is not None else [])
    return unparse(exp)

def interpret_file(filename, env):
    """Interpret a list source file, returning value of last expression"""
    with open(filename, 'r') as f:
        source = f.read()
    asts = parse_multiple(source)
    results = [eval(ast, env) for ast in asts]
    return results[-1]

def repl(env=None):
    """A very simple REPL"""
    env = [] if env is None else env
    while True:
        try:
            print interpret(raw_input("> "), env)
        except (EOFError, KeyboardInterrupt):
            return
        except Exception, e:
            print "! %s" % e
