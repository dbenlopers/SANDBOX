#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 14 from Project Euler
 *
 * The following iterative sequence is defined for the set of positive integers:
 * n -> n/2 (n is even)
 * n -> 3n + 1 (n is odd)
 *
 * Using the rule above and starting with 13, we generate the following sequence:
 *
 * 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
 *
 * It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms, Although it has not been proved yet
 * ( Collazt Problem), it is toughr that all starting numbers finish at 1.
 *
 * Which starting number, under one million, procude the longest chain?
 *
 * NOTE: Once the chain start the terms are allowed to go above one million.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
#define MAX (1 * pow(10,6) ) // One million limit
/**
 * collatz
 * @param unsigned long number
 * @return unsigned long
 * @description
 *  return number/2 (if number is even)
 *  return 3number + 1 (if number is odd)
 **/
unsigned int collatz(unsigned int number);

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start,end;
    // Helper variables
    unsigned int longest = 0;
    unsigned int terms = 0;
    unsigned int j = 0;
    printf("Algorithm starts, please wait....\n");
    // Benchmark starts
    start = clock();
    // Iterating trough MAX number
    for(unsigned int i = 1; i < MAX; i++)
    {
        j = i; // We need to "cache it"...
        unsigned int actualTerms = 1;
        while(j != 1) // ...until the chain is over
        {
            actualTerms ++;
            if(actualTerms > terms)
            {
                terms = actualTerms;
                longest = i; // We found the longest chain
            }
            j = collatz(j); // Apply the rules from the problem
        }
    }
    // Algorithm end
    end = clock();
    printf("Algorithm end\n");
    printf("Time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int collatz(unsigned int number)
{
    if(number % 2 == 0) // First rule
    {
        return number / 2;
    }
    // Second rule
    return (number * 3 + 1);
}
