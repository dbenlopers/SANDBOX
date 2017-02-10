#include <bits/stdc++.h>
#include "FileReader.hpp"
#include "tokenize.h"
using namespace std;

template<typename T>
void PrintVector(const std::vector<T>& vec) {
    for(auto& i : vec)
        std::cout << i << '\n';
    }

void ReadFile(const char* InputFileName){
    int nline = 0;
    io::LineReader in(InputFileName);

    while(char* line = in.next_line()){
        if (nline == 0){
            std::vector<std::string> vec;
            tokenize(line, ",", vec);
            PrintVector(vec);
        }
        nline += 1;
        //cout << line << "\n";
    }
    cout << "Total number of line parsed : " << nline << "\n";
}

int main(){

    ReadFile("/home/akopp/Desktop/TEST/160713 Eloi 384.csv.csv");
    return 0;
}
