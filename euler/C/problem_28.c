#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 28 from Project Euler
 *
 * Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:
 *
 * 21 22 23 24 25
 * 20  7  8  9 10
 * 19  6  1  2 11
 * 18  5  4  3 12
 * 17 16 15 14 13
 *
 * It can be verified that the sum of the numbers on the diagonals is 101.
 *
 * What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
 *
 **/
#define MAX 1001
#define SPIRAL (MAX * MAX)

int main(int argc, char *argv[])
{
    // Benchmar variables
    double start, end;
    // Helper variable
    unsigned int pivot = 0, total = 0;
    // Algorithm starts
    printf("Algorithm starts, please wait.\n");
    start = clock();
    // Iterating trough the spiral
    for(unsigned int i = 1; i <= SPIRAL; i += pivot)
    {
        unsigned int pow = pivot + 1;
        if( pow*pow == i)
        {
            // Since we cannot simply add i++
            // This is the only way to sum the diagonal numbers
            pivot += 2;
        }
        // Our result
        total += i;
    }
    // Finish
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
