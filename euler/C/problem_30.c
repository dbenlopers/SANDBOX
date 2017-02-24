#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 30 from Project Euler
 *
 * Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:
 *
 * 1634 = 1^4 + 6^4 + 3^4 + 4^4
 * 8208 = 8^4 + 2^4 + 0^4 + 8^4
 * 9474 = 9^4 + 4^4 + 7^4 + 4^4
 *
 * As 1 = 1^4 is not a sum it is not included.
 *
 * The sum of these numbers is 1634 + 8208 + 9474 = 19316.
 * Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/
// First af all we need to determine what is the bigger number from this expression
// n * 9^5.
// We know that 9^5 gives us 59049 so, because of the problem, we can do something like
// 5 * 9^5 which gives us 295245 for five digits
// Maybe this is not the fastest approach but it works
#define POWER 5
#define DIGITS 5
#define MAX (int)((DIGITS + 1) * pow(9, POWER)) // Our limit will be greater than the result of the actual limit.

unsigned int to_the_power(unsigned int number, unsigned int summatory);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int total = 0;
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // Core algorithm
    for(unsigned int i = 10; i < MAX; ++i)
    {
        if(i == to_the_power(i, 0))
        {
            total += i;
        }
    }
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int to_the_power(unsigned int number, unsigned int summatory)
{
    if(number == 0)
        return summatory;
    unsigned int temp = number % 10;
    return to_the_power(number / 10, summatory + ( temp * temp * temp * temp * temp));
}
