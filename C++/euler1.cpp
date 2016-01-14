#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

/*
 * Euler problem 1
 */
void prob1()
{
	std::vector<int> list;
	int range = 1000 ;
	int i ;
	for ( i = 1; i < range; i++)
		if ( i % 3 == 0) 
		{
			list.push_back(i);
		}
		else if ( i % 5 ==0)
		{
			list.push_back(i);
		}
	int somme = std::accumulate(list.begin(), list.end(), 0);
	std::cout << "Euler problem 1 results: "<< std::endl;
	std::cout << somme << std::endl;
}

int main()
{
    cout << "Problem 1" << endl;
	prob1();
	return 0;
}
