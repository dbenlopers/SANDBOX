#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 36 fron Project Euler
 *
 * The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.
 *
 * Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
 *
 * (Please note that the palindromic number, in either base, may not include leading zeros.)
 *
 **/
#define LIMIT (int)(1 * pow(10,6))

/**
 * binary
 * @param unsigned long number
 * @return unsigned long
 * @description
 *  Convert a given number in binary digits
 **/
unsigned long binary(unsigned long number);

/**
 * palindrom
 * @param unsigned long number
 * @return unsigned int
 * @description
 *  Check if a given number is palindrom
 **/
unsigned int palindrome(unsigned long number);

/**
 * is_validate
 * @param unsigned int number
 * @return unsigned int
 * @description
 *  Helper function to keep the code clean
 **/
unsigned int is_validate(unsigned int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int total = 0;
    // Start
    printf("Algorithm starts, please wait...\n");
    start = clock();
    for(unsigned int i = 1; i < LIMIT; i++)
    {
        if(is_validate(i) == 1)
            total += i;
    }
    // End
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int is_validate(unsigned int number)
{
    if(palindrome(number) == 1 && palindrome(binary(number)) == 1)
        return 1;
    return 0;
}

unsigned int palindrome(unsigned long number)
{
    unsigned long temp = number, total = 0;
    while(temp != 0)
    {
        unsigned long temp_1 = temp % 10;
        temp /= 10;
        total = 10 * total + temp_1;
    }
    if(total == number)
        return 1;
    return 0;
}

unsigned long binary(unsigned long number)
{
    unsigned long module, i = 1, total = 0;
    do
    {
        module = number % 2;
        total += i * module;
        number /= 2;
        i *= 10;
    }while(number > 0);
    return total;
}
