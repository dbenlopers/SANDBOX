#ifndef DEF_PLATE
#define DEF_PLATE

#include <map>
#include <string>
#include "replica.h"

class plate
{
    private:
        std::map <std::string, replica> replicaList;
        int nbRep;
        
    public:
        plate();
        ~plate();
        void addReplica(replica &Replica);
        void removeReplica(std::string replicaName);

};

#endif
