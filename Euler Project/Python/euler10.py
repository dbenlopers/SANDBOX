#!/usr/bin/env python3
# encoding: utf-8


# function to factor a given positive integer n
def is_prime(n):
    if n ==1: return False
    if n ==2: return True
    # look for factors of 2 first
    if n % 2 == 0: return False
    # now look for odd factors
    p = 3
    while p < n**0.5+1:
        if n % p == 0: return False
        p += 2
    return True

def sum_prime_below(x):
    sum = 0
    for i in range(x):
        if is_prime(i):
            sum += i
    return sum
    

print(sum_prime_below(2000000))

### or 

import math
def isprime(tal):
    prime = 1
    if tal % 2 == 0:
        prime = 0
        return prime
    x = 3
    while x <= math.sqrt(tal):
        if tal % x == 0:
            prime = 0
            break
        x+=2
    return prime
svar = 2
i = 3
while i < 2000000:
    if isprime(i) == 1:
        svar+=i
    i+=1
print svar
