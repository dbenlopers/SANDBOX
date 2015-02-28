#include <vector>
#include <algorithm>
#include <stdexcept>
#include "stat.h"

namespace stat{

    /* Return mean of vector */
    double mean(std::vector<double> &data){
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
    double std(std::vector<double> &data){
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
    
    /* Return variance of vector */
    double var(std::vector<double> &data){
        size_t n = data.size();
        if (n == 0)
        {
            throw std::domain_error("Variance of an empty vector");
        }
        double m = mean(data);
	    double accum = 0.0;
	    std::for_each(std::begin(data), std::end(data), [&](const double d) { 
		    accum += (d - m) * (d - m);
	    });
	    double variance = (accum / (n-1));
	    return variance;
    }

    /* Return median of vector */
    double median(std::vector<double> &data){
	    size_t n = data.size();
	    if (n == 0)
        {
            throw std::domain_error("Median of an empty vector");
        }
	    std::nth_element(data.begin(), data.begin()+n/2, data.end());
        
        // array has a even size, so want the middle of it
        if (n%2 == 0)
        {
            return data[n/2-1];
        }
        // array has a odd size, so make average 
        else 
        {
            return (data[n/2-1] + data[n/2])/2;
        }
    }  

    /* Return Median Absolute Deviation of vector */
    double mad(std::vector<double> &data){
        size_t n = data.size();
	    if (n == 0)
        {
            throw std::domain_error("MAD of an empty vector");
        }   
        double med;
        med = median(data);
        std::vector<double> lessmed;
        //1.4826 * (median(abs(x - median)))
        for (auto it = data.begin(); it != data.end(); ++it){
            lessmed.push_back(static_cast<double>(*it));
        }
        for (auto it = lessmed.begin(); it != lessmed.end(); ++it){
            *it -= med;
        }
        double sum = std::accumulate(std::begin(lessmed), std::end(lessmed), 0.0);
	    double mad = sum/lessmed.size();
        return (1.4826*mad);
    }
}
