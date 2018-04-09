#from package1.subpack1.module_11 import *
from mpack.A import spam

def fun():
    print('fun() in test_m')
    print('<<<<<<<<')
    spam.fun()
    print('>>>>>>>>')

if __name__ == '__main__':
    fun()