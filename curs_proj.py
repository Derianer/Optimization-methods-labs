import json
from numerical_methods.unconditional.func_operations import Function
from numerical_methods.unconditional.gradient_descent import gradient_descent
from numerical_methods.unconditional.direct_coordinate_descent import direct_coordinate_descent 
from numerical_methods.unconditional.hooke_jeeves import hooke_jeeves_method 
from numerical_methods.unconditional.newton_raphson import newton_raphson
from numerical_methods.unconditional.nelder_mid import nelder_mid 
from numerical_methods.unconditional.fletcher_rives import fletcher_rives
from numerical_methods.unconditional.one_dim_optimization import pauell_method, fibonachi_method, golden_section_method

def read_json():
    data = None
    with open("optimization_setting.json", "r") as file:
        data = json.load(file)
    return data



def iterate_gen(gen):
    res = yield from gen
    if res is not None:
        yield res

def iterate_method(method_gen):
    for i, res in enumerate(iterate_gen(method_gen)):
        print(f"Iteration №{i+1}: x = {res['x']}, y = {res['y']}")

def curs_project():

    data = read_json()
    function = data["function"]
    dgd_settings = data["direct_gradinet_descent_settings"]
    nm_settings = data["nelder_mid_settings"]
    hj_settings = data["hooke_jeeves_settings"]
    fgd_settings = data["fastest_gradient_descent_settings"]
    fr_settings = data["fletcher_rives_settings"]
    func = Function(function)

    if dgd_settings["enable"] == True:
        print(" ")
        print('Direct gradien descent with Pauell:')
        iterate_method(direct_coordinate_descent(func, X=dgd_settings["start_X"], \
                        e=dgd_settings["e"], iter_count=dgd_settings["iteration_count"],\
                        opt_method_name="Pauell"))


    if dgd_settings["enable"] == True:
        print(" ")
        print('Direct gradien descent with golden section:')
        iterate_method(direct_coordinate_descent(func, X=dgd_settings["start_X"], \
                        e=dgd_settings["e"], iter_count=dgd_settings["iteration_count"], \
                        opt_method_name="Golden"))

    if nm_settings["enable"] == True:
        print(" ")
        print('Nelder-Mid')
        iterate_method(nelder_mid(func, tops=nm_settings["tops"], e=nm_settings["e"], \
                        alpha=nm_settings["alpha"], beta=nm_settings["beta"], gamma=nm_settings["gamma"]))

    if hj_settings["enable"] == True:
        print(" ")
        print("Hooke Jeeves")
        iterate_method(hooke_jeeves_method(func, X=hj_settings["start_X"], \
                        deltas=hj_settings["deltas"], e=hj_settings["e"]))

    if fgd_settings["enable"] == True:
        print(" ")
        print("Fastest gradient descent")
        iterate_method(gradient_descent(func, X=fgd_settings["start_X"], e1=fgd_settings["e1"],\
                                        e2=fgd_settings["e2"]))

    if fgd_settings["enable"] == True:
        print(" ")
        print("Fletcher Rives")
        iterate_method(fletcher_rives(func, X=fr_settings["start_X"], e1=fr_settings["e1"],\
                                        e2=fr_settings["e2"]))

if __name__ == "__main__":
    curs_project()

    
    

    # func = Function('(x-1)**2 + (y**2 - 3)')
    # start_X = {'x':3, 'y': 4}
    # tops = [{'x':8, 'y':9}, {'x':10, 'y':11}, {'x':8 ,'y':11}]
    # deltas = {'x':1, 'y': 1}
    # E1 = 0.01
    # E2 = 0.015
    # iteration_count = -1