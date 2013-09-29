(defun caar (lst) (car (car lst)))
(defun cddr (lst) (cdr (cdr lst)))
(defun cadr (lst) (car (cdr lst)))
(defun cdar (lst) (cdr (car lst)))
(defun cadar (lst) (car (cdr (car lst))))
(defun caddr (lst) (car (cdr (cdr lst))))
(defun caddar (lst) (car (cdr (cdr (car lst)))))

(defun null (x)
    (eq x 'nil))

(defun and (x y)
    (cond (x (cond (y 't) ('t 'f)))
          ('t 'f)))

(defun not (x)
    (cond (x 'f)
          ('t 't)))

(defun append (x y)
    (cond ((null x) y)
          ('t (cons (car x) (append (cdr x) y)))))

(defun list (x y)
  (cons x (cons y 'nil)))

(defun pair (x y)
  (cond ((and (null x) (null y)) 'nil)
        ((and (not (atom x)) (not (atom y)))
         (cons (list (car x) (car y))
               (pair (cdr x) (cdr y))))))

(defun assoc (x y)
  (cond ((eq (caar y) x) (cadar y))
        ('t (assoc x (cdr y)))))

(defun eval (e a)
  (cond
    ((atom e) (assoc e a))
    ((atom (car e))
     (cond
       ((eq (car e) 'quote) (cadr e))
       ((eq (car e) 'atom)  (atom   (eval (cadr e) a)))
       ((eq (car e) 'eq)    (eq     (eval (cadr e) a)
                                    (eval (caddr e) a)))
       ((eq (car e) 'car)   (car    (eval (cadr e) a)))
       ((eq (car e) 'cdr)   (cdr    (eval (cadr e) a)))
       ((eq (car e) 'cons)  (cons   (eval (cadr e) a)
                                    (eval (caddr e) a)))
       ((eq (car e) 'cond)  (evcon (cdr e) a))
       ('t (eval (cons (assoc (car e) a)
                        (cdr e))
                  a))))
    ((eq (caar e) 'label)
     (eval (cons (caddar e) (cdr e))
            (cons (list (cadar e) (car e)) a)))
    ((eq (caar e) 'lambda)
     (eval (caddar e)
            (append (pair (cadar e) (evlis (cdr e) a))
                     a)))))

(defun evcon (c a)
  (cond ((eval (caar c) a)
         (eval (cadar c) a))
        ('t (evcon (cdr c) a))))

(defun evlis (m a)
  (cond ((null m) 'nil)
        ('t (cons (eval  (car m) a)
                  (evlis (cdr m) a)))))
