
import numpy as np
from simpleai.search import backtrack, CspProblem
def nonequal_constr(variables, values):
    return len(values) == len(set(values))

class Utils:
    @staticmethod
    def matchMatrix(matrix):
        matrix = np.array(matrix, dtype=int)
        zero_indices = np.argwhere(matrix==0)
        print zero_indices
        variables = list(np.unique(zero_indices[:,0]))

        domains = {}
        for v in variables:
            domains[v] = list( zero_indices[zero_indices[:,0]==v][:,1] )
        print domains
        constraints = [[variables, nonequal_constr]]

        csp = CspProblem(variables, domains, constraints)
        result = backtrack(csp)
        return result
        


mat = np.array([1,0,0,1,0,1,0,1,1]).reshape([3,3])
print Utils.matchMatrix(mat)