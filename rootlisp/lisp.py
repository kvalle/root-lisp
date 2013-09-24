# -*- coding: utf-8 -*-

from parser import parse, unparse

isa = isinstance

def interpret(exp):
    """Interpret Lisp expression"""
    ast = parse(exp)
    exp = eval_axiom(ast)
    return unparse(exp)

def eval_axiom(ast):
    """Function for evaluating the basic axioms"""
    if   ast[0] == "quote":  return ast[1]
    elif ast[0] == "atom": return eval_atom(ast[1])
    elif ast[0] == "eq":   return eval_eq(ast[1], ast[2])
    elif ast[0] == "car":  return eval_car(ast[1])
    elif ast[0] == "cdr":  return eval_cdr(ast[1])
    elif ast[0] == "cons": return eval_cons(ast[1], ast[2])
    elif ast[0] == "cond": return eval_cond(ast[1:])
    raise NotImplementedError("lambda and label still missing...")

def eval_atom(x):
    x = eval_axiom(x)
    if isa(x, str) or x == []:
        return 't'
    else:
        return []

def eval_eq(a, b):
    a = eval_axiom(a)
    b = eval_axiom(b)
    if [] == a == b:
        return 't'
    elif isa(a, str) and isa(b, str) and a == b:
        return 't'
    else:
        return []

def eval_car(lst):
    return eval_axiom(lst)[0]

def eval_cdr(lst):
    return eval_axiom(lst)[1:]

def eval_cons(a, b):
    return [eval_axiom(a)] + eval_axiom(b)

def eval_cond(exps):
    for p, e in exps:
        if eval_axiom(p):
            return eval_axiom(e)
