{- 
 - Solution to Project Euler problem 20
 -}


{- 
 - We do a straightforward product thanks to Haskell's built-in arbitrary precision Integer type.
 -}

main = putStrLn (show ans)
ans = digitSum (factorial 100 :: Integer)

digitSum 0 = 0
digitSum n = (mod n 10) + (digitSum (div n 10))

factorial n = product [1..n]
