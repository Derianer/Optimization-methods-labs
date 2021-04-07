import math
import collections
Result = collections.namedtuple('Result', ['func_x', 'x', \
                                'interval', 'iter_count', 'calc_count', 'name', 'E'])

ROUND_NUM = 8 
RES_ROUND = 4
ACCURACY = (1/(pow(10, int(ROUND_NUM/2))))/2

def to_standard_call(generator):
    generator = prepare_gen(generator)
    def iterate(*args):
        try:
            if len(args) != 0:
                result = generator.send(args)
                next(generator)
                return result
            else:
                result = generator.throw(StopIteration)
                return result
        except StopIteration as error:
            return error.value
    return iterate

def gen_function_with_counter(func):
    def with_counter(number_of_calculations=None):
        counter = 0
        while True:
            try:
                args = yield 
                res = func(*args)
                yield res 
                counter += 1
                if number_of_calculations is not None:
                    if counter > number_of_calculations:
                        raise StopIteration
            except StopIteration:
                return counter
    return with_counter

def prepare_gen(generator, number_of_calculations=None):
    gen = generator(number_of_calculations)
    next(gen)
    return gen
                

def sven_method(func, start_x, step_h):
    """Find unimodality interval"""
    func = to_standard_call(func)
    res1 = func(start_x + step_h)
    res2 = func(start_x - step_h)
    if  res1 > res2:
        step_h = -step_h
    next_x = start_x + step_h
    prev_x = start_x - step_h
    f_next = func(next_x)
    f_start = func(start_x)
    while(f_next < f_start):
        prev_x = start_x
        start_x = next_x
        step_h = 2*step_h
        next_x = round(next_x + step_h, ROUND_NUM)
        f_next = func(next_x)
        f_start = func(start_x)
    return sorted([next_x, start_x, prev_x])

def dihotomy_method(func, a, b, e) -> Result:
    func = to_standard_call(func)
    accur = e/100
    diff_const = e/10
    iter_count = 0 
    while abs(round(a - b, ROUND_NUM)) > e:
        if  math.isclose(abs(a-b), e, abs_tol=accur): 
            break
        iter_count += 1
        """stage 3"""
        a_b = abs(a-b)
        _a_b = a + b
        y = round((a + b - diff_const)/2, ROUND_NUM)
        z = round((a + b + diff_const)/2, ROUND_NUM)
        """stage 4"""
        func_y = func(y)
        func_z = func(z)
        if func_y <= func_z:
            b = z
        else:
            a = y
    """stage 5"""
    x = round((a + b)/2, ROUND_NUM)
    result = func(x)
    N = func()
    return Result(round(result, RES_ROUND), round(x, RES_ROUND), \
        [round(a, RES_ROUND), round(b, RES_ROUND)], iter_count, N, 'Dihotomy', e) 

def bisection_method(func, a, b, e):
    func = to_standard_call(func)
    iter_count = 0
    """stage 3"""
    x_mid = round((a + b)/2, ROUND_NUM) 
    L = round(abs(b - a), ROUND_NUM)
    while L > e:
        iter_count += 1
        """stage 4"""
        y = round(a + L/4, ROUND_NUM) 
        z = round(b - L/4, ROUND_NUM)
        """stage 5"""
        func_x_mid = func(x_mid)
        func_y = func(y)
        if func_y < func_x_mid:
            b = x_mid 
            x_mid = y
        else:
            """stage 6"""
            func_z = func(z)
            if func_z < func_x_mid:
                a = x_mid
                x_mid = z
            else:
                a = y
                b = z
        """stage 7"""
        L = abs(round(b - a, ROUND_NUM))
    N = func()
    return Result(round(func_x_mid, RES_ROUND), round(x_mid, RES_ROUND), \
        [round(a, RES_ROUND), round(b, RES_ROUND)],iter_count, N, 'Bisection', e)

def golden_section_method(func, a, b, e):
    GOLDEN_NUM = round((3 - pow(5,1/2))/2, ROUND_NUM)
    iter_count = 0
    func = to_standard_call(func)
    """stage 3"""
    y = round(a + GOLDEN_NUM * (b - a), ROUND_NUM)
    z = round(a + b - y, ROUND_NUM)
    delta = abs(a - b)
    """stage 4"""
    func_y = func(y)
    func_z = func(z)
    while delta > e:
        """stage 5"""
        if func_y <= func_z:
            b = z
            z = y
            y = round(a + b - y, ROUND_NUM)
            func_z = func_y
            func_y = func(y)
        else:
            a = y
            y = z
            z = round(a + b - z, ROUND_NUM)
            func_y = func_z
            func_z = func(z)
        """stage 6"""
        delta = abs(round(a - b, ROUND_NUM))
        iter_count += 1
    x_mid = (a + b)/2
    func_x_mid = func(x_mid)
    N = func()
    return Result(round(func_x_mid, RES_ROUND), round(x_mid, RES_ROUND), \
        [round(a, RES_ROUND), round(b, RES_ROUND)],iter_count, N, "Golden", e)

def fibonachi_numbers():
    a = 0
    b = 1
    yield b
    while True:
        a = a + b
        a, b = b, a
        yield b

def fibonachi_method(func, a, b, e, e_const):
    func = to_standard_call(func)
    fibonachi_gen = fibonachi_numbers()
    fibonachi_sequense = []
    L = abs(round(a - b, ROUND_NUM))
    """stage 2"""
    F_num = round(L/e, 3)
    for fib_num in fibonachi_gen:
        fibonachi_sequense.append(fib_num)
        if fib_num >= F_num:
            break
    """stage 4"""
    N = len(fibonachi_sequense) - 1
    y = round(a + (round(fibonachi_sequense[N-2]/fibonachi_sequense[N], ROUND_NUM))*round(b - a, ROUND_NUM), ROUND_NUM)
    z = round(a + (round(fibonachi_sequense[N-1]/fibonachi_sequense[N], ROUND_NUM))*round(b - a, ROUND_NUM), ROUND_NUM)
    """stage 5"""
    func_y = func(y)
    func_z = func(z)
    for i in range(0,(N-3)):
        """stage 6"""
        if func_y <= func_z:
            b = z
            z = y
            y = round(a + (round(fibonachi_sequense[N-i-3]/fibonachi_sequense[N-i-1], ROUND_NUM))*round(b - a, ROUND_NUM), ROUND_NUM)
            func_z = func_y
            func_y = func(y)
        else:
            a = y
            y = z
            z = round(a + (round(fibonachi_sequense[N-i-2]/fibonachi_sequense[N-i-1], ROUND_NUM))*round(b - a, ROUND_NUM), ROUND_NUM)
            func_y = func_z
            func_z = func(z)
    """stage 7"""
    y = z = (a + b)/2
    z = y + e_const
    func_y = func(y)
    func_z = func(z)
    if func_y <= func_z:
        b = z
    else:
        a = y
    x = (a + b)/2
    func_x = func(x)
    calc_count = func()
    return Result(round(func_x, RES_ROUND), round(x, RES_ROUND), \
        [round(a, RES_ROUND), round(b, RES_ROUND)],N+1 , calc_count, 'Fibonachi', e)