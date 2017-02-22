#!usr/bin/python3

def fibonaccu_seq():
    next, prev, iter = 1, 1, 1
    while 1:
        yield next, iter
        next, prev, iter = prev, next+prev, iter+1

digits = 1000

for num, term, in fibonaccu_seq():
    if len(str(num)) == digits:
        break

print("1st Fibo term with {0} digits is {1}".format(str(digits), str(term)))
