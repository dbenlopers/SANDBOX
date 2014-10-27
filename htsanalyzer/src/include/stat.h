#ifndef DEF_STAT
#define DEF_STAT

#include <vector>
#include <algorithm>
#include <stdexcept>

namespace stat{
    double mean(std::vector<double> &data);
    double std(std::vector<double> &data);
    double var(std::vector<double> &data);
    double median(std::vector<double> &data);
    double mad(std::vector<double> &data);
}

#endif
