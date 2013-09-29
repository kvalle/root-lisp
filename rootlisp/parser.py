# -*- coding: utf-8 -*-

import re

def unparse(ast):
    """Convert an AST back into the corresponding lisp expression"""
    if isinstance(ast, str): return ast
    elif ast == []: return "()"
    else:
        if ast[0] == "quote":
            return "'%s" % unparse(ast[1])
        else:
            return "(%s)" % " ".join([unparse(x) for x in ast])

def parse(source):
    """Parse string representation of one single expression
    into the corresponding Abstract Syntax Tree"""
    exp, rest = partition_exp(source)
    if rest:
        raise SyntaxError('Expected EOF')

    if exp[0] == "'":
        return ["quote", parse(exp[1:])]
    elif exp[0] == "(":
        end = find_matching_paren(exp)
        return [parse(e) for e in split_exps(exp[1:end])]
    else:
        return exp

def parse_multiple(source):
    """Creates a list of ASTs from program source 
    constituting multiple expressions"""
    return [parse(exp) for exp in split_exps(source)]

def split_exps(source):
    """Splits a source string into subexpressions 
    that can be parsed individually"""
    rest = source.strip()
    exps = []
    while rest:
        exp, rest = partition_exp(rest)
        exps.append(exp)
    return exps

def partition_exp(source):
    """Split string into (exp, rest) where exp is the 
    first expression in the string and rest is the 
    rest of the string after this expression."""
    source = source.strip()
    if source[0] == "'":
        exp, rest = partition_exp(source[1:])
        return "'" + exp, rest
    elif source[0] == "(":
        last = find_matching_paren(source)
        return source[:last + 1], source[last + 1:]
    else:
        match = re.match(r"^[^\s)']+", source)
        end = match.end()
        atom = source[:end]
        return atom, source[end:]

def find_matching_paren(source, start=0):
    """Given a string and the index of an opening parenthesis, determine 
    the index of the matching closing paren"""
    assert source[start] == '('
    pos = start
    open_brackets = 1
    while open_brackets > 0:
        pos += 1
        if len(source) == pos:
            raise SyntaxError("Unbalanced expression: %s" % source[start:])
        if source[pos] == '(':
            open_brackets += 1
        if source[pos] == ')':
            open_brackets -= 1
    return pos
