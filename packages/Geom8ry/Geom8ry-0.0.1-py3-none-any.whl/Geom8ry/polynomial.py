from cmath import exp
from math import pi
from .dft import FFT,NthRootOfUnity
# from .idft import dft,NthRootOfUnity

class Polynomial:
    def __init__(self, listOfInt=None):
        if listOfInt is None:
            listOfInt = []
        self.listOfInt = listOfInt
    def __repr__(self):
        rep = ""
        for i in range(len(self.listOfInt)):
            rep += str(self.listOfInt[i]) + str('x^') + str(i) + str(' + ');
        rep = str.removesuffix(rep,'+ ')
        return rep
    def __add__(self, ply2):
        if len(self.listOfInt) != len(ply2.listOfInt):
            raise IndexError
        else:
            return Polynomial([self.listOfInt[i]+ply2.listOfInt[i] for i in range(len(self.listOfInt))])
    def __sub__(self, ply2):
        if len(self.listOfInt) != len(ply2.listOfInt):
            raise IndexError
        else:
            return Polynomial([self.listOfInt[i]-ply2.listOfInt[i] for i in range(len(self.listOfInt))])
    def __mul__(self, ply2):
        n = 1<<(len(self.listOfInt)+len(ply2.listOfInt)-2).bit_length()
        o = NthRootOfUnity(n)
        AT = FFT(self.listOfInt, o)
        BT = FFT(ply2.listOfInt, o)
        C = [AT[i]*BT[i] for i in range(n)]
        # nm = (len(self.listOfInt)+len(ply2.listOfInt)-1)
        D = [round((a/n).real) for a in FFT(C, o ** -1)]
        while len(D) > 0 and D[-1] == 0:
            del D[-1]
        return Polynomial(D)
# //==============================================================
# l = [1,2,3,4]
# p = Polynomial(l)
# l2 = [11,22,33,44]
# p2 = Polynomial(l2)
# print(p)
# print(p2)
# print(p+p2)
# print(p-p2)
# print(p*p2)