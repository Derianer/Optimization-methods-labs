try:
    from .func_operations import Function, vect_mod, one_dim_opt, i_loop, calc_func_vect, vect_mod 
except ImportError:
    from func_operations import Function, vect_mod, one_dim_opt, i_loop, calc_func_vect, vect_mod
from collections import OrderedDict
import random
random.seed(100)


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
    elif len(hessian.keys()) == 1:
        return hessian.popitem()[1].popitem()[1]
    else:
        det = []
        det_t = []
        alg_comp = alg_complement(hessian, len(hessian))
        for i_key, i_value in hessian.items():
            for j_key, j_value in i_value.items():
                det_t.append(alg_comp[i_key][j_key] * j_value)
        
        for i_comp in alg_comp.values():
            for j_comp in i_comp.values():
                det.append(j_comp) 
        return sum(det_t)

def alg_complement(hessian, num=-1):
        alg_comp = OrderedDict()
        minors = get_minors(hessian, num)
        for i, (m_key, m_value) in enumerate(minors.items()):
            alg_comp[m_key] = OrderedDict()
            for j, (key, minor) in enumerate(m_value.items()):
                if num == 0:
                    alg_comp.pop(m_key)
                    return alg_comp
                sign = 1 if ((i+1)+(j+1))%2 == 0 else -1
                det = determinant(minor)
                alg_comp[m_key][key] = (sign * det)
        return alg_comp
        

def get_minors(hessian, num=-1):
    minors = OrderedDict()
    for i_key in hessian.keys():
        minors[i_key] = OrderedDict()
        for j_key in hessian.keys():
            if num == 0:
                minors.pop(i_key)
                return minors 
            num -= 1
            minor = OrderedDict()
            for m_key, m_value in hessian.items():
                if i_key != m_key:
                    minor[m_key] = OrderedDict([(key, value) for key, value in m_value.items() if key != j_key])
            minors[i_key][j_key] = minor
    return minors

def transp_hessian(hessian):
    t_hess = OrderedDict()
    for i_key in hessian.keys():
        t_hess[i_key] = OrderedDict()
        for j_key in hessian.keys():
            t_hess[i_key][j_key] = hessian[j_key][i_key]
    return t_hess
            

def mul_hessian(hessian:OrderedDict, num):
    mult_hess = OrderedDict()
    for key, value in hessian.items():
        mult_hess[key] = OrderedDict()
        for i_key, arg in value.items():
            mult_hess[key][i_key] = arg * num
    return mult_hess

def mult_hess_grad(hessian, gradient):
    mult_matr = OrderedDict()
    for key, value in hessian.items():
        mult_matr[key] = sum([-num * gradient[g_key] for g_key, num in value.items()])
    return mult_matr
            
def corner_minors(hessian:OrderedDict):
    minors = []
    for minor_num in range(len(hessian)):
        minor = OrderedDict()
        for i, (i_key, i_value) in enumerate(hessian.items()):
            if i <= minor_num:
                minor[i_key] = OrderedDict()
                for j, (j_key, j_value) in enumerate(i_value.items()):
                    if j <= minor_num:
                        minor[i_key][j_key] = j_value
        minors.append(determinant(minor))
    return minors
                        

def calc_steps(X:dict, deltas_x):
    assert len(X) == len(deltas_x), "Wrong arguments"
    steps = {key:Function(f"{X[key]} + t*{deltas_x[key]}") for key in X.keys()}
    return steps

def invert_hessian(hessian:dict):
    determ = determinant(hessian)
    t_hess = transp_hessian(hessian)
    alg_comp = alg_complement(t_hess)
    inv_hessian = mul_hessian(alg_comp, 1/determ)
    return inv_hessian


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
        inv_hess = invert_hessian(hessian)
        calc_inv_hess = calc_hessian(inv_hess, **X)
        c_minors = corner_minors(calc_inv_hess)
        if all([minor > 0 for minor in c_minors]):
           d = mult_hess_grad(calc_inv_hess, calc_grad) 
        else:
            d = calc_grad
        steps = calc_steps(X, d) 
        integr_func = func.integrate(**steps)
        opt_step = one_dim_opt(integr_func, 0.001)
        new_X = calc_func_vect(steps, **{'t': opt_step})
        cond1 = abs(func(**X) - func(**new_X))
        cond2 = abs(vect_mod(**X) - vect_mod(**new_X)) 
        if  cond1 <= e2 and \
            cond2 <= e2: 
           return new_X
        X = new_X
        yield X
    return X
        

def test():
    while True:
        newton_raphson(Function('2*x**2+x*y+y**2'), {'x':0.5, 'y':1}, 0.1, 0.15, iter_count=10)
        # newton_raphson(Function('x**2+3*y**2-x+2*y'), {'x':9, 'y':8}, 0.1, 0.01)

if __name__ == "__main__":
    test()