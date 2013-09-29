# -*- coding: utf-8 -*-

def is_atom(e): 
    return isinstance(e, str)

def eval(e, a):
    """Function for evaluating the basic axioms"""
    if is_atom(e): return lookup(e, a)
    elif is_atom(e[0]):
        if e[0] == "quote": return quote(e)
        elif e[0] == "atom": return atom(e, a)
        elif e[0] == "eq": return eq(e, a)
        elif e[0] == "car": return car(e, a)
        elif e[0] == "cdr": return cdr(e, a)
        elif e[0] == "cons": return cons(e, a)
        elif e[0] == "cond": return cond(e, a)
        elif e[0] == "defun": return defun(e, a)
        else: return call_named_fn(e, a)
    elif e[0][0] == "lambda": return apply(e, a)
    elif e[0][0] == "label": return label(e, a)

def lookup(e, a):
    for x, value in a:
        if x == e:
            return value
    raise LookupError("%s is unbound" % e)

def quote(e):
    return e[1]

def atom(e, a):
    a = eval(e[1], a)
    return 't' if is_atom(a) else 'f'

def eq(e, a):
    a, b = eval(e[1], a), eval(e[2], a)
    return 't' if a == b and is_atom(a) else 'f'

def car(e, a):
    return eval(e[1], a)[0]

def cdr(e, a):
    lst = eval(e[1], a)
    return 'nil' if len(lst) == 1 else lst[1:]

def cons(e, a):
    rest = eval(e[2], a)
    if rest == 'nil':
        rest = []
    return [eval(e[1], a)] + rest

def cond(e, a):
    for p, e in e[1:]:
        if eval(p, a) == 't':
            return eval(e, a)

def defun(e, a):
    name, params, body = e[1], e[2], e[3]
    label = ["label", name, ["lambda", params, body]]
    a.insert(0, (name, label))
    return name

def call_named_fn(e, a):
    fn = lookup(e[0], a)
    return eval([fn] + e[1:], a)

def label(e, a):
    _, f, fn = e[0]
    args = e[1:]
    return eval([fn] + args, [(f, e[0])] + a)

def apply(e, a):
    fn, args = e[0], e[1:]
    _, params, body = fn
    evaluated_args = map(lambda e: eval(e, a), args)
    a = zip(params, evaluated_args) + a
    return eval(body, a)
