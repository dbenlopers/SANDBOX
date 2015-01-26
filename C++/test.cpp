#include<iostream>
#include<string>
#include<vector>
#include<algorithm>
#include<cmath>
using namespace std;

inline void keep_window_open() { char ch; cin>>ch; }

int main()
{
        cout << " Hello world !" << endl;
        double pi = 3.14159265;
        cout.precision(4);
        cout << pi << endl;
        cout.precision(2);
        cout << pi << endl;
        cout << "Norwich" << endl ;
        cout.width (15) ;
        cout << "University" << endl ;
        cout.fill ('*') ;
        cout.width (20) ;
        cout << left << "Corps of Cadets" << endl ;
        
        int x;
        cout << "Please enter a value to print :" << endl;
        cin >> x;
        if (cin.fail())
        {
                cout << "Error : not a int !!" << endl;
        }
        else
        {
                cout << "your value is : " << x << endl ;
        }
	keep_window_open();
        return 0;
}
