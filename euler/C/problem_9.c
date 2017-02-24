#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 9 from Project Euler
 *
 * A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
 * a^2 + b^2 = c^2
 *
 * For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.
 * There exists exactly one Pythagorean triplet for which a + b + c = 1000.
 * Find the product abc.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/

#define END 1000 // You can change this

int main(int argc, char* argv[])
{
    double start, end = 0;
    printf("Algorithm starts... Please wait.\n");
    start = clock(); // Benchmark starts
    // Algorithm logic starts here
    unsigned int a,b,c = 0;
    // First Iteration
    for(a = 1; a <= END; a++)
    {
        // Second iteration
        for(b = (a+1); b <= (END - a); b++)
        {
            // Check that a + b + c == END.
            c = (END - a - b); // Invert the formula, easy to assing c in this way
            // Check if the power of a and b is equal to the power of c
            if( ( pow(a,2) + pow(b,2) == pow(c,2) ) )
            {
                // Triplet found :)
                break;
            }
        }
    }
    // Algorithm end
    end = clock();
    printf("Algorithm terminated\n");
    // Print benchmark
    printf("Total Time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
