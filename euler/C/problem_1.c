#include <stdio.h>
#include <stdlib.h>
/***********************
 *
 * Problem 1 From Project Euler
 *
 * If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
 * Find the sum of all the multiples of 3 or 5 below 1000
 *
 * This file is made with VIM under Linux with gcc compiler
 *
 * PLEASE NOTE
 * In order to compile and run you must install gcc and related
 *
 ************************/

int array_sum(int array[]);

int main(int argc, char* argv[])
{
    // I don't think this is the best way to work but...
    int size = 1000;
    int multiple[sizeof(size)] = {0};
    int total = 0;
    // First of all we need to iterate trough 1000 numbers
    for( int i = 0; i < size; i++)
    {
        if( (i % 3 == 0) || (i % 5 == 0) )
            multiple[i] = i;
    }

    // Since C does not have a builtin function I wrote something similar :)
    // And now the final part
    total = array_sum(multiple);
    return 0;
}

/****************
 *
 * array_sum()
 * Simple "hack" to sum array values
 * @param int array[]
 * @return int
 ****************/
int array_sum(int array[])
{
    int i, sum = 0;
    for( i = 0; i < 1000; i++)
    {
        sum += array[i];
    }
    return sum;
}
