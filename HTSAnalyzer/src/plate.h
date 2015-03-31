#ifndef DEF_PLATE
#define DEF_PLATE

#include <string>
#include <vector>
#include <well.h>

class plate
{
	private:
        std::vector<std::vector<well> > Plate;
        std::string Name;
        std::vector<std::vector< std::string> > PlateSetup;
        int SizeCol, SizeRow;
	
	public:
        plate(int row, int col);
        ~plate();
        void add_well(well &Well);
        void print();
        std::vector<std::vector<double>> getMeanPlate();
        std::vector<std::vector<double>> getMedianPlate();
};
#endif
