/* 
 * Well implementation class
 * A well contain value in single cell resolution, they are represented by a vector
 */

#include <iostream>
#include <vector>
#include <string>
#include <iterator>
#include <algorithm>
#include "well.h"
#include "include/stat.h"

// default constructor
well::well()
{
}

// constructor with descriptions (genename for example) and position in plate
well::well(std::string name, int col, int row)
{
	GeneName = name;
	IdCol = col;
	IdRow = row;
}

// destructor
well::~well()
{
}

// add value in vector
void well::add_value(double value)
{
	data.push_back(value);
}

// get value
std::vector<double> well::get_data() const
{
	return data;
}

// set genename of well
void well::set_genename(std::string name)
{
	GeneName = name;
}

// get genename of well
std::string well::get_genename() const
{
	return GeneName;
}

// set col position of well
void well::set_col(int col)
{
	IdCol = col;
}

// set row position of well
void well::set_row(int row)
{
	IdRow = row;
}

// get col positions of well
int well::get_col() const
{
	return IdCol;
}

// get row positions of well
int well::get_row() const
{
	return IdRow;
}

//get number of cell in well
int well::get_size() const
{
	return data.size();
}

// print value in console
void well::print() const
{
	std::copy(data.begin(), data.end(), std::ostream_iterator<double>(std::cout, " "));
	std::endl (std::cout);
}

// get mean of value
double well::get_mean()
{
	return stat::mean(data);
}

// get standart deviation of value
double well::get_std()
{
	return stat::std(data);
}

// get variance of value
double well::get_var()
{
	return stat::var(data);
}

// get median of value
double well::get_median()
{
	return stat::median(data);
}

// get MAD of value
double well::get_mad()
{
    return stat::mad(data);
}
