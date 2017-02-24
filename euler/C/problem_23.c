#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 23 from Project Euler
 *
 * A perfect number is a number for which the sum of its proper divisord is exactly equal to the number. For example, the sum of the
 * proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.
 *
 * A number n is called deficient it the sum of its proper divisors is less than n and it is called abundant it this sum exceeds n.
 *
 * As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundants is 24.
 * By mathematical analysis, it can be shown that all integers greater thatn 28123 can be written as the sum of two
 * number that cannot be expressed as the sum of two abundant numbers is less that this limit.
 *
 * Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/

#define MAX 28123 // Our starting point

/**
 * summatory
 * @param unsigned int
 * @return unsigned int
 * @description
 *  check if numbers are divisible ans sum it.
 **/
unsigned int summatory(unsigned int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int abundants[MAX] = {0}, results[MAX] = {0}, total = 0;
    // Starting the core algorithm
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // Iterating trough numbers
    for(unsigned int i = 1; i < MAX; i++)
    {
        if(summatory(i) > i) // Actually this is the main checking point for abundant number
        {
            abundants[i] = 1; // Flag the position i as abundant
        }
    }
    // Repeat the iteration
    for(unsigned int i = 1; i < MAX; i++)
    {
        // But now 2D version of this iteration...
        for(unsigned int j = 1; j < MAX; j++)
        {
            // ...because we need to check even the sum of two numbers
            if(abundants[i] == 1 && abundants[j] == 1 && (( i + j) < MAX))
            {
                results[i+j] = 1; // Flag the position
            }
        }
    }
    // Repeat the iteration
    for(unsigned int i = 1; i < MAX; i++)
    {
        // Check for a flag
        if(results[i] == 0)
            total += i; // sum the position to the total
    }
    // Core end
    end = clock();
    printf("%d\n", total);
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int summatory(unsigned int number)
{
    unsigned int temp = 1;
    for(unsigned int i = 2; i <= (number/2); i++)
    {
        if(number % i == 0)
            temp += i;
    }
    return temp;
}
