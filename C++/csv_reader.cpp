#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <boost/iostreams/device/mapped_file.hpp>

/*
Function for tokenize a line of csv file, return the passed contained with data
*/
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

/*
Read line by line a csv file
*/
int reader(const std::string& filepath) 
{
	int i {0};
	std::string line;
	std::ifstream myfile(filepath);
	if (myfile.is_open())
	{
		while ( getline (myfile, line))
		{
			std::vector<std::string> tk_list ;
			tokenize(line, tk_list, ",");
			std::cout << "Content of line      : " << line << '\n';
			std::cout << "Fist fields of line  : " << tk_list[0] << '\n';
			i++;
		}
		myfile.close();
		std::cout << "Number of line parsed : " << i << '\n';
	}
	else std::cout << "Unable to open file";

	return 0;
}

/*
Play with memory map file from Boost
*/
void memory_mapped_file(const char * filename)
{
	// Create a file mapping
	boost::iostreams::mapped_file m_file(filename, boost::iostreams::mapped_file::readonly);
	auto f = m_file.const_data();    //return a pointer to the first byte of data 
	auto l = f + m_file.size();
	
	//std::cout << "File data : " << f << '\n';
	std::cout << "File size : " << m_file.size() << '\n';

	uintmax_t m_numLines {0};
	while (f && f!=l)
	{
		if ((f = static_cast<const char *>(memchr(f, '\n', l-f))))
		{
			m_numLines++, f++;
		}
	}
	std::cout << "Number of lines = " << m_numLines << '\n';
}

int main() 
{
	std::string fileName ("/home/arnaud/Desktop/SUBSET 1.1.csv");
	//reader(fileName);
	memory_mapped_file(fileName.c_str());
}
