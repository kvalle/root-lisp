# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from rootlisp.lisp import interpret

class TestFunctions:

    def test_function_call(self):
        assert_equals('(a b)', interpret("((lambda (x) (cons x '(b))) 'a)"))
        assert_equals('(z b c)', interpret("""
            ((lambda (x y) (cons x (cdr y)))
                'z
                '(a b c))
        """))

    def test_calling_argument_as_function(self):
        assert_equals('(a b c)', interpret("""
            ((lambda (f) (f '(b c)))
                '(lambda (x) (cons 'a x)))
        """))

    def test_recursive_function_with_label(self):
        assert_equals('(a m (a m c) d)', interpret("""
            ((label subst (lambda (x y z)
                            (cond ((atom z)
                                   (cond ((eq z y) x)
                                         ('t z)))
                                  ('t (cons (subst x y (car z))
                                            (subst x y (cdr z)))))))
                'm
                'b
                '(a b (a b c) d))
        """))

    def test_simple_defun(self):
        env = []
        interpret("(defun foo (x y z) (cons x (cons y (cons z '()))))", env)
        assert_equals('(a b c)', interpret("(foo 'a 'b 'c)", env))

    def test_recursive_function_with_defun(self):
        env = []
        interpret("""
            (defun subst (x y z) 
                (cond ((atom z)
                       (cond ((eq z y) x)
                             ('t z)))
                      ('t (cons (subst x y (car z))
                                (subst x y (cdr z))))))
        """, env)
        assert_equals('(a m (a m c) d)', interpret("(subst 'm 'b '(a b (a b c) d))", env))
