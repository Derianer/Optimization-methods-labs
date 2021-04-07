from numerical_methods.unconditional.one_dim_optimization import sven_method, dihotomy_method, \
                                            bisection_method, golden_section_method, \
                                            fibonachi_method, gen_function_with_counter 

e1 = 0.1
e2 = 0.01

@gen_function_with_counter
def my_func(x):
    return round(pow(x,2) + 1, 8)

def show_result(result):
    print(f'{result.name}:')
    print(f'f(x) = {result.func_x}' 
            + f'\tx = {result.x}'  
            + f'\tL = {result.interval}'
            + f'\niteration count = {result.iter_count}'
            + f'\tcalculation count = {result.calc_count}'
            + f'\tE = {result.E}')
    print('\n')

def main():

    x1, x2, x3 = sven_method(func=my_func, start_x=2, step_h=0.3)
    print(f'Sven method results: [{x1}, {x2}, {x3}]\n')

    show_result(dihotomy_method(my_func, x1, x3, e1))

    show_result(dihotomy_method(my_func, x1, x3, e2))
    
    show_result(bisection_method(my_func, x1, x3, e1))

    show_result(bisection_method(my_func, x1, x3, e2))

    show_result(golden_section_method(my_func, x1, x3, e1))

    show_result(golden_section_method(my_func, x1, x3, e2))

    show_result(fibonachi_method(my_func, x1, x3, e1, e1/10))

    show_result(fibonachi_method(my_func, x1, x3, e2, e2/10))

if __name__ == "__main__":
    main()
