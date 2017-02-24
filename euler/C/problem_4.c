#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 4 from Project Euler
 *
 * A palindromic number read the same in both ways. The largest palindrome made from the proctur of two 2-digit numbers is 9009.
 * Find the largest palindrome from the product of two 3-digit numbers
 *
 * PLEAE NOTE
 * To compile this algorithm you should have gcc, or similar, installed.
 **/

/*
 * reverse
 * @param int number
 * @return int
 * @description
 *  Since we cannot treath number as string in a strict typed language
 *  we have to find another way to solve the palindrome check
 */
int reverse(int number);

int main(int argc, char **argv)
{
    printf("Algorithm start, please wait...\n");
    // We need to store the palindrome, the size of our test and a temporary variable
    // for our loops
    int palindrome = 0, size = (pow(10,3) - 1), solver = 0;

    for( int i = size; i > 0; i--)
    {
        for(int j = size; j > 0; j--)
        {
            solver = i * j; // Store the temporary multiplication
            if( (solver > palindrome) && (reverse(solver) == solver) )
            {
                palindrome = solver; // Found the actual palindrome...
            }
        }
    }

    printf("Algorithm finish.");
    return 0;
}

int reverse(int number)
{
    int temp = number, reverse; // Variable support
    while(temp != 0)
    {
        reverse = (reverse * 10) + (temp % 10) ;
        temp /= 10;
    }
    return reverse;
}
