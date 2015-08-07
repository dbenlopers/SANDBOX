def factorial(x):
    if x > 0:
        return x*factorial(x-1)
    else:
        return 1

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
