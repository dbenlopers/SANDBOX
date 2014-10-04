#include <iostream>
using namespace std;

double square(double x)
{
    return x*x;
}


void print_square(double x)
{
    cout << "the square of " << x << " is "<< square(x) << "\n";
}

void print() {
    int v[]={0,2,3,4,5,6,7,8,9,10};
    
    for (auto x : v)
        cout << x << "\n";
    for (auto& x : v) //ici on prend la réference donc modification possible ???
        ++x;
    for (auto x : v)
        cout << x << "\n";
}

bool fuck()
{
    for (char c ; cin >> c;)
        cout << "the value of " << c << " is " << int(c) << "\n";
}

int main()
{
    cout << "Hello world \n";
    print_square(15.2);
    print_square(2);
    print_square(1512.2);
    print_square(10);
    print_square(42);
    print();
    fuck();
}
