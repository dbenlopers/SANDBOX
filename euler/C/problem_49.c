#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * PRoblem 49 from Project Euler
 *
 * The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.
 *
 * There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.
 *
 * What 12-digit number do you form by concatenating the three terms in this sequence?
 *
 */
unsigned int is_prime(int number);

void swap(int *first_number, int *second_number);

unsigned int is_permutation(int first_number, int second_number);


int main (int argc, char *argv[])
{
    int deb;
    int pas;
    for (deb=1001; deb<9999; deb+=2)
        if (is_prime(deb))
            for (pas=2; pas*2+deb<9999; pas+=2)
                if (is_permutation(deb,deb+pas) && is_permutation(deb,deb+2*pas) && is_prime(deb+pas) && is_prime(deb+2*pas))
                    printf("%d - %d - %d\n",deb, deb+pas, deb+2*pas);
	return 0;
}

unsigned int is_prime (int number)
{
    for (unsigned int i = 2; (i * i) <= number; i++)
    {
        if (number % i == 0)
            return 0;
    }
    return 1;
}


void swap (int *first_number, int *second_number)
{
    int temp;
    if (*first_number > *second_number)
    {
        temp = *first_number;
        *first_number = *second_number;
        *first_number = temp;
    }
}

unsigned int is_permutation (int first_number, int second_number)
{
    
    int a1 = (first_number / 1) % 10;
    int a2 = (first_number / 10) % 10;
    int a3 = (first_number / 100) % 10;
    int a4 = (first_number / 1000) % 10;
    swap(&a1,&a2);
    swap(&a2,&a3);
    swap(&a1,&a2);
    swap(&a3,&a4);
    swap(&a2,&a3);
    swap(&a1,&a2);
    
    int b1 = (second_number / 1) % 10;
    int b2 = (second_number / 10) % 10;
    int b3 = (second_number / 100) % 10;
    int b4 = (second_number / 1000) % 10;
    swap(&b1,&b2);
    swap(&b2,&b3);
    swap(&b1,&b2);
    swap(&b3,&b4);
    swap(&b2,&b3);
    swap(&b1,&b2);
    
    return ( (a1==b1) && (a2==b2) && (a3==b3) && (a4==b4) );
}
