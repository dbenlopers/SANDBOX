#include <iostream>
#include "LineReader.h"
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

void readLib(const char*file_name, const std::unordered_map<std::string,int> &ctab){
    io::LineReader in(file_name);
    while(char*line = in.next_line()){
        // std::cout << line << std::endl;
        int cnt = 0;
        auto delim = ",;";
        char * token;
        token = std::strtok(line, delim);
        std::string sgrnaseq ;
        std::string geneid ;
        while (token != NULL) {
            cnt += 1;
            // std::cout << cnt<< " " << token << "\t" << std::endl;
            if (cnt == 1){
                geneid = token;
            }
            if (cnt == 3){
                sgrnaseq = token;
            }
            token = std::strtok(NULL, delim);
        }
        cnt = 0;

        auto search = ctab.find(sgrnaseq);
        if(search != ctab.end()) {
            std::cout << geneid << " " << sgrnaseq << " : " << search->second << std::endl;
        }
    }
}

int main(){
    std::unordered_map<std::string,int> ctab;
    readFastqGetCount("/home/arnaud/Downloads/HumanB_lentiGuidePuro.fq", ctab);
    // for (auto &itr : ctab){
    //         std::cout << itr.first << " : " << itr.second << std::endl;
    // }
    readLib("/home/arnaud/Downloads/human_geckov2_library_a_2.csv", ctab);
    return 0;
}
