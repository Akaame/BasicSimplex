
import numpy as np


class SimplexSolver:
    def solve(self, a, b, c):
        a = np.array(a) # Numpy Arrayine donustur
        b = np.array(b).reshape([-1,1]) # b'yi iki boyutlu yap 
        s = np.eye(a.shape[0]) # Hepsinin <= esitligine sahip oldugunu dusunuyoruz
        # slack variablelardan olusan bir array olustrudk
        a = np.hstack((a, s)) # Videodaki matris haline getirmeyi hedefliyoruz
        # slack variablelari ekledik
        a = np.hstack((a, b)) # limit arrayini ekleyelim
        print "Ust kisim: ", a
        c = -1 * np.array(c) # katsayi matrisimizi negatif yapalim
        s_g = np.zeros([a.shape[0]+1]) # a.shape kadar slack variable + sag alt kose
        c = np.hstack((c, s_g)) # matrisin en alt satiri
        print "Alt kisim: ", c
        mat = np.vstack((a,c)) # ust satirla alt satiri birbirine ekleyelim
        print "Son hali: ", mat

        while True:
            # C satiri icinden en kucugu sec matrisin en alt satiri son eleman haric
            c_index = np.argmin(mat[-1,:-1])
            print "En kucuk elemana sahip sutunun indeksi: ", c_index
            # en kucuk olan indekse karsilik gelen sutunu al A'dan
            col = mat[:-1, c_index]
            print "O sutun: ", col
            # Hedef sabitleri bu sutuna bol
            divs = mat[:-1,-1] / col
            print "Hedef siniri sutunun degerlerine bol Pivot belirleme icin: ", divs
            # en kucuk olani al(Pivot)
            pivot_index = np.argmin(divs)
            pivot = col[pivot_index]
            print "Pivotun indeksi ve kendisi: ", pivot_index, pivot
            # 1 / pivot 
            mat[pivot_index,:] /= pivot
            print "Pivot satirinin degistirilmesinden sonra Matris: ", mat
            ## Bu sutunu "Matris Satir islemleri" vasitasiyla sifirlamamiz lazim
            # Bu satir haric diger satirlari alalim
            indices = np.ones(mat.shape[0], dtype=bool)
            indices[pivot_index] = False
            # Her satir icin gerekli carpim katsayisini hesaplayalim
            coeffs = -mat[indices][:,c_index].T.reshape([-1,1])
            row = mat[pivot_index].reshape([-1,1]).T
            # Matrisi guncelleyelim.
            mat[indices] = mat[indices] + coeffs * row
            print "Matrisin guncellenmis hali: ", mat
            # Bu dongu en alt satir pozitif olana kadar surecek.
            if not np.any([mat[-1]<0]):
                break
        # birim vektor iceremeyen sutunlar haricinde her degisken hedefte bir degere esit olacak
        # sutunlarin uzunluklarini alalim
        lens = np.linalg.norm(mat,axis=0) # Uzunluklari bul
        print "Sutun uzunluklari: ", lens
        unit_indices = np.argwhere(lens==1.) # Birim matrislerin indeksleri
        print "Birim matrislerin indeksleri: ", unit_indices 
        results = [0 for i in unit_indices]
        for index in unit_indices:
            # Birim matrisler icinde 1 olan satirin indeksini bul
            col = mat[:,index]
            one_index = np.argwhere(col==1.) # 
            print "Bir olan satirin indeksi", one_index[0][0]
            results[index[0]] = mat[one_index[0][0],-1]
        return results # 6, 4, 8


""" 
Videodaki problem:
Maksimize 8x + 6y 
2x + 5y <= 40
3x + 3y <= 30
8x + 4y <= 64
x >= 0
y >= 0
c = [8, 6]
a = [[2, 5], [3, 3], [8, 4]]
b = [40, 30, 64]
"""

c = [8, 6]
a = [[2, 5], [3, 3], [8, 4]]
b = [40, 30, 64]

ss = SimplexSolver()

print ss.solve(a, b, c)
