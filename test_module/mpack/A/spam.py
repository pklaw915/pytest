# to import grok in the same package
#import grok                     # Error (not found)
#from mpack.A import grok        # OK, absolute
from . import grok             # OK, relative, better

# to import foo in a sub package
from .subA import foo

# to import bar in a neighbor package
from ..B import bar

def fun():
    print("func in mpack.A.spam")
    print('<<<<<<<<')
    grok.fun()
    print('>>>>>>>>')

    print('<<<<<<<<')
    bar.fun()
    print('>>>>>>>>')

if __name__ == '__main__':
    fun()