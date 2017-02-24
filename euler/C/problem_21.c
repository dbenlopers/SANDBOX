#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 21 from Project Euler
 *
 * Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evently into n)
 * if d(a) = b and d(b) = a, where a != b, then a and b are amicable pair and each of a and be are called amicable numbers
 *
 * For example, the proper divisors of 220 are 1, 2, 3, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(200) = 284.
 * The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.
 *
 * Evaluate the sum of all the amicable numbers unders 10000.
 *
 * PLASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/
#define MAX (int)( 1 * pow(10, 4) ) // Our maxmium number

/**
 * d
 * @param unsigned long int number
 * @return unsigned long int
 * @description
 *  Find the proper divisors of a given number and sum them
 **/
unsigned int d(unsigned int number);

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int summatory = 0, temp = 0;
    // Run the algorithm
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // For each number to MAX
    for(unsigned int i = 1; i < MAX; i++)
    {
        temp = d(i); // Core
        if( d(temp) == i && i != temp) // Amicable number
            summatory += i;
    }
    // Finish
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int d(unsigned int number)
{
    // Helper variables
    unsigned int summatory = 0;

    for(unsigned int i = 1; i < number; i++)
    {
        if( number % i == 0) // Divisor found
            summatory += i;
    }
    return summatory;
}
