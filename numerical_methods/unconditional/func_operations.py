from sympy import Symbol, simplify, lambdify
import sympy
import math
from collections import OrderedDict
from one_dim_optimization import dihotomy_method, sven_method, gen_function_with_counter, Result



def i_loop(iter_count):
    while iter_count != 0:
        iter_count -= 1
        yield
    raise StopIteration

def vect_mod(**X):
    return math.sqrt(sum([x**2 for _, x in X.items()]))

def calc_func_vect(func_vect:dict, **args) -> dict:
    c_vect = {}
    for key, value in func_vect.items():
        if isinstance(value, Function):
            c_vect[key] = value(**args)
        else:
            c_vect[key] = value
    return c_vect

def one_dim_opt(func, e, opt_method=dihotomy_method):
    assert func.is_one_dim(), "Function is not one dimentional"
    arg_name = func.get_arguments()[0]
    @gen_function_with_counter
    def func_to_opt(x):
        kwarg = {arg_name:x}
        return func(**kwarg)
    l1, l2, l3 = sven_method(func=func_to_opt, start_x=3, step_h=0.3)
    result = opt_method(func_to_opt, l1, l3, e)
    return result.x

class Function:

    def result_formatting(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, sympy.Basic):
                if result.is_Integer:
                    return int(result)
                elif result.is_Float:
                    return float(result)
            return result
        return inner
    
    def __init__(self, expr):
        self._sp_expr = simplify(expr)
        self._arguments = self._sp_expr.free_symbols
        
    @result_formatting
    def __call__(self, **args):
        if isinstance(self._sp_expr, sympy.Number):
            return self._sp_expr
        assert len(args) <= len(self._arguments), "Wrong arguments count" 
        num_arguments = [(self._get_symbol_by_name(key), value) \
                        for key, value in args.items() if not isinstance(value, Function)]
        res_func = self._integrate(**args)
        if not res_func.is_Number:
            assert len(num_arguments) == len(res_func.free_symbols) 
            result = res_func.subs(num_arguments)
            return result
        else:
            return res_func 
            

            
    def __str__(self):
        return str(self._sp_expr)
        
    def __repr__(self):
        return str(self._sp_expr)

    def _integrate(self, **kwargs):
        """Return sympy function representation"""
        functors = [(self._get_symbol_by_name(key), value._sp_expr) \
                    for key, value in kwargs.items() if isinstance(value, Function)]
        num_arguments = [(self._get_symbol_by_name(key), value) \
                        for key, value in kwargs.items() if not isinstance(value, Function)]
        integr = self._sp_expr.subs(functors)
        integr = integr.subs(num_arguments)
        return integr

    def is_one_dim(self):
        return len(self._arguments) == 1

    def integrate(self, **kwargs):  
        integr = self._integrate(**kwargs)
        new_func = Function(integr)
        return new_func

    def get_arguments(self):
        return [str(arg) for arg in self._arguments]
        
    def _get_symbol_by_name(self, name:str) -> Symbol:
        s = [arg for arg in self._arguments if arg.name == name]
        assert len(s) > 0, "No such symbol"
        return s[0]
    
    def diff(self, sym_name, num=1):
        arg_symb = [symb for symb in self._arguments if symb.name == sym_name]
        assert len(arg_symb) > 0, "Wrong argument"
        arg = arg_symb[0]
        return self._sp_expr.diff(arg, num)
    
    def grad(self, num=1):
        diffs = [[symb.name, self._sp_expr.diff(symb, num)] for symb in self._arguments]
        gradient = {}
        for name, d in diffs:
            if d.is_Integer:
                gradient[name] = int(d)
            elif d.is_Float:
                gradient[name] = float(d)
            else:
                gradient[name] = Function(d)
        return gradient
    

if __name__ == "__main__":
    func = Function("x**2+3*y+2")
    num = func(x=5, y=6)
    num2 = func(x="x", y=Function("x+5"))
    d = func.diff('x')
    g = func.grad()
    print('ok')