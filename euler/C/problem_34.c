#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 34 from Project Euler
 * 145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
 *
 * Find the sum of all numbers which are equal to the sum of the factorial of their digits.
 *
 * Note: as 1! = 1 and 2! = 2 are not sums they are not included.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/
#define MAX 50000

unsigned int factorial(unsigned int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int temp = 0, position = 0, total = 0;
    // Start
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // Iterating trough the max number
    for(unsigned int i = 3; i < MAX; i++)
    {
        temp = i;
        position = 0;
        // Determine factorial of a number
        do
        {
            // Calculate factorial of a number
            position += factorial(temp % 10);
            // Factorial computation ends here
            if(position > i)
            {
                break;
            }
            temp /= 10;
        } while(temp != 0);
        // If the sum of all numbers are equal to the sum
        // of the factorial
        if(position == i)
        {
            // Our goal
            total += i;
        }
    }
    // End
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int factorial(unsigned int number)
{
    unsigned int factorial = 1;
    for(unsigned int i = number; i > 1; i--)
    {
        factorial *= i;
    }
    return factorial;
}
