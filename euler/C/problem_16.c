#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 16 from Project Euler
 *
 * 2?15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
 * What is the sum of the digits of the number 2^1000?
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 */
#define POW (1000)
#define MIN_POW ( POW - 1)
int main(int argc,char* argv[])
{
    // Benchmark variables
    double start, end;
    // The array of every power
    unsigned int powers[POW] = {1};
    // Total
    unsigned int total = 0;
    // Start the benchmark
    start = clock();
    for(unsigned short int i = 1; i <= POW; i++)
    {
        for(unsigned short int j = 0; j < MIN_POW; j++)
        {
            powers[j] *= 2;
        }
        for(unsigned short int j = 0; j < MIN_POW; j++)
        {
            if(powers[j] > 9)
            {
                powers[j + 1] += 1;
                powers[j] %= 10;
            }
        }
    }
    // Sum all the digits
    for(unsigned int i = 0; i < MIN_POW; i++)
    {
        total += powers[i];
    }
    // Algorithm end
    end = clock();
    printf("%d\n", total);
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
