# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from rootlisp.lisp import interpret

class TestAxioms:
    """
    Tests for each of the axioms.

    Used more or less directly from "The Roots of Lisp" by Paul Graham
    """

    def test_evaluating_atoms(self):
        assert_equals('foo', interpret('a', [('a', 'foo')]))

    def test_quote(self):
        assert_equals('a', interpret('(quote a)'))
        assert_equals('a', interpret("'a"))
        assert_equals('(a b c)', interpret("(quote (a b c))"))
        assert_equals('(a b c)', interpret("'(a b c)"))

    def test_atom(self):
        assert_equals('t', interpret("(atom 'a)"))
        assert_equals('f', interpret("(atom '(a b c))"))
        assert_equals('t', interpret("(atom 'nil)"))
        assert_equals('t', interpret("(atom (atom 'a))"))
        assert_equals('f', interpret("(atom '(atom 'a))"))

    def test_eq(self):
        assert_equals('t', interpret("(eq 'a 'a)"))
        assert_equals('f', interpret("(eq 'a 'b)"))
        assert_equals('f', interpret("(eq '(a) '(a))"))

    def test_car(self):
        assert_equals('a', interpret("(car '(a b c))"))

    def test_cdr(self):
        assert_equals('(b c)', interpret("(cdr '(a b c))"))
        assert_equals('nil', interpret("(cdr '(a))"))

    def test_cons(self):
        assert_equals('(a b c)', interpret("(cons 'a '(b c))"))
        assert_equals('(a)', interpret("(cons 'a 'nil)"))
        assert_equals('(a b c)', interpret("(cons 'a (cons 'b  (cons 'c 'nil)))"))
        assert_equals('a', interpret("(car (cons 'a '(b c)))"))
        assert_equals('(b c)', interpret("(cdr (cons 'a '(b c)))"))

    def test_cond(self):
        lisp = """
            (cond ((eq 'a 'b) 'first)
                  ((atom 'a) 'second))
        """
        assert_equals('second', interpret(lisp))
