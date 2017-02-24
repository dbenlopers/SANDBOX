#include <time.h>
#include <math.h>
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
/**
 * Problem 27 from Project Euler
 *
 * Euler discovered the remarkable quadratic formula:
 *
 * n² + n + 41
 *
 * It turns out that the formula will produce 40 primes for the consecutive values n = 0 to 39. However, when n = 40, 402 + 40 + 41 = 40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41² + 41 + 41 is clearly divisible by 41.
 *
 * The incredible formula  n² − 79n + 1601 was discovered, which produces 80 primes for the consecutive values n = 0 to 79. The product of the coefficients, −79 and 1601, is −126479.
 *
 * Considering quadratics of the form:
 *
 * n² + an + b, where |a| < 1000 and |b| < 1000
 *
 * where |n| is the modulus/absolute value of n
 * e.g. |11| = 11 and |−4| = 4
 * Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
#define MAX 1000 // As always
#define REVERSE ((MAX * (-1)) + 1) // -999
/**
 * is_prime
 * @param signed int number
 * @return unsigned int
 * @description
 *  A new kind of check for prime number, bit faster
 **/
unsigned int is_prime(int number);

int main(int argc, char *argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    int counter = 0, first_maximum = 0, second_maximum = 0, number = 0;
    // This is a freaking awesome alternative method for abs()
    // Thanks to http://stackoverflow.com/a/9772647/1202367
    unsigned int const mask = number >> sizeof(int) * (CHAR_BIT - 1);
    // Algorithm starts
    start = clock();
    printf("Algorithm starts, please wait.\n");
    // Iterating our limit
    // idk if there's a better solution but I feel comfortable with this
    // three loopsi
    for(int i = REVERSE; i < MAX; i++)
    {
        for(int j = REVERSE; j < MAX; j++)
        {
            int temp = 0;
            number = j;
            for(int k = 0; is_prime((number + mask) ^ mask) == 1; k++)
            {
                temp++;
                number = (k * k) + (i * k) + j; // Hello Euler
            }
            if(temp > counter)
            {
                // Normal swap of terms
                counter = temp;
                first_maximum = i;
                second_maximum = j;
            }
        }
    }
    // Algorithm end
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int is_prime(int number)
{
    if(number <= 1)
    {
        // Zero and One are not prime...
        return 0;
    }
    if(number == 2)
    {
        // Two is prime!
        return 1;
    }
    if(number % 2 == 0)
    {
        // Even numbers are not prime :(
        return 0;
    }
    for(unsigned int i = 3; (i * i) <= number; i+=2)
    {
        if(number % i == 0)
        {
            // Not prime :-(
            return 0;
        }
    }
    // Is prime!
    return 1;
}
