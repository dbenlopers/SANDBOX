{- 
 - Solution to Project Euler problem 7
 -}


main = putStrLn (show ans)
ans = primes !! 10000

-- A lazy infinite sequence of prime numbers
primes = sieve [2..] where
	sieve (p:xs) = p : sieve (filter (\x -> mod x p /= 0) xs)
