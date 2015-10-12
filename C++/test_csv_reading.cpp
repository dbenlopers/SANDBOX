#include <iostream>
#include "csv_parser.h"
#include <string>
#include <string.h>
#include <unordered_map>

void readFastqGetCount(const char*file_name, std::unordered_map<std::string,int> &ctab){
    int nline = 0;
    int nreadcount = 0;
    io::LineReader in(file_name);
    while(char*line = in.next_line()){
        nline += 1;
        if (nline%4 == 2){
            nreadcount += 1;
            std::string str_line = line;
            auto got = ctab.find(str_line);
            if (got == ctab.end()){
                ctab.insert({str_line, 1});
            }else {
                ctab[str_line] += 1;
            }
        }
    }
}


int main(){
    // io::CSVReader<2> in("/home/arnaud/Desktop/HDV/DATA/target_8.3.csv");
    // in.read_header(io::ignore_extra_column, "Well", "AvgIntenCh2");
    // std::string Well = "";
    // int AvgIntenCh2 = 0;
    // while(in.read_row(Well, AvgIntenCh2)){
    //     std::cout << Well << " " << AvgIntenCh2  << std::endl;
    // }

    // io::LineReader in("/home/arnaud/Downloads/HumanB_lentiGuidePuro.fq");
    // while(char*line = in.next_line()){
    //     std::string str_line = line;
    //     std::cout << line << std::endl;
        // char * token;
        // auto delim = "\t; ";
        // token = strtok(line, delim);
        // while (token != NULL) {
        //     std::cout << token << "\t";
        //     token = std::strtok(NULL, delim);
        // }
        // std::cout << std::endl;
    // }
    std::unordered_map<std::string,int> ctab;
    readFastqGetCount("/home/arnaud/Downloads/HumanB_lentiGuidePuro.fq", ctab);
    for (auto &itr : ctab){
            std::cout << itr.first << " : " << itr.second << std::endl;
    }
    return 0;
}
