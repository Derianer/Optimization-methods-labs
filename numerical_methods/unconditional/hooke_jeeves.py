import operator as op
try:
    from .func_operations import Function, one_dim_opt, calc_func_vect
except ImportError:
    from func_operations import Function, one_dim_opt, calc_func_vect





def vec_operation(operation, *vectors):
    return [operation(*x) for x in zip(*vectors)]

def calc_steps(X:dict, deltas_x):
    assert len(X) == len(deltas_x), "Wrong arguments"
    steps = {key:Function(f"{X[key]} + l*{deltas_x[key]}") for key in X.keys()}
    return steps

def i_loop(iter_count):
    while iter_count != 0:
        iter_count -= 1
        yield
    raise StopIteration
    
def hooke_jeeves_method(func, X:dict, deltas:list, e, a=2, iter_count = -1):
    if isinstance(func, str):
        func = Function(func) 
    assert len(X) == len(deltas)
    for k in i_loop(iter_count):
        f = func(**X)
        f_modif = f
        x_modif = X
        for d_key, delta in deltas.items():
            xmd = dict([(x_key,x - delta) if d_key == x_key else (x_key, x) for x_key, x in x_modif.items()])
            xpd = dict([(x_key,x + delta) if d_key == x_key else (x_key, x) for x_key, x in x_modif.items()])
            fmd = func(**xmd)
            fpd = func(**xpd)
            if fpd < f_modif:
                x_modif = xpd if fpd < fmd else xmd
                f_modif = fpd if fpd < fmd else fmd
            elif fmd < f_modif:
                x_modif = xpd if fpd < fmd else xmd
                f_modif = fpd if fpd < fmd else fmd
        if f_modif < f:
            d = dict([(key, value - X[key]) for key, value in x_modif.items()])
            steps = calc_steps(X, d)
            step_func = func.integrate(**steps)
            step = {'l':one_dim_opt(step_func, e=e/10)}
            X = calc_func_vect(steps, **step)
            # X = vec_operation(op.add, x_modif, vec_operation(lambda x: x*l, vec_operation(op.sub, x_modif, X)))
        else:
            count = 0
            for key, delta in deltas.items():
                if delta > e:
                    count += 1
                    deltas[key] = delta/a
            if count == 0:
                return X

                    
def test():
    # func = Function("8*x**2+4*x*y+5*x**2")
    func = Function("x**2+3*y**2-x+2*y")
    hooke_jeeves_method(func=func, X={'x':9, 'y':8}, deltas={'x':1, 'y':1}, e=0.1, a=2) 


if __name__ == "__main__":
    test()        


                    