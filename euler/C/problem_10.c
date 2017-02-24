#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
/**
 * Problem 10 from Project Euler
 *
 * The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17
 *
 * Find the sum of all the primes below two million.
 *
 * PLEASE NOTE
 * In order to compile this algorithm you must have gcc, or similar, installed
 *
 **/

#define MAX (2 * pow(10,6)) // Algorithm task, you can change it

/**
 * isPrime
 * @param unsigned int number
 * @description
 *  Check is a given number is a prime number
 **/
bool isPrime(unsigned int number);

int main(int argc,char* argv[])
{
    double start, end = 0; // Benchmakr variables
    printf("Algorithm starts, Please wait...\n");
    start = clock(); // Start the benchmark
    // Start the algorithm
    unsigned int i = 3;
    unsigned long primeSummatory = 2;
    while(i <= MAX) // Until we reach two million...
    {
        if( isPrime(i) ) // ...check if i is prime...
        {
            primeSummatory += i; // ...if so sum it...
        }
        i += 2; //...increment, avoid even number
    }
    // Finish the algorithm
    end = clock(); // Finish the benchmark
    printf("Algorithm end\n");
    printf("Total time: %f\n", (end-start)/CLOCKS_PER_SEC);
    return 0;
}

bool isPrime(unsigned int number)
{
    // We can assume that the number will be always
    // >= 1 because of the algorithm but I want to
    // controll it anyway
    if( number <= 1)
        return false;

    for(unsigned int i = 2; i*i <= number; i++)
    {
        if( number % i == 0)
            return false;
    }
    return true;
}
