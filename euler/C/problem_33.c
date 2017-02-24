#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
/**
 * Problem 33 from Project Euler
 *
 * The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
 *
 * We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
 *
 * There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.
 *
 * If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
 *
 **/
#define MAX 10
#define LOOP_START 11
#define LOOP_END 99

/**
 * fraction
 * @param unsigned int numerator
 * @param unsigned int denominator
 * @return unsigned double
 * @description
 *  Perform the fraction of two given numbers
 **/
double fraction(unsigned int numerator, unsigned int denominator);

/**
 * digit_cancelable
 * @param unsigned int numerator
 * @param unsigned int denominator
 * @return unsigned int
 * @description
 *  Check if the fraction is digit cancelable
 **/
unsigned int digit_cancelable(unsigned int numerator, unsigned int denominator);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int trivial_numerator = 1, trivial_denominator = 1;
    // Start
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // We skip the first ten numbers because the are digit cancelable
    for(unsigned int i = LOOP_START; i <= LOOP_END; i++)
    {
        for(unsigned int j = LOOP_START; j < i; j++)
        {
            if(digit_cancelable(j, i) == 1)
            {
                trivial_numerator *= j;
                trivial_denominator *= i;
            }
        }
    }
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

inline double fraction(unsigned int numerator, unsigned int denominator)
{
    double d = (double)denominator;
    return numerator / d;
}

unsigned int digit_cancelable(unsigned int numerator, unsigned int denominator)
{
    if(denominator % MAX == 0 || numerator % MAX == 0)
        // We do not care about multiples of 10 here
        return 0;

    double fr = fraction(numerator, denominator);
    unsigned int numerator_1 = numerator / MAX, numerator_2 = numerator % MAX;
    unsigned int denominator_1 = denominator / MAX, denominator_2 = denominator % MAX;

    // Start all the checks we need to ensure that those numbers are digit cancelable
    if(numerator_1 - denominator_1 == 0)
    {
       if(fraction(numerator_2, denominator_2) - fr == 0)
           return 1;
       else
           return 0;
    }
    if(numerator_1 == denominator_2)
    {
        if(fraction(numerator_2, denominator_1) - fr == 0)
            return 1;
        else
            return 0;
    }
    if(numerator_2 == denominator_1)
    {
        if(fraction(numerator_1, denominator_2) - fr == 0)
            return 1;
        else
            return 0;
    }
    if(numerator_2 == denominator_2)
    {
        if(fraction(numerator_1, denominator_1) - fr == 0)
            return 1;
        else
            return 0;
    }

    return 0;
}
