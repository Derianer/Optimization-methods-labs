import sympy as sp
from collections import namedtuple

Result = namedtuple('Result',['x', 'y', 'f_res'])

def frank_wolf():
    start_x = [0, 0]
    x, y = sp.symbols('x y')
    args = [x, y]
    f = -x**2-3*y**2+x-2*y
    term1 = x - y - 3 
    term2 = 2*x+7*y - 15
    term3 = 2*x + y + 3
    terms = [term1, term2, term3]
    grad = [f.diff(symb) for symb in [x, y]]
    calc_grad = [func.subs([[x, start_x[0]], [y, start_x[1]]]) for func in grad]
    F0 = calc_grad[0]*x+calc_grad[1]*y
    res = sp.linsolve([F0, term1, term2, term3], x, y)
    print('finish')

    




def analytical_corner_search():
    x, y = sp.symbols('x y')
    f = -x**2-3*y**2+x-2*y
    term1 = x - y - 3 
    term2 = 2*x+7*y - 15
    term3 = 2*x + y + 3
    terms = [term1, term2, term3]
    results = [term_solving(f, term, x, y) for term in terms]
    dxf1 = f.diff(x)
    dyf1 = f.diff(y)

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


    _x = sp.solve(dxf1, x)[0]
    _y = sp.solve(dyf1, y)[0]
    unc_res = Result(_x, _y, f.subs([[x, _x], [y, _y]]))
    results.append(unc_res)
    extr = extrem(results, key=lambda res: res.f_res)
    print(f"extremum is {float(extr.f_res)}")
    print("finish")


def term_solving(f, term, x, y):
    y1 = sp.solve(term, y)[0]
    df1 = f.subs(y, y1)
    df1 = df1.diff(x)
    x1 = sp.solve(df1, x)[0]
    y1 = y1.subs(x, x1)
    f_res = f.subs([(x, x1), (y, y1)])
    # print(sp.Float(res)) 
    res = Result(int(x1), int(y1), float(f_res))
    return res


if __name__ == "__main__":
    # analytical_corner_search()
    frank_wolf()