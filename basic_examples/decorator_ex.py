import functools


def simple_decorator(func):
    def wrapper():
        print('before 111')
        func()
        print('after 111')
    return wrapper


def fn_no_decorator():
    print('do something...')


@simple_decorator
def fn_with_simple_decorator_1():
    print('do something...')


print('1 >>>>>>>>>>>>>')
fn_no_decorator()
print('2 >>>>>>>>>>>>>')
simple_decorator(fn_no_decorator)()
print('3 >>>>>>>>>>>>>')
fn_with_simple_decorator_1()


def get_simple_decorator(arg):
    def decorator(func):
        def wrapper():
            print('before 222')
            print('arg = %s' % arg)
            func()
            print('after 222')
        return wrapper
    return decorator


@get_simple_decorator('passing something to get decorator...')
def fn_with_simple_decorator_2():
    print('do something...')


print('4 >>>>>>>>>>>>>')
fn_with_simple_decorator_2()


@get_simple_decorator('first')
@simple_decorator
def fn_with_2_simple_decorator():
    print('do something...')


print('5 >>>>>>>>>>>>>')
fn_with_2_simple_decorator()


def decorator_for_fn_with_arg(func):
    def wrapper(arg):
        print('before 333')
        func(arg)
        print('after 333')
    return wrapper


@decorator_for_fn_with_arg
def fn_with_arg(arg):
    print('do something..., arg = %s' % arg)


print('6 >>>>>>>>>>>>>')
fn_with_arg('hello')


def decorator_for_fn_with_any_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('before 444')
        func(*args, **kw)
        print('after 444')
    return wrapper


@decorator_for_fn_with_any_args
def fn_with_any_args(arg1, arg2):
    print('do something in fn_with_any_args(arg1, arg2)...')
    print('... arg1 = %s' % arg1)
    print('... arg2 = %s' % arg2)


print('7 >>>>>>>>>>>>>')
fn_with_any_args('1111111', 2222222)


#####################################################
#####################################################
#####################################################

class MyDecorator(object):

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        print('before')
        self.fn(*args, **kwargs)
        print('after')


@MyDecorator
def hello1(name):
    '''hello1 doc...'''
    print('hello %s' % name)


print('8 >>>>>>>>>>>>>')
hello1('pk')
#print(hello1.__name__)     # error
print(hello1.__doc__)      # error


class MakeHtmlTagClass(object):

    def __init__(self, tag, css_class=""):
        self._tag = tag
        self._css_class = " class='{0}'".format(css_class) if css_class != "" else ""

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            '''wrapped in makeHtmlTagClass'''
            return "<" + self._tag + self._css_class + ">" \
                   + fn(*args, **kwargs) + "</" + self._tag + ">"

        return wrapped


@MakeHtmlTagClass(tag="b", css_class="bold_css")
@MakeHtmlTagClass(tag="i", css_class="italic_css")
def hello2(name):
    '''
    hello2 doc...
    '''
    return "Hello, {}".format(name)


print('9 >>>>>>>>>>>>>')
print(hello2("pk"))
print(hello2.__name__)
print(hello2.__doc__)


def memo(fn):
    cache = {}
    miss = object()

    @functools.wraps(fn)
    def wrapper(*args):
        result = cache.get(args, miss)
        if result is miss:
            result = fn(*args)
            cache[args] = result
        return result

    return wrapper


@memo
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print('10 >>>>>>>>>>>>>')
n = fib(5)
n = fib(6)
print(n)

