#include <iostream>s
#include <vector>
#include <numeric>
#include <cmath>

using namespace std;

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

int main()
{
	cout << "Problem 3" << endl;
	prob3();
	return 0;
}
