#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 15 from Project Euler
 *
 * Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.
 * How many such routes are there through a 20×20 grid?
 *
 * PLASE NOTE
 * In order to compile this file you must have gcc, or similar, installed
 *
 */

#define GRID 20

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start, end;
    // Define our grid
    unsigned long long grid[GRID + 1][GRID + 1] = {0}; // why + 1? Avoid segfault problem.
    // Algorithm starts
    start = clock();
    // Iterating trough the maximum number of the grid
    for (unsigned short int i = 1; i <= GRID; ++i)
    {
        grid[0][i] = 1; // Build grid columns
        grid[i][0] = 1; // Build the grid rows
    }
    // The fun part
    for (unsigned short int i = 1; i <= GRID; ++i)
    {
        for (unsigned short int j = 1; j <= GRID; ++j)
        {
            // Sum the grid value, this is why we put the GRID + 1
            grid[i][j] = grid[i - 1][j] + grid[i][j - 1];
        }
    }
    // Algorithm end
    end = clock();
    printf("Alrogithm end.\n");
    printf("Time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
