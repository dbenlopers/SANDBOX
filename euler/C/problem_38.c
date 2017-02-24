#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 38 from Project Euler
 *
 * Take the number 192 and multiply it by each of 1, 2, and 3:
 *
 * 192 × 1 = 192
 * 192 × 2 = 384
 * 192 × 3 = 576
 * By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)
 *
 * The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).
 *
 * What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?
 *
 **/
#define LIMIT (int)(1 * pow(10,4))
#define HALF (int)(LIMIT / 2)

/**
 * check_pandigital
 * @param unsigned int number
 * @return unsigned int
 * @description
 *  Check if a given number is pandigital
 **/
unsigned int check_pandigital(unsigned int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper Variables
    unsigned int total = 0, totals[LIMIT];
    // Start
    start = clock();
    printf("Algorithm starts, please wait...\n");
    for(unsigned int i = HALF; i <= LIMIT; i++)
    {
        total = i * 2 + LIMIT * (i);
        if(check_pandigital(total))
        {
            // Found it!!
            // Store it
            totals[i] = total;
        }
    }
    // End
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int check_pandigital(unsigned int number)
{
    // Fancy way to iterate without a for
    unsigned int temp = 0, mask = 0xFFFFFFFF;
    while(number)
    {
        if(!(number % 10))
            return 0;
        temp |= 0x1 << (number % 10 - 1);
        number /= 10;
        mask <<= 1;
    }
    return (temp == ~mask);
}
