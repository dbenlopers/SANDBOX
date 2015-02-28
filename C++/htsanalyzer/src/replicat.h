#ifndef DEF_REPLICAT
#define DEF_REPLICAT

#include <vector>
#include "plate.h"

class replicat
{
    private:
        std::vector<plate> ListeRep;
        int nbRep;
        
    public:
        replicat();
        ~replicat();

};

#endif
