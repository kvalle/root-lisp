# -*- coding: utf-8 -*-

isa = isinstance

def eval_axiom(ast, env):
    """Function for evaluating the basic axioms"""
    if isa(ast, str):        return eval_var(ast, env)
    elif ast[0] == "quote":  return ast[1]
    elif ast[0] == "atom":   return eval_atom(ast[1], env)
    elif ast[0] == "eq":     return eval_eq(ast[1], ast[2], env)
    elif ast[0] == "car":    return eval_car(ast[1], env)
    elif ast[0] == "cdr":    return eval_cdr(ast[1], env)
    elif ast[0] == "cons":   return eval_cons(ast[1], ast[2], env)
    elif ast[0] == "cond":   return eval_cond(ast[1:], env)
    elif ast[0] == "defun":  return eval_defun(ast[1], ast[2], ast[3], env)
    else: return apply_fn(ast[0], ast[1:], env)

def eval_var(var, env):
    for x, value in env:
        if x == var:
            return value
    raise LookupError("%s is unbound" % var)

def eval_atom(x, env):
    x = eval_axiom(x, env)
    if isa(x, str) or x == []:
        return 't'
    else:
        return []

def eval_eq(a, b, env):
    a = eval_axiom(a, env)
    b = eval_axiom(b, env)
    if [] == a == b:
        return 't'
    elif isa(a, str) and isa(b, str) and a == b:
        return 't'
    else:
        return []

def eval_car(lst, env):
    return eval_axiom(lst, env)[0]

def eval_cdr(lst, env):
    return eval_axiom(lst, env)[1:]

def eval_cons(a, b, env):
    return [eval_axiom(a, env)] + eval_axiom(b, env)

def eval_cond(exps, env):
    for p, e in exps:
        if eval_axiom(p, env):
            return eval_axiom(e, env)

def eval_defun(name, params, body, env):
    label = ["label", name, ["lambda", params, body]]
    env.insert(0, (name, label))
    return "t"

def apply_fn(fn, args, env):
    new_env = env

    # (f args)
    if isa(fn, str):
        fn = eval_var(fn, env)

    # ((label f (lambda ...) args))
    if fn[0] == "label":
        new_env = [(fn[1], fn)] + new_env
        fn = fn[2]

    (_, params, body) = fn
    args = [eval_axiom(e, env) for e in args]
    new_env = zip(params, args) + new_env

    return eval_axiom(body, new_env)
