#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
/**
 * Problem 7 from Project Euler
 *
 * By listing the first six prime numbers: 2,3,5,7,11 and 13, we can see that the 6th prime is 13
 * What is the 10001st prime number?
 *
 * PLEASE NOTE
 * In order to compile this file you must have gcc, or similar, installed
 *
 **/
#define LIMIT 10001 // Algorithm limit, change it for testing

bool isPrime(unsigned int number);

int main(int argc, char* argv[])
{
    double clockStart, clockEnd; // First time that I'm using this to bench the algorithm

    unsigned int pivot = 3; // Where we start to test our prime numbers
    unsigned int j = 2; // Internal counter, we need to declare here

    printf("Algorithm is online, Please wait....\n");

    clockStart = clock(); // Starting the benchmark

    while( j < LIMIT)
    {
        pivot += 2;
        if( isPrime(pivot) )
            j++;
    }

    clockEnd = clock(); // Finishing the benchmark
    printf("Algorithm end.\n");
    printf("Time: %f", (clockEnd - clockStart)/CLOCKS_PER_SEC);
    return 0;
}

bool isPrime(unsigned int number)
{
    if( number <= 1)
        return false;

    for(unsigned int i = 2; i*i <= number; i++)
    {
        if( number % i == 0)
            return false;
    }
    return true;
}
