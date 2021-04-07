try:
    from .func_operations import Function, i_loop, calc_func_vect 
except ImportError:
    from func_operations import Function, i_loop, calc_func_vect 


def hessian_matrix(func):
    gradient = func.grad()
    hessian = {}
    for arg, diff in gradient.items():
        if isinstance(diff, Function):
            hessian[arg] = diff.grad()
        elif isinstance(diff, (int, float)):
            hessian[arg] = 0
    return hessian

def calc_hessian(hessian, **args):
    c_hessian = {arg:calc_func_vect(grad, **args) \
                 for arg, grad in hessian.items()}
    return c_hessian

def newton_raphson(func, X:dict, e1, e2, iter_count=-1):
    if isinstance(func, str):
        func = Function(func) 
    gradient = func.grad()
    hessian = hessian_matrix(func)
    for _ in i_loop:
        calc_grad = calc_func_vect(gradient, **X)
        if calc_grad < e1:
            return X
        

        