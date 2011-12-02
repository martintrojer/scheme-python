from unittest import *
import mtscheme

class simple_test(TestCase):
    def setUp(self):
        self.mts = mtscheme.MTScheme()

class prim_add(simple_test):
    def runTest(self):
        assert self.mts.run("(+ 1 1)") == 1+1
        assert self.mts.run("(+ 1 (+ 2 3))") == 1+(2+3)
        self.assertAlmostEqual(self.mts.run("(+ 1 (+ 2 3.14))"),(1+(2+3.14)))
class prim_sub(simple_test):
    def runTest(self):
        assert self.mts.run("(- 1 1)") == 1-1
        assert self.mts.run("(- 1 (+ 2 3))") == 1-(2+3)
        self.assertAlmostEqual(self.mts.run("(- 1.1 1)"),(1.1-1))
class prim_mul(simple_test):
    def runTest(self):
        assert self.mts.run("(* 1 1)") == 1*1
        assert self.mts.run("(* 0 (* 2 3))") == 0*(2*3)
        self.assertAlmostEqual(self.mts.run("(* 10 (- 2.1 3))"), 10*(2.1-3))
class prim_div(simple_test):
    def runTest(self):
        assert self.mts.run("(/ 9 (+ 1 (- 3 1)))") == (9/(1+(3-1)))
        self.assertEqual(self.mts.run("(/ 100 3.0)"),100/3.0)
class prim_eq(simple_test):
    def runTest(self):
        assert self.mts.run("(= 1 1)") == True
        assert self.mts.run("(= 1.1 1)") == False
class prim_not(simple_test):
    def runTest(self):
        assert self.mts.run("(not (= 1 1))") == False
        assert self.mts.run("(not (= 1.1 1))") == True
class prim_lt(simple_test):
    def runTest(self):
        assert self.mts.run("(< 1 1.1)") == True
        assert self.mts.run("(< 1.1 1)") == False
class prim_gt(simple_test):
    def runTest(self):
        assert self.mts.run("(> 1 1.1)") == False
        assert self.mts.run("(> 1.1 1)") == True
class prim_le(simple_test):
    def runTest(self):
        assert self.mts.run("(<= 1 1.1)") == True
        assert self.mts.run("(<= 1.1 1.1)") == True
        assert self.mts.run("(<= 1.1 1)") == False
class prim_ge(simple_test):
    def runTest(self):
        assert self.mts.run("(>= 1 1.1)") == False
        assert self.mts.run("(>= 1.1 1.1)") == True
        assert self.mts.run("(>= 1.1 1)") == True
class prim_cons(simple_test):
    def runTest(self):
        assert self.mts.run("(cons 1 2)") == [1, 2]
        assert self.mts.run("(cons 1 (cons 2 3))") == [1, 2, 3]
class prim_list(simple_test):
    def runTest(self):
        assert self.mts.run("(list 5 (list 1 1) 2)") == [5, [1, 1], 2]
class prim_append(simple_test):
    def runTest(self):
        assert self.mts.run("(append 1 (list 2 3))") == [1, 2, 3]
        assert self.mts.run("(append (list 1 2) (cons 3 4))") == [1, 2, 3, 4]
class prim_car(simple_test):
    def runTest(self):
        assert self.mts.run("(car (list 5 (list 1 1) 2))") == 5
class prim_cdr(simple_test):
    def runTest(self):
        assert self.mts.run("(cdr (list 5 (list 1 1) 2))") == [[1, 1], 2]
class prim_null(simple_test):
    def runTest(self):
        self.mts.run("(define l (list 1 2))")
        assert self.mts.run("(null? l)") == False
        assert self.mts.run("(null? (cdr l))") == False
        assert self.mts.run("(null? (cdr (cdr l)))") == True
class prim_if(simple_test):
    def runTest(self):
        assert self.mts.run("(if (< 2 1) 10 11)") == 11
        assert self.mts.run("(if (< 1 2) 10 11)") == 10
        assert self.mts.run("(if (= 0 0) 20)") == 20
        assert self.mts.run("(if (= 0 1) 20)") == self.mts.nil
class prim_cond(simple_test):
    def runTest(self):
        self.mts.run("(define x -1)")
        assert self.mts.run("(cond ((< x 0) (- 0 x)) ((= x 0) 100) (else x))") == 1
        self.mts.run("(define x 0)")
        assert self.mts.run("(cond ((< x 0) (- 0 x)) ((= x 0) 100) (else x))") == 100
        self.mts.run("(define x 1)")
        assert self.mts.run("(cond ((< x 0) (- 0 x)) ((= x 0) 100) (else x))") == 1        
class prim_def(simple_test):
    def runTest(self):
        self.mts.run("(define kalle 3.14)")
        assert self.mts.run("(kalle)") == 3.14
        self.mts.run("(define olle (+ 1 1))")
        assert self.mts.run("(olle)") == 2
        self.mts.run("(define val 10)")
        self.mts.run("(define (factorial x) (if (= x 0) 1 (* x (factorial (- x 1)))))")
        assert self.mts.run("(factorial val)") == 3628800
        self.mts.run("(define (add x y) (define (worker x y) (+ x y)) (worker x y))")
        assert self.mts.run("(add 1 3)") == 1+3
        self.mts.run("(define (simple-adder x) (define val 4) (+ val x))")
        assert self.mts.run("(simple-adder 1)") == 4+1
class prim_lambda(simple_test):
    def runTest(self):
        self.mts.run("(define (adder val) (lambda(x) (+ x val)))")
        self.mts.run("(define add4 (adder 4))")
        assert self.mts.run("(add4 4)") == 8
        self.mts.run("(define (map f l) (if (not (null? l)) (cons (f (car l)) (map f (cdr l)))))")
        self.mts.run("(define l (list 1 2 3))")
        assert self.mts.run("(map (lambda(x) (* x x)) l)") == [1, 4, 9]
class prim_begin(simple_test):
    def runTest(self):
        self.mts.run("(define (foreach f l) (if (not (null? l)) (begin (f (car l)) (foreach f (cdr l)))))")
        self.mts.run("(define l (list 1 2 3))")
        print "\nThis test should now print:\n1\n2\n3\n--->"
        self.mts.run("(foreach display l)")
        print "<---"
class prim_let(simple_test):
    def runTest(self):
        assert self.mts.run("(let ((a (+ 1 1))(b 3)) (+ a b))") == 3+(1+1)
class prim_display_env(simple_test):
    def runTest(self):
        self.mts.run("(display-env)")
        
if __name__ == "__main__":
    tests = TestSuite()
    tests.addTest(prim_add())
    tests.addTest(prim_sub())
    tests.addTest(prim_mul())
    tests.addTest(prim_div())
    tests.addTest(prim_eq())
    tests.addTest(prim_gt())
    tests.addTest(prim_lt())
    tests.addTest(prim_ge())
    tests.addTest(prim_le())
    tests.addTest(prim_not())
    tests.addTest(prim_cons())
    tests.addTest(prim_list())
    tests.addTest(prim_append())
    tests.addTest(prim_car())
    tests.addTest(prim_cdr())
    tests.addTest(prim_null())
    tests.addTest(prim_if())
    tests.addTest(prim_cond())
    tests.addTest(prim_def())
    tests.addTest(prim_lambda())
    tests.addTest(prim_begin())
    tests.addTest(prim_let())
#    tests.addTest(prim_display_env())
    
    runner = TextTestRunner()
    runner.run(tests)
        

