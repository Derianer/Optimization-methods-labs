try:
    from .func_operations import Function, one_dim_opt, calc_func_vect, vect_mod 
except ImportError:
    from func_operations import Function, one_dim_opt, calc_func_vect, vect_mod 
from collections import OrderedDict
import math



def nelder_mid(func, tops:list, e=0.01, alpha=1, beta=0.5, gamma=2):
    if isinstance(func, str):
        func = Function(func) 
    while True:
        n = len(tops[0])
        sort_tops = sorted(tops, key=lambda x: func(**x))
        best_point = sort_tops[0] 
        worst_point = sort_tops[-1] 
        second_worst_point = sort_tops[-2]
        args_sum = {} 
        for key in tops[0].keys():
            args_sum[key] = 0
        for top in tops:
            if top is not worst_point:
                for key in top:
                    args_sum[key] += top[key]
        weight_center = {key:(value/(n)) for key, value in args_sum.items()}
        sigma = math.sqrt(sum([(func(**x) - func(**weight_center))**2 for x in tops])/(n+1))
        if sigma <= e:
            return best_point
        else:
            # reflect = weight_center + alpha*(weight_center - worst_point)
            reflect = {key:(weight_center[key] + alpha*(weight_center[key] - worst_point[key])) for key in weight_center.keys()}
            tops.remove(worst_point)
            if func(**reflect) <= func(**best_point):
                stretch = {key:(weight_center[key] + gamma * (reflect[key] - weight_center[key])) for key in weight_center.keys()}
                if func(**stretch) < func(**best_point):
                    tops.append(stretch)
                else:
                    tops.append(reflect)
            elif func(**second_worst_point) < func(**reflect) and func(**reflect) <= func(**worst_point):
                compression = {key:(weight_center[key] + beta*(worst_point[key] - weight_center[key])) for key in weight_center.keys()}
                tops.append(compression)
            elif func(**best_point) < func(**reflect) and func(**reflect) <= func(**second_worst_point):
                tops.append(reflect)
            elif func(**reflect) > func(**worst_point):
                new_tops = []
                tops.append(worst_point)
                for top in tops:
                    new_top = {key:(best_point[key] + 0.5*(arg - best_point[key])) for key, arg in top.items()}
                    # new_top = {}
                    # for key in top.keys():
                    #     s = 0.5*(top[key] - best_point[key])
                    #     new_top[key] = top[key] + s
                    new_tops.append(new_top)
                tops = new_tops
            
            
                
def test():
    tops = [{'x':8, 'y':9}, {'x':10, 'y':11}, {'x':8 ,'y':11}]
    nelder_mid(Function("4*(x - 5)**2 + (y - 6)**2"), tops=tops, e=0.2)

                
if __name__ == "__main__":
    test()
