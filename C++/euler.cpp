#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <cmath>

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

/*
 * Euler problem 2
 */

void prob2()
{
    std::vector<int> list;
    int i = 1;
    int j = 2;
    int n = 0;
    list.push_back(j);
    while (n < 4000000)
    {
        n = i + j;
        i = j;
        j = n;
        if ( n > 4000000)
        {
            break;
        }
        else 
        {
            if (n % 2 ==0)
            {
                list.push_back(n);
            }
            cout << n <<endl;
        }
    }
    int somme = std::accumulate(list.begin(), list.end(), 0);
    std::cout << "Euler problem 2 results: "<< std::endl;
	std::cout << somme << std::endl;
}


/*
 * Euler problem 2 alias
 */
void prob2alias()
{

    int term_1 = 1;
    int term_2 = 2;
    int term_3 = 0;
    int MaxTerm = 0;
    int sum = 0;

    cout<< "This Program lists the Fibonacci sequence. Please enter the Max number you want to have sequence:" << endl;

    cin >> MaxTerm ;

    while (term_1 <= MaxTerm)
    {
        cout<< term_1 << endl;
        if ((term_1 %2) == 0)
        {   
            sum += term_1;
        }

        term_3 = term_1 + term_2;
        term_1 = term_2;
        term_2 = term_3;

    }
    cout << "the sum of even value numbers is: "<< sum << endl;
}

/*
 * Euler problem 3 
 */
void prob3()
{
    long long int x;
	x = 0;
	while(x<=0) {
		cout << "Enter an integer greater than 0." << endl;
	  cin >> x;
	}

	for(int k=2; k<(sqrt((double)x)); k++){
		if(x % k == 0) {
			x = x/k;
		}
	}

	int count = 0;
	int temp = 0;
	int largestprime = 0;
	for(long long int i=(x/2); i>0; i--){
		if(x % i== 0) {
			count = 0;
			for(long long int j=(i/2); j>0; j--){
				if(i % j== 0) {
		          count++;
				}
			}
			if(count == 1 && largestprime == 0) largestprime= i;
		}
	}
	if (largestprime != 0) {
	cout << largestprime << " is the largest prime multiple of " << x << endl;;
	}
	else {
		cout << x << " is a prime number." << endl;
	}
}

/*
 * Euler problem 4
 */
void prob4()
{

}

int main()
{
    //cout << "Problem 1" << endl;
	//prob1();
	//cout << "Problem 2" << endl;
	//prob2();
	//prob2alias();
	//cout << "Problem 3" << endl;
	//prob3();
	prob4();
	return 0;
}
