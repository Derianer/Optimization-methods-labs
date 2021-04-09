from numerical_methods.unconditional.func_operations import Function
from numerical_methods.unconditional.gradient_descent import gradient_descent
from numerical_methods.unconditional.direct_coordinate_descent import direct_coordinate_descent 
from numerical_methods.unconditional.hooke_jeeves import hooke_jeeves_method 
from numerical_methods.unconditional.newton_raphson import newton_raphson

def iterate_gen(gen):
    res = yield from gen
    if res is not None:
        yield res

def iterate_method(method_gen):
    for i, res in enumerate(iterate_gen(method_gen)):
        print(f"Iteration №{i+1}: x = {res['x']}, y = {res['y']}")

def second_lab():
    func = Function('x**2+7*y**2-3*x-y')
    start_X = {'x':4, 'y': 3}
    deltas = {'x':1, 'y': 1}
    E1 = 0.01
    E2 = 0.015
    iteration_count = 2
    print('Gradient descent:')
    iterate_method(gradient_descent(func, X=start_X, e1=E1, e2=E2, iter_count=iteration_count))
    print('Hooke Jeeves:')
    iterate_method(hooke_jeeves_method(func, X=start_X, deltas=deltas, e=E1, iter_count=7))
    print('Direct gradien descent:')
    iterate_method(direct_coordinate_descent(func, X=start_X, e=E1, iter_count=iteration_count))
    print('Newton Raphson:')
    iterate_method(newton_raphson(func, X=start_X, e1=0, e2=E2, iter_count=iteration_count))

if __name__ == '__main__':
    second_lab()
    