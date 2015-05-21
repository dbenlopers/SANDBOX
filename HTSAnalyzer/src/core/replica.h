#ifndef DEF_REPLICA
#define DEF_REPLICA

#include <string>
#include <vector>
#include "replica.h"
#include "well.h"

class replica
{
	private:
        std::vector<std::vector<well> > Replica;
        std::string Name;
        std::vector<std::vector< std::string> > PlateSetup;
        int SizeCol, SizeRow;
	
	public:
        replica(int row, int col);
        ~replica();
        void add_well(well &Well);
        void remove_well(id);
        void print();
        std::vector<std::vector<double>> getMeanReplica();
        std::vector<std::vector<double>> getMedianReplica();
};
#endif
