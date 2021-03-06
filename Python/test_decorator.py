# -*- coding: utf-8 -*-
import time
import functools

# use a decorator for timing function
def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def snooze(seconds):
    time.sleep(seconds)
    

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
    
    
@functools.lru_cache()
@clock
def fibonacci_with_cache(n):
    if n < 2:
        return n
    return fibonacci_with_cache(n-2) + fibonacci_with_cache(n-1)
    
@clock
def fibonacci_without_cache(n):
    if n < 2:
        return n
    return fibonacci_without_cache(n-2) + fibonacci_without_cache(n-1)
    
    
if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
    
    print("-------------------------------")
    print("fibonacci without cache")
    print(fibonacci_without_cache(6))
    print("fibonacci with cache")
    print(fibonacci_with_cache(6))
    
    
