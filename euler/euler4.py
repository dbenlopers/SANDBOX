#!/usr/bin/env python3
# encoding: utf-8
"""
Euler problems4 with python
Find the largest palindrome made from the product of two 3-digit numbers.
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99
"""

def is_pal(to_test):
    return str(to_test) == str(to_test)[::-1]
    
x = 999
y = 999
max_pal = 0

for i in range(x):
    for j in range(y):
        product = i * j
        if is_pal(product) and product > max_pal:
            max_pal = product

print(max_pal)
