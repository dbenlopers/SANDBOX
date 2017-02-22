# 
# Solution to Project Euler problem 57



def compute():
	ans = 0
	numer = 0
	denom = 1
	for i in range(1000):
		numer, denom = denom, denom * 2 + numer
		if len(str(numer + denom)) > len(str(denom)):
			ans += 1
	return str(ans)


if __name__ == "__main__":
	print(compute())
