#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 46 on Project Euler
 *
 * It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.
 *
 * 9 = 7 + 2×1^2
 * 15 = 7 + 2×2^2
 * 21 = 3 + 2×3^2
 * 25 = 7 + 2×3^2
 * 27 = 19 + 2×2^2
 * 33 = 31 + 2×1^2
 *
 * It turns out that the conjecture was false.
 *
 * What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
 *
 **/

/**
 * Classic is_prime function already use
 **/
unsigned int is_prime(int number);

/**
 * is_concjecture_find
 * @param int
 * @return unsigned int
 * @description
 *  Check if the number is composite
 **/
unsigned is_concjecture_find(int odd_number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int number = 3;
    // Start
    printf("Algorithm Starts, please wait...\n");
    start = clock();
    while(is_concjecture_find(number))
    {
        number += 2;
    }
    end = clock();
    printf("Algorithm end.\n");
    printf("%d\n", number);
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int is_prime(int number)
{
    for(unsigned int i = 2; (i * i) <= number; i++)
    {
        if(number % i == 0)
        {
            return 0;
        }
    }
    return 1;
}

unsigned int is_concjecture_find(int odd_number)
{
    for(unsigned int i = 0; (2 * i * i) < odd_number; i++)
    {
        if(is_prime(odd_number - 2 * i * i))
        {
            return 1;
        }
    }
    return 0;
}
