#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 31 from Project Euler
 *
 * In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:
 *
 * 1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).
 * It is possible to make £2 in the following way:
 *
 * 1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
 * How many different ways can £2 be made using any number of coins?
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/

#define MAX 201 // Maxmium value for pence
#define COINS 8 // Number of coins in general circulation

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int total[MAX][COINS] = {1};
    unsigned int coins[COINS] = {1, 2, 5, 10, 20, 100, 200}; // Possible coins
    // Algorithm starts
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // Core
    for(unsigned int i = 1; i < MAX; i++)
    {
        for(unsigned int j = 1; j < COINS; j++)
        {
            // check for a new way
            unsigned int temp = i - coins[j];
            if(temp > 0)
            {
                total[i][j] = total[i][j - 1] + total[temp][j];
            }
            else
            {
                total[i][j] = total[i][j - 1];
            }
        }
    }
    // End
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
