import numpy as np


class UnbalancedTransport(Exception):
    pass


class UnknownMethod(Exception):
    pass


class Utils:
    """ Satir/Sutun farki icin Utility sinifi(VAM Metodu) """
    @staticmethod
    def getRowDiff(matrix):
        temp = np.partition(matrix, 1, axis=1)
        return np.reshape(temp[:, 1] - temp[:, 0], [1, -1])

    @staticmethod
    def getColDiff(matrix):
        temp = np.partition(matrix, 1, axis=0)
        return np.reshape(temp[1] - temp[0], [1, -1])


class TransportProblem:

    def solve(self, road_cost, supply, demand, method='NWCorner'):
        # NumPy array yap
        rc = np.array(road_cost)
        s = np.array(supply)
        d = np.array(demand)
        allocs = None
        # Balanced mi Unbalanced mi?
        if np.sum(s) != np.sum(d):
            raise UnbalancedTransport()
        # Metod kontrolu
        if method == 'NWCorner':
            allocs = self._NWCorner(rc, s, d)
        elif method == 'LeastCost':
            allocs = self._LeastCost(rc, s, d)
        elif method == "VAM":
            allocs = self._VAM(rc, s, d)
        else:
            raise UnknownMethod()

        cost = np.multiply(allocs, rc)
        return cost, np.sum(cost)

    def _VAM(self, rc, s, d):
        rc = np.copy(rc)
        allocations = np.zeros_like(rc)
        lim = np.iinfo(rc.dtype).max
        while True:
            col_diff = Utils.getColDiff(rc)
            row_diff = Utils.getRowDiff(rc)
            con = np.array([col_diff, row_diff])
            highest_index = np.argmax(con)
            # maksimum indexs sutunda mi satirda mi
            if highest_index >= col_diff.shape[1]:
                # satirda
                # bu satirdaki en kucuk degeri bul
                highest_index -= col_diff.shape[1]
                index = np.argmin(rc[highest_index])
                sup = min(s[index], d[highest_index])
                allocations[highest_index][index] = sup
                s[index] -= sup
                d[highest_index] -= sup
            else:
                # sutunda
                # bu sutundaki en kucuk degeri bul
                index = np.argmin(rc[:, highest_index])
                sup = min(s[index], d[highest_index])
                allocations[highest_index][index] = sup
                s[index] -= sup
                d[highest_index] -= sup

            # burada sutun ve ya satirin sifir olma durumuna gore rc matrisi kucultulecek
            row_indices = s == 0
            rc[row_indices] = lim
            col_indices = d == 0
            rc[:, col_indices] = lim

            if np.sum(s) == 0:
                break

        return allocations

    def _LeastCost(self, rc, s, d):
        """
        O an costu en az olandan atama yap
        """
        rc = np.copy(rc)
        allocations = np.zeros_like(rc)
        limit_supply = s.shape[0]
        limit_demand = d.shape[0]
        while True:
            coords = np.argmin(rc)
            i = coords / limit_demand
            j = coords % limit_demand
            sup = min(s[i], d[j])  # arz ve talepten kucugunu al
            rc[i, j] = np.iinfo(rc.dtype).max
            allocations[i, j] = sup  # atama yap
            s[i] -= sup  # azalt
            d[j] -= sup  # azalt
            if np.sum(s) == 0:
                break
        return allocations

    def _NWCorner(self, rc, s, d):
        """
        Sol ust taraftan baslayip bitene kadar atama yap.
        Cozum bulur ama bulunan cozum genelde optimal degildir.
        Cunku amac sadece sol ust taraftan baslayarak 
        O anda mevcut olan talebi mevcut arzla doldurmaktir.
        RC matrisine dikkat edilmez.
        """
        # atamalar matrisi
        allocations = np.zeros_like(rc)
        limit_supply = s.shape[0] - 1
        limit_demand = d.shape[0] - 1
        i = 0
        j = 0  # Sol ust nokta
        while True:
            sup = min(s[i], d[j])  # arz ve talepten kucugunu al
            allocations[i, j] = sup  # atama yap
            s[i] -= sup  # azalt
            d[j] -= sup  # azalt
            if s[i] == 0:  # eger bu satirdaki arz bittiyse digerine gec
                i += 1
            if d[j] == 0:  # eger bu sutundaki talep bittiyse digerine gec
                j += 1
            if i > limit_supply or j > limit_demand:
                break
        return allocations


"""
Balanced Transportation

        A   B   C    Supply
1       2   7   5       200
2       3   4   2       300
3       5   4   7       500

Demand 200 400 400
"""

# Bu tabloyu uc ayri matris haline getirecegiz.

rc = [
    [2, 7, 5],
    [3, 4, 2],
    [5, 4, 7]
]

supply = [200, 300, 500]
demand = [200, 400, 400]

tp = TransportProblem()
print tp.solve(rc, supply, demand, method="VAM")
