# -*- coding: utf-8 -*-

import re

def unparse(ast):
    if ast == []:
        return "()"
    elif isinstance(ast, list):
        if ast[0] == "quote":
            return "'%s" % unparse(ast[1])
        else:
            return "(%s)" % " ".join([unparse(x) for x in ast])
    else:
        return str(ast)

def parse(source):
    "Creates an Abstract Syntax Tree (AST) from program source (as string)"
    source = expand_quote_ticks(source)
    return analyze(tokenize(source))

def expand_quoted_symbol(source):
    # match anything with a tick (`',) followed by at least one character
    # that is not whitespace, a paren or another tick
    match = re.search(r"'([^'\(\s]+)", source)
    if match:
        start, end = match.span()
        source = "%(pre)s(quote %(quoted)s)%(post)s" % {
            "pre": source[:start], 
            "quoted": match.group(1), 
            "post": source[end:]
        }
    return source

def expand_quoted_list(source):
    # match any tick followed directly by an opening parenthesis
    match = re.search(r"'\(", source)
    if match:
        start = match.start()
        end = find_matching_paren(source, start + 1)
        source = "%(pre)s(quote %(quoted)s)%(post)s" % {
            "pre": source[:start],
            "quoted": source[start + 1:end],
            "post": source[end:] 
        }
    return source

def expand_quote_ticks(source):
    while "'" in source:
        source = expand_quoted_symbol(source)
        source = expand_quoted_list(source)
    return source

def find_matching_paren(source, start):
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

def tokenize(source):
    "Create list of tokens from (preprocessed) program source"
    return source.replace("(", " ( ").replace(")", " ) ").split()

def untokenize(tokens):
    return " ".join(tokens).replace("( ", "(").replace(" )", ")")

def analyze(tokens):
    """Transform list of token to AST

    Expects the tokens to constitute *one* single full AST.
    Throws an error otherwise.
    """
    sexp, rest = _read_elem(tokens)
    if len(rest) > 0:
        raise SyntaxError("Expected EOF got '%s'" % untokenize(rest))
    return sexp

def _read_elem(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF before closing paren")
    if tokens[0] == "(":
        return _read_list(tokens[1:])
    else:
        return (tokens[0], tokens[1:])

def _read_list(tokens):
    res = []
    while True:
        el, tokens = _read_elem(tokens)
        if el == ")": 
            break
        res.append(el)
    return res, tokens
