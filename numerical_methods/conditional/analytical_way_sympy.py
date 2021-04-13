import sympy as sp
import math
from collections import namedtuple

Result = namedtuple('Result',['x', 'y', 'f_res'])

def frank_wolf():
    start_x = [0, 0]
    e = 0.01
    x, y = sp.symbols('x y')
    Z = sp.symbols('Z')
    t = sp.symbols('t')
    args = [x, y]
    # f = x**2+3*y**2-x+2*y
    # term1 = x - y - 3 
    # term2 = 2*x+7*y - 15
    # term3 = 2*x + y + 3
    # terms = [term1, term2, term3]
    f = x**2+7*y**2-3*x-y
    term1 = x - 2*y - 4 
    term2 = 3*x+4*y - 12
    term3 = x
    terms = [term1, term2, term3]
    grad = [f.diff(symb) for symb in [x, y]]
    while True:
        calc_grad = [func.subs([[x, start_x[0]], [y, start_x[1]]]) for func in grad]
        F0 = calc_grad[0]*x+calc_grad[1]*y - Z
        # result = sp.linsolve([F0, term1, term3], x, y, Z )
        results = []
        used = []
        for term in terms:
            for i_term in terms:
                if term is not i_term and not i_term in used:
                    res = sp.linsolve([F0, term, i_term], x, y, Z )
                    if len(res) != 0:
                        results.append(res.args[0].args)
            used.append(term)
        min_res = min(results, key=lambda arg: arg[2])
    
        step1 = start_x[0] + t * (min_res[0] - start_x[0])
        step2 = start_x[1] + t * (min_res[1] - start_x[1])
        _f = f.subs([(x , step1), (y, step2)])
        d_f = _f.diff(t)
        _t = sp.solve(d_f, t)[0]
        new_x = [float(step.subs(t, _t)) for step in [step1, step2]]
        s = abs(sum([(x1 - x0)**2 for x1, x0 in zip(new_x, start_x)]))
        mod_x = math.sqrt(s) 
        if mod_x < e:
            print('Maximum is:')
            print(f'x = {new_x[0]}, y = {new_x[1]}')
            return new_x
        calc_f = f.subs([(x, float(new_x[0])), (y, float(new_x[1]))])
        print(f'x = {new_x[0]}, y = {new_x[1]}')
        start_x = new_x
    print('finish')

def analytical_corner_search():
    x, y = sp.symbols('x y')
    # f = -x**2-3*y**2+x-2*y
    # term1 = x - y - 3 
    # term2 = 2*x+7*y - 15
    # term3 = 2*x + y + 3
    # terms = [term1, term2, term3]
    f = -x**2-7*y**2+3*x+y
    term1 = x - 2*y - 4 
    term2 = 3*x+4*y - 12
    term3 = x
    terms = [term1, term2, term3]

    results = [term_solving(f, term, x, y) for term in terms]
    dxf1 = f.diff(x)
    dyf1 = f.diff(y)




    _x = sp.solve(dxf1, x)[0]
    _y = sp.solve(dyf1, y)[0]
    unc_res = Result(float(_x), float(_y), float(f.subs([[x, _x], [y, _y]])))
    print(f'x = {unc_res.x}, y = {unc_res.y}, f = {unc_res.f_res}')
    results.append(unc_res)

    H = sp.Matrix([[dxf1.diff(x), dxf1.diff(y)],\
                    [dyf1.diff(x), dyf1.diff(y)]])
    for row_num in range(H.rows):
        print(H.row(row_num))
    d1 = H[0] 
    d2 = H.det()
    extrem = None
    if d1 < 0 and d2 > 0:
        print("this is max")
        extrem = max  
    elif d1 > 0 and d2 > 0:
        print("this is min")
        extrem = min
    else:
        print("unknown")
        return 1
    extr = extrem(results, key=lambda res: res.f_res)
    print(f"extremum is {float(extr.f_res)}")
    print("finish")


def term_solving(f, term, x, y):
    try:
        y1 = sp.solve(term, y)[0]
    except:
        # y1 = sp.solve(term, y)
        y1 = x
    df1 = f.subs(y, y1)
    df1 = df1.diff(x)
    x1 = sp.solve(df1, x)[0]
    y1 = y1.subs(x, x1)
    f_res = f.subs([(x, x1), (y, y1)])
    # print(sp.Float(res)) 
    res = Result(float(x1), float(y1), float(f_res))
    print(f'x = {res.x}, y = {res.y}, f = {res.f_res}')
    return res


if __name__ == "__main__":
    analytical_corner_search()
    frank_wolf()