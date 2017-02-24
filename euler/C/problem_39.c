#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 39 from Project Euler
 * If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.
 *
 * {20,48,52}, {24,45,51}, {30,40,50}
 *
 * For which value of p ≤ 1000, is the number of solutions maximised?
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
// Problem limit
#define MAX 1000

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int summatories[MAX] = {0};
    unsigned int index = 0, total = 0;
    // Start
    start = clock();
    printf("Algorithm starts, please wait...\n");
    /**
     * Formula used
     *  A = 2 * x * n - x ^ 2
     *  B = 2 * n ^ 2 - 2 * x * n
     *  C = 2 * n ^ 2 - 2 * x * n + x ^ 2
     *  Where x % 2 == 1 and n > x
     **/
    for(unsigned int i = 1; i < MAX; i += 2)
    {
        for(unsigned int j = (i + 1); /* No limit */; ++j)
        {
            unsigned int n = 4 * j * j + 2 * j * i;
            if(n > (MAX - 1))
                break;
            for(unsigned int k = n; k < MAX; k += n)
            {
                if(k > (MAX - 1))
                    break;
                // Build the solution
                summatories[k] += 1;
            }
        }
    }
    for(unsigned int i = 0; i < MAX; i++)
    {
        if(summatories[i] > total)
        {
            // Maximised
            total = summatories[i];
            index = i;
        }
    }
    // End
    end = clock();
    printf("%d\n", index);
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
