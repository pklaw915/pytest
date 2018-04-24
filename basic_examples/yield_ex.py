import asyncio

# 1: print in the function
def fab1(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1

# 2: return a list
def fab2(max):
    n, a, b = 0, 0, 1
    L = []
    while n < max:
        L.append(b)
        a, b = b, a + b
        n = n + 1
    return L

# 3: an iterator
class Fab:
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()

# 4: yield
def fab3(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield  b
        a, b = b, a + b
        n = n + 1

# 5: yield from
def fab4(max):
    # same as:
    # for item in fab3(max): yield item
    yield from fab3(max)
    return max

def fab5(max):
    n = yield from fab4(max)
    print('count: %d' % n)

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)  # 和next方法一样 获取下一个值，必须先使用None参数调用一次， 执行到yield
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)  # 先发送值给yield语句，再执行到yield语句时返回
        print('[PRODUCER] Consumer return:%s' % r)
    c.close()

if __name__ == '__main__':
    #fab1(5)
    #
    #for n in fab2(5):
    #    print(n)
    #
    #for n in Fab(5):
    #    print(n)
    #
    #for n in fab3(5):
    #    print(n)
    #
    #a = [n for n in fab3(5)]        # a list
    #for n in a:
    #    print(n)
    #
    #g = (n for n in fab3(5))        # a generator
    #for n in g:
    #    print(n)
    #
    #c = consumer()
    #produce(c)
    #
    #for n in fab4(5):
    #    print(n)
    for n in fab5(5):
        print(n)




