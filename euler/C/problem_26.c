#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 26 from Project Euler
 *
 * A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:
 *
 * 1/2  =   0.5
 * 1/3=     0.(3)
 * 1/4=     0.25
 * 1/5=     0.2
 * 1/6=     0.1(6)
 * 1/7=     0.(142857)
 * 1/8=     0.125
 * 1/9=     0.(1)
 * 1/10=    0.1
 * Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.
 *
 * Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 **/
#define D_MAX 1000 // Our D maxmium value

/**
 * number_lenght
 * @param unsigned int number
 * @return unsigned int
 * @description
 *  Take a number and define its lenght
 **/
unsigned int number_lenght(unsigned int number);

int main(int argc, char* argv[])
{
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned int temp = 0, result = 0, max_lenght = 0;
    // Algorithm start
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // Core
    for(unsigned int i = D_MAX; i > 2; --i)
    {
        if((i % 2 != 0) && (i % 5 != 0))
        {
            temp = number_lenght(i);
            // If our number is longer than the previous one...
            if(temp > max_lenght)
            {
                // ... Use it!
                max_lenght = temp;
                result = i; // Possible result
            }
        }
    }
    // Algorithm end
    end = clock();
    printf("%d\n", result);
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}

unsigned int number_lenght(unsigned int number)
{
    unsigned int mod = 10 % number;
    unsigned int lenght = 0;
    // Until we have "drain" our number...
    while(mod != 0 && mod != 1)
    {
        // ... By simply iterate trough "10 % number" ...
        mod = (mod * 10) % number;
        // ... Increase its lenght
        lenght++;
    }
    return lenght;
}
