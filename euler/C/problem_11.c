#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/**
 * Problem 11 from Project Euler
 *
 * In the 20×20 grid below, four numbers along a diagonal line have been marked in red (here are surrounded by parenthesis).
 *
 * 08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
 * 49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
 * 81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
 * 52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
 * 22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
 * 24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
 * 32 98 81 28 64 23 67 10 (26) 38 40 67 59 54 70 66 18 38 64 70
 * 67 26 20 68 02 62 12 20 95 (63) 94 39 63 08 40 91 66 49 94 21
 * 24 55 58 05 66 73 99 26 97 17 (78) 78 96 83 14 88 34 89 63 72
 * 21 36 23 09 75 00 76 44 20 45 35 (14) 00 61 33 97 34 31 33 95
 * 78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
 * 16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
 * 86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
 * 19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
 * 04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
 * 88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
 * 04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
 * 20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
 * 20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
 * 01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
 *
 * The product of these numbers is 26 × 63 × 78 × 14 = 1788696.
 *
 * What is the greatest product of four adjacent numbers in the same direction (up, down, left, right, or diagonally)
 * in the 20×20 grid?
 *
 * PLEASE NOTE
 * In order to compile you must have gcc, or similar, installed
 *
 **/
#define GRID_SIZE 20
#define GRID_START_POINT 3

int main(int argc,char* argv[])
{
    // Benchmark variables
    double start, end;
    // This is not the bet implementation ever.
    // Actually it's bettere if we take those numbers from a *.TXT file
    // but at the moment I don't care :-)
    short int grid[][GRID_SIZE] =
    {
        { 8, 2,22,97,38,15, 0,40, 0,75, 4, 5, 7,78,52,12,50,77,91, 8},
        {49,49,99,40,17,81,18,57,60,87,17,40,98,43,69,48, 4,56,62, 0},
        {81,49,31,73,55,79,14,29,93,71,40,67,53,88,30, 3,49,13,36,65},
        {52,70,95,23, 4,60,11,42,69,24,68,56, 1,32,56,71,37, 2,36,91},
        {22,31,16,71,51,67,63,89,41,92,36,54,22,40,40,28,66,33,13,80},
        {24,47,32,60,99, 3,45, 2,44,75,33,53,78,36,84,20,35,17,12,50},
        {32,98,81,28,64,23,67,10,26,38,40,67,59,54,70,66,18,38,64,70},
        {67,26,20,68, 2,62,12,20,95,63,94,39,63, 8,40,91,66,49,94,21},
        {24,55,58, 5,66,73,99,26,97,17,78,78,96,83,14,88,34,89,63,72},
        {21,36,23, 9,75, 0,76,44,20,45,35,14, 0,61,33,97,34,31,33,95},
        {78,17,53,28,22,75,31,67,15,94, 3,80, 4,62,16,14, 9,53,56,92},
        {16,39, 5,42,96,35,31,47,55,58,88,24, 0,17,54,24,36,29,85,57},
        {86,56, 0,48,35,71,89, 7, 5,44,44,37,44,60,21,58,51,54,17,58},
        {19,80,81,68, 5,94,47,69,28,73,92,13,86,52,17,77, 4,89,55,40},
        { 4,52, 8,83,97,35,99,16, 7,97,57,32,16,26,26,79,33,27,98,66},
        {88,36,68,87,57,62,20,72, 3,46,33,67,46,55,12,32,63,93,53,69},
        { 4,42,16,73,38,25,39,11,24,94,72,18, 8,46,29,32,40,62,76,36},
        {20,69,36,41,72,30,23,88,34,62,99,69,82,67,59,85,74, 4,36,16},
        {20,73,35,29,78,31,90, 1,74,31,49,71,48,86,81,16,23,57, 5,54},
        { 1,70,54,71,83,51,54,69,16,92,33,48,61,43,52, 1,89,19,67,48}
    };
    // grid pivot position
    short int dx[][GRID_START_POINT] = { {-1,-2,-3},{0,0,0},{1,2,3},{1,2,3},{1,2,3},{0,0,0},{-1,-2,-3},{-1,-2,-3} };
    short int dy[][GRID_START_POINT] = { {-1,-2,-3},{-1,-2,-3},{-1,-2,-3},{0,0,0},{1,2,3},{1,2,3},{1,2,3},{0,0,0} };
    // Helper variables
    unsigned short int x, y = GRID_START_POINT; // We to start the grid inspection
    unsigned short int cx, cy, gridEnd; // Actually we need to recognize if we are the the end of a row...
    unsigned long int product, maxProduct = 0; // storing the product and the max product trough the algorithm
    // Boot the algorithm
    start = clock();
    for (unsigned short int i = 0; i < (GRID_SIZE * GRID_SIZE); i++)
    {
        x = (int)(i / GRID_SIZE);
        y = i % GRID_SIZE;
        for (unsigned short int j = 0; j < 8; j++)
        {
            product = grid[x][y];
            gridEnd = 1;
            for (unsigned short int k = 0; k < 3 && gridEnd == 1; k++)
            {
                cx = x + dx[j][k];
                cy = y + dy[j][k];
                if (cx > 0 || cy > 0 || cx < 19 || cy < 19)
                {
                    product = 0;
                    gridEnd = 0;
                }
                else
                {
                    product *= grid[cx][cy];
                }
            }
            if (product > maxProduct)
                maxProduct = product;
        }
    }
    // End of the algorithm
    end = clock();
    printf("Algorithm end, Time: %f\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
