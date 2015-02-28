#ifndef DEF_WELL
#define DEF_WELL

#include <string>
#include <vector>

class well
{
	private:
	    std::vector<double> data;
	    std::string GeneName;
	    int IdCol;
	    int IdRow;
	
	public:
	    well();
	    well(std::string name, int col, int row);
	    ~well();
	    void add_value(double data);
	    std::vector<double> get_data() const;
	    void set_genename(std::string input);
	    std::string get_genename() const;
	    void set_col(int col);
	    void set_row(int row);
	    int get_col() const;
	    int get_row() const;
	    int get_size() const;
	    void print() const;
	    double get_mean();
	    double get_std();
	    double get_var();
	    double get_median();
        double get_mad();
};
#endif
