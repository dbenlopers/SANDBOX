{- 
 - Solution to Project Euler problem 97
 -}


main = putStrLn (show ans)
ans = mod (28433 * 2^7830457 + 1) (10^10)
