#!/usr/bin/env python3
# encoding: utf-8

def factorial2(x):
    fact = 1
    if x < 0:
        return 0
    elif x == 0:
        return 1
    else:
        for i in range(1, x+1):
            fact *= i
        return fact

def sum_digits(n):
   r = 0
   while n:
       r, n = r + n % 10, n / 10
   return r

print(sum_digits(factorial2(100)))
