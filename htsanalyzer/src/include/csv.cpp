#include <iostream>     // cout, endl
#include <fstream>      // fstream
#include <vector>
#include <string>
#include <algorithm>    // copy
#include <iterator>     // ostream_operator
#include <stdexcept>
#include <boost/tokenizer.hpp>

namespace csv {
    void CSVReader(std::string filePath)
    {
        using namespace std;
        using namespace boost;

        string data(filePath);

        ifstream in(data.c_str());
        if (!in.is_open()) 
        {
            cout << "File Not open"<< filePath << endl;
        }

        typedef tokenizer< escaped_list_separator<char> > Tokenizer;

        vector< string > vec;
        string line;

        while (getline(in,line))
        {
            Tokenizer tok(line);
            vec.assign(tok.begin(),tok.end());

            if (vec.size() < 3) continue;

            copy(vec.begin(), vec.end(),
                 ostream_iterator<string>(cout, "|"));

            cout << "\n----------------------" << endl;
        }
    }
}
