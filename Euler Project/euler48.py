#!/usr/bin/env python3
# encoding: utf-8

sum = 0
N= 1000
for i in range(1,N+1):
    sum += i**i

print(str(sum)[-10:])
