#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>

namespace stat {
    /* Return mean of vector */
    template<typename T>
    double mean(std::vector<T> &data){
        size_t n = data.size();
        if (n == 0)
        {
            throw std::domain_error("Mean of an empty vector");
        }
        double sum = std::accumulate(std::begin(data), std::end(data), 0.0);
        double mean = sum/n;
        return mean;
    }

    /* Return standart deviation of vector */
    template<typename T>
    double std(std::vector<T> &data){
        size_t n = data.size();
        if (n == 0)
        {
            throw std::domain_error("Standart Deviation of an empty vector");
        }
        double m = mean(data);
        double accum = 0.0;
        std::for_each(std::begin(data), std::end(data), [&](const double d) { 
            accum += (d - m) * (d - m);
        });
        double stdev = sqrt(accum / (n-1));
        return stdev;
    }
}
int main(int argc, char** argv)
{
    std::vector<double> log{20,24,37,42,23,45,37};
    std::cout << "Vector mean : " << stat::mean(log) << std::endl;
    std::cout << "Vector std : " << stat::std(log) << std::endl;
}

