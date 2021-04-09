try:
    from .func_operations import Function, one_dim_opt, calc_func_vect, vect_mod 
except ImportError:
    from func_operations import Function, one_dim_opt, calc_func_vect, vect_mod 
from collections import OrderedDict
import math



def calc_grad(gradient:dict, **args) -> dict:
    return calc_func_vect(gradient, **args)

def grad_mod(**X):
    return vect_mod(**X)

def calc_steps(X:dict, grad:dict):
    assert len(X) == len(grad), "Wrong arguments"
    steps = {key:Function(f"{X[key]} - l*{grad[key]}") for key in X.keys()}
    return steps

def compare_args(args1:dict, args2:dict, e):
    for key in args1.keys():
        if abs(args1[key] - args2[key]) >= e:
            return False
    return True

def gradient_descent(func, X:dict, e1, e2, iter_count=-1):
    if isinstance(func, str):
        func = Function(func) 
    gradient = func.grad()
    calculated_grad = calc_grad(gradient, **X)
    grad_module = grad_mod(**calculated_grad)
    if grad_module < e1: 
        return X
    while iter_count != 0: 
        steps = calc_steps(X, calculated_grad)
        step_func = func.integrate(**steps)
        step ={'l':one_dim_opt(step_func, e1/100)}
        args_with_step = calc_grad(steps, **step)
        func_with_step = func(**args_with_step)
        if compare_args(X, args_with_step, e2) and abs(func_with_step - func(**X)) <= e2:
            return args_with_step
        X = args_with_step
        calculated_grad = calc_grad(gradient, **X)
        grad_module = grad_mod(**calculated_grad)
        iter_count -= 1
        if grad_module < e1 or iter_count == 0: 
            return X
        yield X
    return X
    
def tests():
    gradient_descent("8*x**2+4*x*y+5*y**2", {'x':4, 'y':-3}, 0.1, 0.1, 2) 

if __name__ == "__main__":
    tests()