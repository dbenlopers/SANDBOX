{- 
 - Solution to Project Euler problem 48
 -}


main = putStrLn (show ans)
ans = mod (sum [k^k | k <- [1..1000]]) (10^10)
