
import numpy as np
import SetCoverProblem as scp

class AssignmentProblemSolver:
    def solve(self, matrix):
        """ 
        Verilen matris icin Assignment Problemi coz.
        Cozum icin Set Cover Destekli Hungarian Method kullan
        Soft versiyon
        """
        # Asama 1
        # Matrisin her satirindan o satirdaki en kucuk elemani cikar
        row_min = np.min(matrix, axis = 1)
        matrix = (matrix.T - row_min).T
        
        # Asama 2
        # Matrisin her sutunundan o sutundaki en kucuk elemani cikar 
        col_min = np.min(matrix, axis = 0)
        matrix -= col_min

        print "Matrixin yeni hali: ", matrix
        
        # Asama 3
        while True:
            print "Asama 3 Baslangici"
            cover, row_indices, col_indices = scp.Utils.getMinimumSetCover(matrix)
            # Row ve col indislerden "cover matrix" olustur."
            # Cover matrisin true oldugu yerlerde matrisi uzeri cizilmistir.
            print "------------------"
            cover_matrix = np.zeros_like(matrix, dtype=np.bool)
            cover_matrix[row_indices] = True
            cover_matrix[:, col_indices] = True
            # Sifirlarin uzerini orten cizgileri tutan cover matrisini olustur
            print "Cizgi sayisi: ", cover
            print "Cizgi matrisi: ", cover_matrix
        
            if cover == matrix.shape[0]: # Cizgi sayisi matrisin satir sayisina esitse cevap bulundu
                # asama 3.1: Iyi senaryo
                print "Asama 3.1 Baslangici"
                return matrix # TODO eslestirme yap
            else: # Degilse asil algoritma basliyor.
                print "Asama 3.2 Baslangici"
                # TODO
                smallest =  np.min(matrix[cover_matrix==False])
                print "Matrisin ilk hali", matrix
                print smallest
                # Uzeri cizilmemis yerlerdeki en kucuk degeri
                print matrix[row_indices]
                print matrix[:, col_indices]
                # Uzeri cizilmemis satirlardan cikar
                # uzeri cizilmemis satirlari bulmak icin:
                mask = np.ones(matrix.shape[0], dtype=np.bool)
                mask[row_indices] = False
                matrix[mask] -= smallest
                print "Matrisin son hali", matrix
                # Uzeri cizilmis sutunlara ekle
                matrix[:, col_indices] += smallest
                
aps = AssignmentProblemSolver()
# Iyi senaryo
"""
mat = np.array([250, 400, 350, 400, 600, 350, 200, 400, 250]).reshape([3,3])
print aps.solve(mat)
"""
# Kotu senaryo
# http://www.math.harvard.edu/archive/20_spring_05/handouts/assignment_overheads.pdf
mat = np.array([90, 75, 75, 80, 35, 85, 55, 65, 125, 95, 90, 105, 45, 110, 95, 115]).reshape([4,4])
print aps.solve(mat)