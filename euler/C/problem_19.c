#include <time.h>
#include <stdio.h>
#include <stdlib.h>
/**
 * Problem 19 from Project Euler
 *
 * You are given the following information, but you may prefer to do some research for yourself.
 *  - 1 Jan 1990 was a Monday
 *  - Thirty days has September,
 *    April, June and November.
 *    All the rest have thirty-one,
 *    Saving February alone,
 *    Which has twenty-eight, rain or shine.
 *    And on leap years, twenty-nine.
 *  - A leap year occours on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
 *
 * How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
 *
 *
 **/

// After a bounch of researches I figure it our that the fiven information are corrects :)
// I will just take the "easy way"
#define TOTAL_MONTHS 12 // It's odd I know...
#define START_YEAR 1901
#define END_YEAR 2000

int main(int argc, char* argv[])
{
    // We are going to computer the total number of days in all the months in all
    // the given year-range. Why this? Simply
    // If this total is divisible by 7 will by a Sunday.
    // Benchmark variables
    double start, end;
    // Helper variables
    unsigned short int monthEnds[TOTAL_MONTHS] = {31,28,31,30,31,30,31,31,30,31,30,31};
    unsigned short int counter = 0, totalSundays = 0;
    // Algorithm starts
    printf("Algorithm starts, please wait...\n");
    start = clock();
    // For each months in a year...
    for(unsigned short int i = 0; i < TOTAL_MONTHS; i++)
    {
        // ... sum every days
        counter += monthEnds[i];
    }
    // This is the core of the algorithm, for every year in our range...
    for(unsigned short int j = START_YEAR; j <= END_YEAR; j++)
    {
        // ... If it's not a leap or a century && a century leap...
        if( !(j % 4) || ( !(j % 100) && !(j % 400) ) )
        {
            monthEnds[1] = 29; // ... We have to change the February end
        }
        else
        {
            monthEnds[1] = 28; // ... Otherwise we have to restore to the original one
        }
        // For every months in a year...
        for(unsigned short int i = 0; i < TOTAL_MONTHS; i++)
        {
            // If the day is divisible by 7...
            if( !(( counter - 1) % 7))
            {
                totalSundays ++; // it's a fucking sunday!!
            }
            counter += monthEnds[i]; // add another day after the check
        }
    }
    // Algorithm end
    end = clock();
    printf("Algorithm end.\n");
    printf("Total time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
