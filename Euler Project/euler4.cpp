#include <iostream>
// You don't need <math.h>

int reverse(int num)
{
    int new_num = 0;
    while (num != 0)
    {
        int digit = num % 10;     // Move the declaration inside the loop
        new_num = new_num * 10 + digit;
        num /= 10;
    }
    return new_num;
}

int main()
{
    int largest = 0;
    for (int n1 = 999; n1 >= 100; n1--)
    {
        for (int n2 = 999; n2 >= n1; n2--)
        {
            int product = n1 * n2;
            if (product > largest && reverse(product) == product)
            {
                largest = product;
            }
        }
    }
    std::cout << "Largest " << largest << std::endl;
    return 0;
}
