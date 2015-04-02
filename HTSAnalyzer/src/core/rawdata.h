#ifndef DEF_RAWDATA
#define DEF_RAWDATA

#include <vector>

class rawdata
{
    private:
        std::string feature;
        std::vector<double> featData;
    
    public:

    rawdata();
    rawdata(std::string& feat, std::vector<double>& featData);
    ~rawdata(); 
}

#endif
