try:
    from .func_operations import Function, one_dim_opt_fibonachi, one_dim_opt_pauell, one_dim_opt_golden, vect_mod
except ImportError:
    from func_operations import Function, one_dim_opt_fibonachi, one_dim_opt_pauell, one_dim_opt_golden, vect_mod


def i_loop(iter_count):
    while iter_count != 0:
        iter_count -= 1
        yield
    raise StopIteration

def integrate_args_to_func(func, **kwargs):
    integrated = {key:func.integrate(**{key:value}) for key, value in kwargs.items()}
    return integrated


def direct_coordinate_descent(func, X:dict, e, opt_method_name='Pauell', iter_count=-1):
    if isinstance(func, str):
        func = Function(func) 
    for _ in i_loop(iter_count):
        # integrated = integrate_args_to_func(func, **X)
        new_X = {}
        for key in X.keys():
            integrated = func.integrate(**{key:X[key]})
            if  opt_method_name == 'Pauell':
                new_X[integrated.get_arguments()[0]] = one_dim_opt_pauell(integrated, e, e)
            elif opt_method_name == 'Golden':
                new_X[integrated.get_arguments()[0]] = one_dim_opt_golden(integrated, e/10, e/100)
        # new_X = {key:one_dim_opt(value, e/10) for key, value in integrated.items()}
        delta = {key:abs(X[key] - new_X[key]) for key in X.keys()}
        X = new_X 
        if vect_mod(**delta) < e:
           return X 
        yield X
    return X


def test():
    direct_coordinate_descent(Function('x**2+3*y**2-x+2*y'), {'x':9, 'y':8}, 0.1)

if __name__ == "__main__":
    test()