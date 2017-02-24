#include <time.h>
#include <math.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
/**
 * Problem 41 from Project Euler
 *
 * We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
 *
 * What is the largest n-digit pandigital prime that exists?
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
#define MAX (int)(1 * pow(10,7))

// Reused function from an old algorithm
unsigned int is_pandigital(unsigned int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int *primes, result = 0;
    // Assign the right size to our array
    assert(primes = malloc(MAX * sizeof(int)));
    primes[0] = primes[1] = 0;
    for(unsigned int i = 2; i < MAX; i++)
    {
        primes[i] = 1;
    }
    // Start
    printf("Algorithm starts, please wait...\n");
    start = clock();
    for(unsigned int i = 2; i < 1000; i++)
    {
        if(primes[i])
        {
            for(unsigned int j = (i * 2); j < MAX; j += i)
            {
                primes[j] = 0;
            }
        }
    }
    for(unsigned int i = (MAX - 1); i > 0; i--)
    {
        if(primes[i] && is_pandigital(i))
        {
            // Found it
            result = i;
            break;
        }
    }
    // END
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int is_pandigital(unsigned int number)
{
    // Helper variables
    unsigned int temp = number;
    unsigned int counter = 0;
    unsigned int numbers[10] = {0};
    unsigned int result = 1;

    while(temp > 0)
    {
        numbers[temp % 10] = !numbers[temp % 10];
        temp /= 10;
        counter++;
    }

    for(unsigned int i = 1; i <= counter; i++)
    {
        result *= numbers[i];
    }

    return result;

}
