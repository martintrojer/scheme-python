# Simple Scheme Interpreter
# Martin Trojer <martin.trojer@gmail.com>
#
# Very fragile to ill-formed input,
#  will give bizarre runtime errors instead of syntax / parse errors
# Currently only a subset of the language

import inspect
import pyparsing
import pdb
import pprint

class MTScheme:

    def getenv(self, name, env):
        for frame in env:
            if frame.has_key(name):
                return frame[name]
        raise Exception("Unbound '" + name +"'")    

    def inenv(self, name, env):
        for frame in env:
            if frame.has_key(name):
                return True
        return False

    def expand_env(self, new, old):
        res = [new]
        for frame in old:
            res.append(frame)
        return res
    
    def defenv(self, name, val, env):
        env[0][name] = val

    def isprim(self, name, env):
        return inspect.isfunction(self.getenv(name, env))

    def islazy(self, name, env):
        if self.isprim(name, env):
            return name in ['if', 'define', 'lambda', 'begin', 'let', 'cond']
        return False

    def isatom(self, name):
        return not (type(name) == list or type(name) == dict)

    def isnumber(self, name):
        return name.replace(".","").replace("-","").isdigit()

    def number(self, name):
        if "." in name:
            return float(name)
        else:
            return int(name)

    def _display(self, sexpr, env):
        print sexpr[0]
        return self.nil

    def _display_env(self, sexpr, env):
        pprint.pprint(env)
        return self.nil

    def _newline(self, sexpr, env):
        print "\n"
        return self.nil

    def _define(self, sexpr, env):
        name = ""
        args = []
        body = []
        if self.isatom(sexpr[0]):
            name = sexpr[0]
            body = sexpr[1:]
        else:
            name = sexpr[0][0]
            args = sexpr[0][1:]
            body = sexpr[1:]

#        pdb.set_trace()
        if len(args)==0:
            #defining a variable or lambda function
            #flag used to update current env (and not creating a new tmp env)
            self.def_mode = True
            res = self._eval(body[0], env)
            self.def_mode = False
            self.defenv(name, res, env)
        else:
            #defining a function (sugar version)
            self.defenv(name, [args, body], env)
            return self.nil

    def _begin(self, sexpr, env):
        res = False
        nenv = self.expand_env({}, env)
        for exp in sexpr:
            res = self._eval(exp,nenv)
        return res

    def _let(self, sexpr, env):
#        pdb.set_trace()
        nenv = self.expand_env({}, env)
        for exp in sexpr[0]:
            self._define(exp, nenv)
        return self._eval(sexpr[1],nenv)

    def _if(self, sexpr, env):
#        pdb.set_trace()
        if self._eval(sexpr[0],env):
            return self._eval(sexpr[1],env)
        elif len(sexpr)==3:
            return self._eval(sexpr[2],env)
        return self.nil

    def _cons(self, sexpr, env):
#        pdb.set_trace()
        def flatten(l):
            for e in l:
                if type(e) == list:
                    for i in flatten(e):
                        yield i
                else:
                    yield e                
        return list(flatten(sexpr))

    def _cond(self, sexpr, env):
#        pdb.set_trace()
        for exp in sexpr:
            if type(exp[0]) == str and exp[0]=="else":
                return self._eval(exp[1],env)
            elif self._eval(exp[0], env):
                return self._eval(exp[1],env)
        return self.nil
    
    def _apply(self, fn, args, env):
        if self.isprim(fn, env):
            #function to call?
            return self.getenv(fn,env)(self, args, env)
        elif self.isatom(self.getenv(fn, env)):
            #variable?
            return self.getenv(fn, env)
        else:
            #self-defined function
#            pdb.set_trace()
            if len(self.getenv(fn,env)[0]) != len(args):
                raise Exception("Wrong number of arguments '" + fn + "'")
            newenv = dict(zip(self.getenv(fn,env)[0], args))

            #Global flag to cover the case when we want define to go into the global env
            #There is probably a better solution for this
            if (self.def_mode):
                env.insert(0,newenv)
            else:
                nenv = self.expand_env(newenv, env)
                env = nenv

            #run the whole body
            body = self.getenv(fn,env)[1]
            res = self.nil
            for exp in body:
                res = self._eval(exp, env)

            return res

    def _eval(self, sexpr, env):
        if self.isatom(sexpr):
            if self.isnumber(sexpr):
                return self.number(sexpr)
            elif self.inenv(sexpr, env):
                return self.getenv(sexpr,env)
            else:
                return sexpr

        fn = sexpr[0]
        args = sexpr[1:]

        if not self.islazy(fn, env):
            args = map(lambda n: self._eval(n, env), args)
        if self.nil in args:
            #Terrible hack (I think)
#            pdb.set_trace()
            args.remove(self.nil)
        return self._apply(fn, args, env)

    def_mode = False
    nil = "nil"
    
    globs = {}
    globs['define'] = _define
    globs['lambda'] = lambda self, sexpr, env: [sexpr[0],sexpr[1:]]
    globs['display'] = _display
    globs['newline'] = _newline
    globs['begin'] = _begin
    globs['let'] = _let
    globs['if'] = _if
    globs['cond'] = _cond
    globs['cons'] = _cons
    globs['list'] = lambda self, sexpr, env: sexpr
    globs['append'] = _cons
    globs['car'] = lambda self, sexpr, env: sexpr[0][0]
    globs['cdr'] = lambda self, sexpr, env: sexpr[0][1:]
    globs['+'] = lambda self, sexpr, env: sexpr[0] + sexpr[1]
    globs['-'] = lambda self, sexpr, env: sexpr[0] - sexpr[1]
    globs['*'] = lambda self, sexpr, env: sexpr[0] * sexpr[1]
    globs['/'] = lambda self, sexpr, env: sexpr[0] / sexpr[1]
    globs['='] = lambda self, sexpr, env: sexpr[0] == sexpr[1]
    globs['>'] = lambda self, sexpr, env: sexpr[0] > sexpr[1]
    globs['<'] = lambda self, sexpr, env: sexpr[0] < sexpr[1]
    globs['>='] = lambda self, sexpr, env: sexpr[0] >= sexpr[1]
    globs['<='] = lambda self, sexpr, env: sexpr[0] <= sexpr[1]
    globs['not'] = lambda self, sexpr, env: not sexpr[0]
    globs['null?'] = lambda self, sexpr, env: len(sexpr[0])==0
    globs['display-env'] = _display_env

    global_env = [globs,]

    parser = pyparsing.nestedExpr()

    def run(self, expr_str):
        sexpr = []
        try:
            sexpr = self.parser.parseString(expr_str).asList()[0]
        except Exception as e:            
            print "Parse Error:", e
            return

        try:
            return self._eval(sexpr, self.global_env)
        except Exception as e:
            print e.args[0], type(e)
            return
        
if __name__ == "__main__":
    mts = MTScheme()

    while(True):
        exp_str = raw_input("MTScheme$ ")
        print mts.run(exp_str.strip())

