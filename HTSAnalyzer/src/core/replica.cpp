/*
 * replica implementation 
 * a replica contain a number of well, depend on replica format
 */
#include <iostream>
#include <string>
#include <vector>
#include "replica.h"
#include "well.h"
 
replica::replica(int row, int col)
{
    SizeRow = row;
    SizeCol = col;
}
 
replica::~replica()
{ 
}


void replica::add_well(well &Well)
{
    int col = Well.get_col();
    int row = Well.get_row();
    Replica[row][col] = Well;
}



void replica::print()
{
    int i,j;
    well tmp;
    for (i=0; i < SizeRow; i++)
        for (j=0; j < SizeCol; j++)
            tmp = Replica[i][j];
            std::cout <<  tmp.get_mean() << "/t";
        std::cout << std::endl;
}


std::vector<std::vector<double>> replica::getMeanReplica()
{  
    well tmp;
    int i,j;
    std::vector<std::vector<double>> meanreplica;
    meanreplica.resize(SizeRow);
    for (int i = 0; i < SizeRow; ++i)
        meanreplica[i].resize(SizeCol);
    
    for (i = 0; i < SizeRow; i++)
        for (j = 0; j < SizeCol; j++)
            tmp = Replica[i][j];
            meanreplica[i][j] = tmp.get_mean();
    
    return meanreplica;
}

std::vector<std::vector<double>> replica::getMedianReplica()
{
    well tmp;
    int i,j;
    std::vector<std::vector<double>> medianreplica;
    medianreplica.resize(SizeRow);
    for (int i = 0; i < SizeRow; ++i)
        medianreplica[i].resize(SizeCol);
    
    for (i = 0; i < SizeRow; i++)
        for (j = 0; j < SizeCol; j++)
            tmp = Replica[i][j];
            medianreplica[i][j] = tmp.get_median();
    return medianreplica;
}
