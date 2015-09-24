#include <iostream>
#include "csv_parser.h"
#include <string>

int main(){
    // io::CSVReader<2> in("/home/arnaud/Desktop/HDV/DATA/target_8.3.csv");
    // in.read_header(io::ignore_extra_column, "Well", "AvgIntenCh2");
    // std::string Well = "";
    // int AvgIntenCh2 = 0;
    // while(in.read_row(Well, AvgIntenCh2)){
    //     std::cout << Well << " " << AvgIntenCh2  << std::endl;
    // }

    io::LineReader in("/home/arnaud/Desktop/TEMP/final_Cufflinks_genes_HUVEC-2x75-10885-rep2.genes.gtf");
    while(char*line = in.next_line()){
        std::cout << line << std::endl;
    }
    return 0;
}
