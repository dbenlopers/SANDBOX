#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int is_prime(n) {
    if (n % 2 == 0){
        return 0;
    }
    int p = 3;
    while(p < ((int) pow(n, 0.5) + 1)) {
        if (n % p == 0) return 0;
        p += 2;
    }
    return 1;
}

int nth_prime(n) {
    int prime = 2;
    int count = 1;
    int iter = 3;
    while(count < n) {
        if (is_prime(iter)==1) {
            prime = iter;
            count += 1;
        }
        iter += 2;
    }
    return prime;

}

int main(int argc, char **argv) {
    printf("%d\n", nth_prime(10001));
   return 0;
}
