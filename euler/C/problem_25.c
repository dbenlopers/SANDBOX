#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 25 from Project Euler
 *
 * The Fibonacci sequence is defined by the recurrence relation:
 *  Fn = Fn−1 + Fn−2, where F1 = 1 and F2 = 1.
 * Hence the first 12 terms will be:
 * F1 = 1
 * F2 = 1
 * F3 = 2
 * F4 = 3
 * F5 = 5
 * F6 = 8
 * F7 = 13
 * F8 = 21
 * F9 = 34
 * F10 = 55
 * F11 = 89
 * F12 = 144
 *
 * The 12th term, F12, is the first term to contain three digits
 *
 * What is the first term in the Fibonacci sequence to contain 1000 digits?
 *
 **/
#define DIGITS 1000 // Max digits, write like that just because :)

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variable
    unsigned int pivot[DIGITS] = {1}, swapper[DIGITS] = {1}, numbers[DIGITS] = {1};
    unsigned int total = 2;
    // Algorithm starts here
    printf("Algorithm starts, please wait\n");
    start = clock();
    // Until we reach the maximum of our algorithm
    while(numbers[(DIGITS-1)] == 0)
    {
        // For each digits
        for(unsigned int i = 0; i < DIGITS; i++)
        {
            // We have to sum our actual digits...
            numbers[i] = pivot[i] + swapper[i];
            // ...until we have a number greater than 9
            if(numbers[i] > 9)
            {
                pivot[i + 1] += numbers[i] / 10;
                numbers[i] %= 10;
            }
            // Swap the terms
            pivot[i] = swapper[i];
            swapper[i] = numbers[i];
        }
        // Increase our total based on fibonacci rule
        total++;
    }
    // Algorithm end
    end = clock();
    printf("Algorithm end\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
