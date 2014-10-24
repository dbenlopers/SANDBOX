library(foreach)
library(doMC)


A <- 5
B <- "oizf"

list = list()

print(A)
blabla <- function(input) {
  print(B)
  input <- input + 2
  return(c(input, B))
}

list <- foreach(1:10) %dopar% {
  blabla(A)
}


print(list)

var = list[[2]][2]

print(var)