# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_raises_regexp

from rootlisp.parser import tokenize, parse, unparse, expand_quote_ticks, \
    find_matching_paren, expand_quoted_symbol, expand_quoted_list

class TestParsing:

    ## Basic parsing

    def test_tokenize_single_atom(self):
        assert_equals(['foo'], tokenize('foo'))

    def test_tokenize_list(self):
        source = '(foo 1 2)'
        tokens = ['(', 'foo', '1', '2', ')']
        assert_equals(tokens, tokenize(source))

    def test_parse_on_simple_list(self):
        program = '(foo bar)'
        assert_equals(['foo', 'bar'], parse(program))

    def test_parse_on_tested_list(self):
        program = '(foo (bar x y) (baz x))'
        ast = ['foo', 
                ['bar', 'x', 'y'], 
                ['baz', 'x']]
        assert_equals(ast, parse(program))

    ## Tests for parsing bad expressions

    def test_parse_exception_missing_paren(self):
        with assert_raises_regexp(SyntaxError, 'Unexpected EOF'):
            parse('(foo (bar x y)')

    def test_parse_exception_extra_paren(self):
        with assert_raises_regexp(SyntaxError, 'Expected EOF'):
            parse('(foo (bar x y)))')

    ## Tests for find_matching_paren function

    def test_find_matching_paren(self):
        source = "(foo (bar) '(this ((is)) quoted))"
        assert_equals(32, find_matching_paren(source, 0))
        assert_equals(9, find_matching_paren(source, 5))

    def test_find_matching_empty_parens(self):
        assert_equals(1, find_matching_paren("()", 0))

    def test_find_matching_paren_throws_exception_on_bad_initial_position(self):
        """If asked to find closing paren from an index where there is no opening
        paren, the function should raise an error"""

        with assert_raises(AssertionError):
            find_matching_paren("string without parens", 4)

    def test_find_matching_paren_throws_exception_on_no_closing_paren(self):
        """The function should raise error when there is no matching paren to be found"""

        with assert_raises_regexp(SyntaxError, "Unbalanced expression"):
            find_matching_paren("string (without closing paren", 7)

    ## Tests for expanding quoted symbols

    def test_expand_single_quoted_symbol(self):
        assert_equals("(foo (quote bar))", expand_quoted_symbol("(foo 'bar)"))
        assert_equals("(foo (quote #t))", expand_quoted_symbol("(foo '#t)"))
        assert_equals("(foo (quote +))", expand_quoted_symbol("(foo '+)"))

    def test_expand_quoted_symbol_dont_touch_nested_quote_on_list(self):
        source = "(foo ''(bar))"
        assert_equals(source, expand_quoted_symbol(source))

    def test_expand_quotes_with_only_symbols(self):
        assert_equals("(quote foo)", expand_quote_ticks("'foo"))
        assert_equals("(quote (quote (quote foo)))", expand_quote_ticks("'''foo"))

    def test_parse_quote_tick_on_atom(self):
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", "+"], parse("'+"))
        assert_equals(["quote", "1"], parse("'1"))

    def test_nested_quotes(self):
        assert_equals(["quote", ["quote", "foo"]], parse("''foo"))
        assert_equals(["quote", ["quote", ["quote", "foo"]]], parse("'''foo"))

    ## Tests for expanding quoted lists

    def test_expand_single_quoted_list(self):
        assert_equals("(foo (quote (+ 1 2)))", expand_quoted_list("(foo '(+ 1 2))"))
        assert_equals("(foo (quote (#t #f)))", expand_quoted_list("(foo '(#t #f))"))

    def test_expand_quotes_with_lists(self):
        assert_equals("(quote (foo bar))", expand_quote_ticks("'(foo bar)"))
        assert_equals("(quote (quote (quote (foo bar))))", 
            expand_quote_ticks("'''(foo bar)"))

    def test_parse_quote_tick_on_list(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", []], parse("'()"))

    def test_nested_quotes_on_lists(self):
        assert_equals(["quote", ["quote", ["foo", "bar"]]], parse("''(foo bar)"))

    def test_unparse_symbol(self):
        assert_equals("+", unparse("+"))
        assert_equals("foo", unparse("foo"))
        assert_equals("lambda", unparse("lambda"))

    def test_unparse_list(self):
        assert_equals("(1 2 3)", unparse(["1", "2", "3"]))
        assert_equals("(if (foo bar) 42 end)", 
            unparse(["if", ["foo", "bar"], "42", "end"]))

    def test_unparse_quotes(self):
        assert_equals("'foo", unparse(["quote", "foo"]))
        assert_equals("'(1 2 3)", unparse(["quote", ["1", "2", "3"]]))

    def test_unparse_empty_list(self):
        assert_equals("()", unparse([]))
