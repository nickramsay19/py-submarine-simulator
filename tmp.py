# Mutple, FieldTuple
# Field, tupdleif 

class ABSTRACT: # fake top inheritance ceiling that we will want to exclude from __mro__ loop
    pass

class A(ABSTRACT):
    a: str = 'a'

class B(A):
    b: str = 'b'

class C(B):
    c: str = 'c'

    '''def __new__(cls, *args, **kwargs):
        filter(lambda x: issubclass(x, ABSTRACT) and x != ABSTRACT, reversed(cls.__mro__)):
            print(t)'''

    def __init__(self, *args, **kwargs):
        for t in filter(lambda x: issubclass(x, ABSTRACT) and x != ABSTRACT, reversed(self.__class__.__mro__)):
            print(t)

c = C()



