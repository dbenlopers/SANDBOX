#!/usr/bin/env python3
# encoding: utf-8


def SumSquare(x):
    val = 0
    for i in range(1, x+1):
        val += i*i
    return val
    
def SquareSum(x):
    val = 0
    for i in range(1, x+1):
        val += i
    return val*val
    
x = 100
print(SquareSum(x) - SumSquare(x))

## or
print(sum(range(1,101)) ** 2) - sum(map(lambda x: x ** 2, range(1, 101)))
