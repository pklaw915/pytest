import collections


class Meta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return type.__prepare__(metacls, name, bases)

    #def __new__(cls, name, bases, namespace, **kwds):
    #    return type.__new__(cls, name, bases, namespace, kwds)


class MyClass(metaclass=Meta):
    pass

class MySubclass(MyClass):
    pass


class OrderedClass(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.members = tuple(namespace)
        return result

class A(metaclass=OrderedClass):
    def one(self): pass
    def two(self): pass
    def three(self): pass
    def four(self): pass


a = MyClass()
print(a)
b = type(a)
print(b)
print(A.members)