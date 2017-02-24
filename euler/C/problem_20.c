#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 20 from Project Euler
 *
 * n! means n × (n − 1) × ... × 3 × 2 × 1
 * For example, 10! = 10 × 9 × ... × 3 × 2 × 1 = 3628800,
 * and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.
 *
 * Find the sum of the digits in the number 100!
 *
 * PLEASE NOTE
 * In order to compile this file you must have gcc, or similar, installed
 *
 */

#define MAX 100
// We grab the max digits possible from the factorial of MAX
// it hasn't to be precise, we do not care since other numbers will be
// filled by 1s (during multiplication) and 0s (when we create the sum)
#define MAX_DIGITS (int)( MAX * log10(MAX) ) //We know this FOR SURE

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int digits[200] = {1}; // We need to store the digits...
    unsigned int total = 0, k = 0; // ... and the total sum of them
    // Algorithm start
    printf("Algorithm starts, plase wait... \n");
    start = clock();
    // Creating the factorial
    for(unsigned short int i = 1; i <= MAX; i++)
    {
        for(unsigned short int j = 0; j < MAX_DIGITS; j++)
        {
            digits[j] = (digits[j] * i) + k;
            k = (digits[j] / 10);
            digits[j] %= 10;
        }
    }
    // Sum the digits from the factorial
    for(unsigned short int i = MAX_DIGITS; i > 0; i--)
    {
        total += digits[i];
    }
    // End of the algorithm
    end = clock();
    printf("Algorithm finish.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
