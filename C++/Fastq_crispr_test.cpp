#include <iostream>
#include "LineReader.h"
#include <string>
#include <string.h>
#include <unordered_map>
#include "tokenize.h"
#include <vector>

void readFastqGetCount(const char*file_name, std::unordered_map<std::string,int> &ctab, int trim){
    int nline = 0;
    int nreadcount = 0;
    io::LineReader in(file_name);

    // Parse all line of fastq file
    while(char*line = in.next_line()){
        nline += 1;

        // Read are every 4 line and second line of Read entry
        if (nline%4 == 2){
            nreadcount += 1;
            std::string str_line = line;

            // Trimme the read if necessary
            auto trimmed_line =str_line.substr(trim);

            // Find and insert into map
            auto got = ctab.find(trimmed_line);
            if (got == ctab.end()){
                ctab.insert({trimmed_line, 1});
            }else {
                ctab[trimmed_line] += 1;
            }
        }
    }
}

void readLib(const char*file_name, const std::unordered_map<std::string,int> &ctab, int trim){
    io::LineReader in(file_name);
    while(char*line = in.next_line()){
        // std::cout << line << std::endl;

        std::vector<std::string> vec;
        tokenize(line, ",", vec);

        auto __sgrna_pos = 2;
        auto __geneid_pos = 0;
        auto sgrnaseq = vec[__sgrna_pos];
        auto geneid = vec[__geneid_pos];

        // Try catch error if seq is smaller than trim
        try{
            sgrnaseq = sgrnaseq.substr(trim);
        }catch(const exception & e){
            std::cerr << sgrnaseq << " " << e.what() << std::endl;
        }

        auto search = ctab.find(sgrnaseq);
        if(search != ctab.end()) {
            std::cout << geneid << " " << sgrnaseq << " : " << search->second << std::endl;
        }
    }
}

int main(){
    auto trim = 0;
    std::unordered_map<std::string,int> ctab;
    readFastqGetCount("/home/arnaud/Downloads/HumanA_lentiCRISPRv2.fq", ctab, trim);
    // for (auto &itr : ctab){
    //         std::cout << itr.first << " : " << itr.second << std::endl;
    // }
    readLib("/home/arnaud/Downloads/human_geckov2_library_a_2.csv", ctab, trim);
    return 0;
}
