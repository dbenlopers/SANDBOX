#include <iostream>
#include <fstream>
#include <string>
#include <vector>

template <class ContainerT>
void tokenize(const std::string& str, ContainerT& tokens, const std::string& delimiters = " ", bool trimEmpty = false)
{
	std::string::size_type pos, lastPos = 0;
	using value_type = typename ContainerT::value_type;
	using size_type = typename ContainerT::size_type;

	while(true)
	{
		pos = str.find_first_of(delimiters, lastPos);
		if(pos == std::string::npos)
		{
			pos = str.length();
			
			if(pos != lastPos || !trimEmpty)
				tokens.push_back(value_type(str.data()+lastPos, (size_type)pos-lastPos));
			break;
		}
		else
		{
			if(pos != lastPos || !trimEmpty)
				tokens.push_back(value_type(str.data()+lastPos, (size_type)pos-lastPos));
		}
		lastPos = pos + 1;
	}
}

int reader(const std::string& filepath) 
{
	std::string line;
	std::ifstream myfile(filepath);
	if (myfile.is_open())
	{
		while ( getline (myfile, line))
		{
			std::vector<std::string> tk_list ;
			tokenize(line, tk_list, ",");
			std::cout << "Content of list      : " << line << '\n';
			std::cout << "Fist fields of line  : " << tk_list[0] << '\n';
		}
		myfile.close();
	}
	else std::cout << "Unable to open file";

	return 0;
}

int main() 
{
	std::string fileName ("/home/arnaud/Desktop/asso_gene_genome_goid.csv");
	reader(fileName);
}
