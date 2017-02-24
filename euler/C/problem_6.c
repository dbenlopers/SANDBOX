#include <stdlib.h>
#include <stdio.h>
#include <math.h>
/**
 * Problem 6 from Project Euler
 *
 * The sum of the squares of the first ten natural numbers is,
 *  1^2 + 2^2 + ... + 10^2 = 385
 * The square of the sum of the first the natural numbers is,
 *  (1 + 2 + ... + 10)^2 = 55^2 = 3025
 * Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 - 385 = 2640.
 * Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
 *
 * PLEASE NOTE
 * In order to compile this file you must have gcc, or similar, installed on your machine
 *
 **/

/**
 * sumOfSquare
 * @param int size
 * @return int
 * @description
 *  Take a size and create the sumo of the square of the "size" natural numbers
 **/
int sumOfSquare(int size);

/**
 * squareOfSum
 * @param int size
 * @return int
 * @description
 *  Take a size and create the square of the sum of the "size" natural numbers
 **/
int squareOfSum(int size);

int main(int argc, char **argv)
{
    printf("Algorithm start, please wait...\n");
    // With scalability in mind, we don't want our algorithm to be fixed
    int size = 100, difference = 0;
    // By using this two useful functions we don't have much to do
    difference = squareOfSum(size) - sumOfSquare(size);
    printf("Algorithm end.\n");
}

int sumOfSquare(int size)
{
    int summatory = 0;
    for(int i = 1; i <= size; i++)
    {
        summatory += pow(i,2);
    }
    return summatory;
}

int squareOfSum(int size)
{
    int square = 0;
    for(int i = 1; i <= size; i++)
    {
        square += i;
    }
    return pow(square,2);
}
