try:
    from .func_operations import Function, one_dim_opt, calc_func_vect, vect_mod, i_loop 
    from .newton_raphson import hessian_matrix 
except ImportError:
    from func_operations import Function, one_dim_opt, calc_func_vect, vect_mod, i_loop 
    from newton_raphson import hessian_matrix 

def calc_steps(X:dict, deltas_x):
    assert len(X) == len(deltas_x), "Wrong arguments"
    steps = {key:Function(f"{X[key]} + t*{deltas_x[key]}") for key in X.keys()}
    return steps

def calc_Hd(H, d):
    Hd = {}
    for h_key, h_value in H.items():
        Hd[h_key] = sum([h_value[d_key] * d[d_key] for d_key in d.keys()])
        # for v_key, v_value in h_value:
    return Hd

def scalar_mult(vect1, vect2):
    return sum(vect1[key] * vect2[key] for key in vect1.keys())

            
def compare_args(args1:dict, args2:dict, e):
    mod = vect_mod(**dict([(key, args1[key] - args2[key]) for key in args1.keys()]))
    if mod < e:
        return True
    else:
        return False
        

def f_calculation_formulas(func, d, **X):
    grad = func.grad()
    calc_grad = calc_func_vect(grad, **X)
    H = hessian_matrix(func) 
    Hd = calc_Hd(H, d)
    numerator = scalar_mult(d, calc_grad)
    denominator = scalar_mult(Hd, d) 
    res = -(numerator/denominator)
    return float(res)
    
def fletcher_rives(func, X, e1, e2, iter_count=-1):
    if isinstance(func, str):
        func = Function(func) 
    prev_X = None
    prev_d = None
    prev_B = None
    grad = func.grad()
    while i_loop(iter_count):
        calc_grad = calc_func_vect(grad, **X)
        if vect_mod(**calc_grad) < e1:
            return X
        d = None 
        if prev_X is None:
            d = {key:-value for key, value in calc_grad.items()} 
        else:
            _d = {key:-value for key, value in calc_grad.items()} 
            B = (vect_mod(**calc_func_vect(grad, **X)))**2/(vect_mod(**calc_func_vect(grad, **prev_X)))**2
            # B = dict([(key, (prev_B*value)) for key, value in prev_d])    
            d = dict([(key, (_d[key] + B*prev_d[key])) for key in _d.keys()])
            prev_B = B 
        step_form = calc_steps(X, d)
        step = f_calculation_formulas(func, d, **X)
        next_X = calc_func_vect(step_form,  **{'t': step})
        if compare_args(next_X, X, e2) and abs(func(**next_X) - func(**X)) < e2:
            return next_X 
        prev_X = X
        X = next_X
        prev_d = d
    return X
            
def test():
    fletcher_rives(Function("2*x**2 + x*y + y**2"), X={'x':0.5, 'y':1}, e1=0.1, e2=0.15)

if __name__ == "__main__":
    test()
