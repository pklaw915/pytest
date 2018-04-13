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

