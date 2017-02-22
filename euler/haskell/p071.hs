{- 
 - Solution to Project Euler problem 71
 -}

import Data.Ratio ((%), numerator)


main = putStrLn (show ans)
ans = numerator $ foldl1 max [((div (d * 3) 7) - (if (mod d 7) == 0 then 1 else 0)) % d | d <- [1..10^6]]
