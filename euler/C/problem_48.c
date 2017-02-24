#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 48 from Project Euler
 *
 * The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
 *
 * Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
#define MODULAR 10000000000

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned long long int total = 0;
    // Start
    printf("Algorithm stars... please wait.\n");
    start = clock();
    for(unsigned int i = 1; i <= 1000; i++)
    {
        unsigned long long int temp = i;
        for(unsigned int j = 0; j < (i - 1); j++)
        {
            temp = (temp * i) % MODULAR;
        }
        total = (total + temp) % MODULAR;
    }
    // End
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
