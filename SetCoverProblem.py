
import numpy as np

class SetCover:
    def solve(self, rel_matrix, costs):
        print rel_matrix
        I = set() # satir indekslerini tutacak
        # Eklenebilecek eleman sayisi = n, o sutun icin cost = c
        # en buyuk n/c'yi bul
        i = 0
        while i<3:
            i+=1
            I_mat = np.array(list(I), dtype=np.int)
            print "Index matrisi, ", I_mat
            mask = np.ones([rel_matrix.shape[0]], dtype=np.bool)
            mask[I_mat] = False
            print "Maskelenmis satirlar, ", rel_matrix[mask]
            cost_per_piece = np.sum(rel_matrix[mask], axis=0, dtype=np.float) / costs
            print cost_per_piece
            greatest_index = np.argmax(cost_per_piece)
            col_greatest = np.where(rel_matrix[:,greatest_index]==True)
            print col_greatest
            for index in col_greatest:
                I.add(index[0])
            if len(I) == rel_matrix.shape[0]:
                break
        return len(I),np.array(list(I), dtype=np.bool)

class Utils:
    @staticmethod
    def getMinimumSetCover(matrix):
        print matrix
        mat_len = matrix.shape[0]
        indices = np.argwhere(matrix == 0)
        rel_matrix = np.zeros([indices.shape[0], mat_len*2], dtype=np.bool)
        for idx, index in enumerate(indices):
            row_index = index[0]
            col_index = index[1]
            rel_matrix[idx][row_index] = True
            rel_matrix[idx][col_index+mat_len] = True
        print 1./np.sum(rel_matrix, axis=0 )**2
        prob = SetCover()
        sol, sol_matrix = prob.solve(rel_matrix, np.ones(rel_matrix.shape[1]))
        
        return sol, sol_matrix[:mat_len], sol_matrix[mat_len:]

mat = np.array([0,1,1,1,0,0,0,1,1]).reshape([3,3])
print Utils.getMinimumSetCover(mat)