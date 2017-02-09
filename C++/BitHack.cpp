#include <iostream>
#include <bitset>
using namespace std;

// is odd or even
void isOdd(int n)
{
    if (n & 1)
        cout << n << " is odd" << endl;
    else
        cout << n << " is even" << endl;
}

// if two int have opposite sign
void oppositeSign(int x, int y)
{
    cout << x << "  in binary is " << bitset<32>(x) << endl;
    cout << y << " in binary is " << bitset<32>(y) << endl;

     // true iff x and y have opposite signs
    bool isOpposite = ((x ^ y) < 0);

    if (isOpposite)
        cout << x << " and " << y << " have opposite signs" << endl;
    else
        cout << x << " and " << y << " don't have opposite signs" << endl;
}

void addOne(int x)
{
    cout << x << " + " << 1 << " is " << -~x << endl;
}

void swap(int &x, int &y)
{
    if (x != y)
    {
        x = x ^ y;
        y = x ^ y;
        x = x ^ y;
    }
}

// Function to turn off k'th bit in n
int turnOffKthBit(int n, int k)
{
    return n & ~(1 << (k - 1));
}

// Function to turn on k'th bit in n
int turnOnKthBit(int n, int k)
{
    return n | (1 << (k - 1));
}

// Function to check if k'th bit is set for n or not
int isKthBitset(int n, int k)
{
    return n & (1 << (k - 1));
}

// Function to toggle k'th bit of n
int toggleKthBit(int n, int k)
{
    return n ^ (1 << (k - 1));
}

// main function
int main()
{
    isOdd(5);
    oppositeSign(4, -8);
    addOne(4);

    int x = 3, y = 4;
    cout << "Before swap: x = " << x << " and y = " << y << endl;
    swap(x, y);
    cout << "After swap: x = " << x << " and y = " << y << endl;

    int n = 20;
    int k = 3;

    cout << n << " in binary is " << bitset<8>(n) << endl;
    cout << "Turning k'th bit off" << endl;
    n = turnOffKthBit(n, k);
    cout << n << " in binary is " << bitset<8>(n) << endl;

    cout << n << " in binary is " << bitset<8>(n) << endl;
    cout << "Turning k'th bit on" << endl;
    n = turnOnKthBit(n, k);
    cout << n << " in binary is " << bitset<8>(n) << endl;

    cout << n << " in binary is " << bitset<8>(n) << endl;
    if (isKthBitset(n, k))
        cout << "k-th bit is set" << endl;
    else
        cout << "k-th bit is not set" << endl;

    cout << n << " in binary is " << bitset<8>(n) << endl;
    cout << "Toggling k'th bit of n" << endl;
    n = toggleKthBit(n, k);
    cout << n << " in binary is " << bitset<8>(n) << endl;

    return 0;
}
