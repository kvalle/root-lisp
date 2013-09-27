
(defun zip (x y) 
    (cond ((null x) y)
          ((null y) x)
          ('t (cons (car x) 
                    (cons (car y) 
                          (zip (cdr x) (cdr y)))))))

(zip '(a b c d) '(x y z))
