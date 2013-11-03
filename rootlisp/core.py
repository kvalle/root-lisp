# -*- coding: utf-8 -*-

def is_atom(exp): 
    return isinstance(exp, str)

def eval(exp, env):
    """Function for evaluating the basic axioms"""
    if is_atom(exp): return lookup(exp, env)
    elif is_atom(exp[0]):
        if exp[0] == "quote": return quote(exp)
        elif exp[0] == "atom": return atom(exp, env)
        elif exp[0] == "eq": return eq(exp, env)
        elif exp[0] == "car": return car(exp, env)
        elif exp[0] == "cdr": return cdr(exp, env)
        elif exp[0] == "cons": return cons(exp, env)
        elif exp[0] == "cond": return cond(exp, env)
        elif exp[0] == "defun": return defun(exp, env)
        else: return call_named_fn(exp, env)
    elif exp[0][0] == "lambda": return apply(exp, env)
    elif exp[0][0] == "label": return label(exp, env)

def lookup(atom, env):
    for x, value in env:
        if x == atom:
            return value
    raise LookupError("%s is unbound" % atom)

def quote(exp):
    return exp[1]

def atom(exp, env):
    val = eval(exp[1], env)
    return 't' if is_atom(val) else 'f'

def eq(exp, env):
    v1, v2 = eval(exp[1], env), eval(exp[2], env)
    return 't' if v1 == v2 and is_atom(v1) else 'f'

def car(exp, env):
    return eval(exp[1], env)[0]

def cdr(exp, env):
    lst = eval(exp[1], env)
    return 'nil' if len(lst) == 1 else lst[1:]

def cons(exp, env):
    rest = eval(exp[2], env)
    if rest == 'nil':
        rest = []
    return [eval(exp[1], env)] + rest

def cond(exp, env):
    for p, e in exp[1:]:
        if eval(p, env) == 't':
            return eval(e, env)

def defun(exp, env):
    name, params, body = exp[1], exp[2], exp[3]
    label = ["label", name, ["lambda", params, body]]
    env.insert(0, (name, label))
    return name

def call_named_fn(exp, env):
    fn = lookup(exp[0], env)
    return eval([fn] + exp[1:], env)

def label(exp, env):
    _, f, fn = exp[0]
    args = exp[1:]
    return eval([fn] + args, [(f, exp[0])] + env)

def apply(exp, env):
    fn, args = exp[0], exp[1:]
    _, params, body = fn
    evaluated_args = map(lambda e: eval(e, env), args)
    new_env = zip(params, evaluated_args) + env
    return eval(body, new_env)
