#include <vector>
#include <iostream>
#include <algorithm>

struct IdxCompare
{
    const std::vector<int>& target;

    IdxCompare(const std::vector<int>& target): target(target) {}

    bool operator()(int a, int b) const { return target[a] < target[b]; }
};

int main()
{
    std::vector<int> x = {15, 3, 0, 20};
    std::vector<int> y;

    // initialize indexes
    for(size_t i = 0; i < x.size(); ++i)
        y.push_back(i);

    std::sort(y.begin(), y.end(), IdxCompare(x));

    std::cout << "\nvector x: " << '\n';
    for(size_t i = 0; i < x.size(); ++i)
        std::cout << x[i] << '\n';

    std::cout << "\nvector y: " << '\n';
    for(size_t i = 0; i < x.size(); ++i)
        std::cout << y[i] << '\n';

    std::cout << "\nvector x through y: " << '\n';
    for(size_t i = 0; i < x.size(); ++i)
        std::cout << x[y[i]] << '\n';
}
