{- 
 - Solution to Project Euler problem 56
 -}


main = putStrLn (show ans)
ans = foldl1 max [digitsum (a^b) | a <- [0..99], b <- [0..99]]

digitsum 0 = 0
digitsum n = (mod n 10) + (digitsum (div n 10))
