#include <stdio.h>
#include <stdlib.h>
/****************************************
 *
 * Problem 3 from Project Euler
 *
 * The prime factors of 13195 are 5, 7, 13 and 29.
 *
 * What is the largest prime factor of the number 600851475143 ?
 *
 * PLEASE NOTE
 * In order to compile this file you must have gcc installed
 *******************************************/

/*
 * Thanks to Casablanca for this implementation
 * of a dynamically growing array
 * @reference http://stackoverflow.com/a/3536261/1202367
 **/
// Defining a new structure
typedef struct
{
    int *array;
    size_t used;
    size_t size;
} Array;

// Helpers function to handle the new Array struct
/**
 * initArray
 * @param Array *a
 * @param size_t initialSize
 * @description
 *  Initialize a new array with a static size
 * */
void initArray(Array *a, size_t initialSize);
/**
 * insertArray
 * @param Array *a
 * @param int element
 * @description
 *  Push a new element inside our Array *a, if the size
 *  is not enough we realloc a new array
 **/
void insertArray(Array *a, int element);
/**
 * freeArray
 * @param Array *a
 * @description
 *  release the array memeory
 * */
void freeArray(Array *a);

// Algorithm start
int main(int argc, char **argv)
{
    long int startPoint = 600851475143; // Starting point from project euler, you can change it
    Array primeFactors; // Our beautiful new Array for prime factors
    int maxPrimeFactor = 0; // Max, if founded.
    initArray(&primeFactors, 1); // Initialize empty array with size of one

    // Start the iteration
    while( startPoint > 1 )
    {
        for( int i = 2; i <= startPoint; i++)
        {
            if( startPoint % i == 0) // If startPoint is divisible by i
            {
                startPoint = (startPoint / i); // Actually divide the starting Point
                insertArray(&primeFactors, i); // Inser the value inside our Array
                if( primeFactors.array[i] > maxPrimeFactor) // check if is the Max around here
                {
                    maxPrimeFactor = primeFactors.array[i]; // If max, save it.
                }
            }
        }
    }
    freeArray(&primeFactors); // Release the ... memory
    return 0; // End of the algorithm
}

// Implementation of the helper functions
// see the header above for any details
void initArray(Array *a, size_t initialSize)
{
    a->array = (int *)malloc(initialSize * sizeof(int));
    a->used = 0;
    a->size = initialSize;
}
void insertArray(Array *a, int element)
{
    if( a->used == a->size)
    {
        a->size *= 2;
        a->array = (int *)realloc(a->array, a->size * sizeof(int));
    }
    a->array[a->used++] = element;
}
void freeArray(Array *a)
{
    free(a->array);
    a->array = NULL;
    a->used = a->size = 0;
}
