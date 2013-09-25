# -*- coding: utf-8 -*-

from parser import parse, unparse
from core import eval_axiom

def interpret(exp, env=None):
    """Interpret a single Lisp expression"""
    ast = parse(exp)
    exp = eval_axiom(ast, env if env is not None else [])
    return unparse(exp)

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
    repl()
