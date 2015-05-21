#ifndef DEF_PLATEMAP
#define DEF_PLATEMAP

#include <map>
#include <string>

class platemap
{
    private:
        std::map <std::string, std::string> PlateSetup;

    public:
        platemap();
        ~platemap();
        std::string getPosition(std::string to_search);
        std::string getContent();
        void print();
        platemap getPlateMap();
};

#endif
