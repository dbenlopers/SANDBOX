/*
 * Plate implementation 
 * a plate contain a number of well, depend on plate format
 */
#include <iostream>
#include <string>
#include <vector>
#include "plate.h"
#include "well.h"
 
plate::plate(int row, int col)
{
    SizeRow = row;
    SizeCol = col;
}
 
plate::~plate()
{ 
}


void plate::add_well(well &Well)
{
    int col = Well.get_col();
    int row = Well.get_row();
    Plate[row][col] = Well;
}



void plate::print()
{
    int i,j;
    well tmp;
    for (i=0; i < SizeRow; i++)
        for (j=0; j < SizeCol; j++)
            tmp = Plate[i][j];
            std::cout <<  tmp.get_mean() << "/t";
        std::cout << std::endl;
}


std::vector<std::vector<double>> plate::getMeanPlate()
{  
    well tmp;
    int i,j;
    std::vector<std::vector<double>> meanplate;
    meanplate.resize(SizeRow);
    for (int i = 0; i < SizeRow; ++i)
        meanplate[i].resize(SizeCol);
    
    for (i = 0; i < SizeRow; i++)
        for (j = 0; j < SizeCol; j++)
            tmp = Plate[i][j];
            meanplate[i][j] = tmp.get_mean();
    
    return meanplate;
}

std::vector<std::vector<double>> plate::getMedianPlate()
{
    well tmp;
    int i,j;
    std::vector<std::vector<double>> medianplate;
    medianplate.resize(SizeRow);
    for (int i = 0; i < SizeRow; ++i)
        medianplate[i].resize(SizeCol);
    
    for (i = 0; i < SizeRow; i++)
        for (j = 0; j < SizeCol; j++)
            tmp = Plate[i][j];
            medianplate[i][j] = tmp.get_median();
    return medianplate;
}
