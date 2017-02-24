#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
/**********************************
 *
 * Problem 5 from Project Euler
 *
 * 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
 * What is the smallest positive number that is evenly divisible by all the numbers from 1 to 20?
 *
 * PLEASE NOTE
 * In order to use this algorithm you must have gcc installed, or similar.
 *
 ***********************************/

/**
 * checkDivisible
 * @param int number
 * @return bool
 * @description
 *  Check if a number is evenly divisible from a range of others
 **/
bool checkDivisible(int number);

// Algorithm starts
int main(int argc, char **argv)
{
    // We don't have a fixed lenght of operation
    // so ther's a infinite loop
    printf("Algorithm start, please wait...\n");
    for(int i = 1; ;i++)
    {
        if( checkDivisible(i) ) // Check if the current number is evenly divisible
        {
            // If so, it's finish
            printf("Evenly divisible test passed. End\n");
            return 0;
        }
    }
    printf("Algorithm Error, you shouldn't be here anyway.\n");
    return -1;
}

bool checkDivisible(int number)
{
    // Check for our range of test numbers
    // if "number" is evenly divisible by all of them
    if(number%2==0){
        return false;
    }
    for( int i = 3; i <= 20; i+=2)
    {
        if( number % i != 0)
            return false; // Nope
    }
    return true; // Yep
}
