# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from rootlisp.lisp import interpret, interpret_file

class TestStdlib:

    def setup(self):
        self.env = []
        interpret_file("stdlib.lisp", self.env)

    def test_null(self):
        assert_equals('()', interpret("(null 'a)", self.env))
        assert_equals('t', interpret("(null '())", self.env))

    def test_and(self):
        assert_equals('t', interpret("(and (atom 'a) (eq 'a 'a))", self.env))
        assert_equals('()', interpret("(and (atom 'a) (eq 'a 'b))", self.env))

    def test_not(self):
        assert_equals('()', interpret("(not (eq 'a 'a))", self.env))
        assert_equals('t', interpret("(not (eq 'a 'b))", self.env))

    def test_append(self):
        assert_equals('(a b c d)', interpret("(append '(a b) '(c d))", self.env))
        assert_equals('(c d)', interpret("(append '() '(c d))", self.env))

    def test_pair(self):
        assert_equals('((x a) (y b) (z c))', 
            interpret("(pair '(x y z) '(a b c))", self.env))

    def test_assoc(self):
        assert_equals('a', interpret("(assoc 'x '((x a) (y b)))", self.env))
        assert_equals('b', interpret("(assoc 'y '((x a) (y b)))", self.env))
        assert_equals('new', interpret("(assoc 'x '((x new) (x a) (y b)))", self.env))

    def test_eval_lookup(self):
        assert_equals('a', interpret("(eval 'x '((x a) (y b)))", self.env))

    def test_eval_eq(self):
        assert_equals('t', interpret("(eval '(eq 'a 'a) '())", self.env))

    def test_eval_cons(self):
        program = """
            (eval '(cons x '(b c)) 
                  '((x a) (y b)))
        """
        assert_equals('(a b c)', interpret(program, self.env))

    def test_eval_cond(self):
        program = """
            (eval '(cond ((atom x) 'atom) 
                         ('t 'list)) 
                  '((x '(a b))))
        """
        assert_equals('list', interpret(program, self.env))

    def test_eval_lambda_direct(self):
        program = """
            (eval '((lambda (x y) (cons x (cdr y)))
                    'a
                    '(b c d))
                  '())
        """
        assert_equals('(a c d)', interpret(program, self.env))

    def test_eval_lambda_lookup(self):
        program = """
            (eval '(f '(b c))
                  '((f (lambda (x) (cons 'a x)))))
        """
        assert_equals('(a b c)', interpret(program, self.env))

    def test_eval_label(self):
        program = """
            (eval '((label firstatom (lambda (x)
                                       (cond ((atom x) x)
                                             ('t (firstatom (car x))))))
                    y)
                  '((y ((a b) (c d)))))
        """
        assert_equals('a', interpret(program, self.env))
