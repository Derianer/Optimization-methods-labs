try:
    from .func_operations import Function, i_loop, calc_func_vect, vect_mod 
except ImportError:
    from func_operations import Function, i_loop, calc_func_vect, vect_mod
from collections import OrderedDict


def hessian_matrix(func):
    gradient = func.grad()
    hessian = OrderedDict()
    # hessian = {}
    for arg, diff in gradient.items():
        hessian[arg] = OrderedDict()
        for arg_name in func.get_arguments():
            if isinstance(diff, Function):
                if arg_name in diff.get_arguments():
                    hessian[arg][arg_name] = diff.diff(arg_name)
                else: 
                    hessian[arg][arg_name] = 0
            elif isinstance(diff, (int, float)):
                hessian[arg][arg_name] = 0
    return hessian

def calc_hessian(hessian, **args):
    # c_hessian = {arg:calc_func_vect(grad, **args) \
    #              for arg, grad in hessian.items()}
    c_hessian = OrderedDict()
    for arg, grad in hessian.items():
        c_hessian[arg] = calc_func_vect(grad, **args)
    return c_hessian

def determinant(hessian:dict):
    if len(hessian.keys()) == 2:
        keys = [key for key in hessian.keys()]
        return (hessian[keys[0]][keys[0]] * hessian[keys[1]][keys[1]])\
               -(hessian[keys[0]][keys[1]] * hessian[keys[1]][keys[0]]) 
    else:
        det = []
        for i, minor in enumerate(get_minors(hessian, len(hessian))):
            sign = -1 if i % 2 else 1
            det.append(sign * minor[0] * determinant(minor[1]))
        return sum(det)

            

def get_minors(hessian, num=-1):
    minors = []
    for i_key in hessian.keys():
        for j_key in hessian.keys():
            if num == 0:
                return minors 
            num -= 1
            minor = OrderedDict()
            for m_key, m_value in hessian.items():
                if j_key != m_key:
                    minor[m_key] = OrderedDict([(key, value) for key, value in m_value.items() if key != j_key])
            minors.append((hessian[i_key][j_key], minor))
    return minors



def invert_hessian(hessian:dict):
    inv_hessian = {}
    for key, value in hessian.items():
        pass


def newton_raphson(func, X:dict, e1, e2, iter_count=-1):
    if isinstance(func, str):
        func = Function(func) 
    gradient = func.grad()
    hessian = hessian_matrix(func)
    for _ in i_loop(iter_count):
        calc_grad = calc_func_vect(gradient, **X)
        grad_mod = vect_mod(**calc_grad) 
        if grad_mod < e1:
            return X
        calc_hess = calc_hessian(hessian, **X)
        inv_hess = determinant(calc_hess)
        print('ok')
        return 0
        

def test():
    while True:
        newton_raphson(Function('x**2+3*y**2-x+2*y + z**2 + 2*z'), {'x':9, 'y':8, 'z':3}, 0.1, 0.01)
        # newton_raphson(Function('x**2+3*y**2-x+2*y'), {'x':9, 'y':8}, 0.1, 0.01)

if __name__ == "__main__":
    test()