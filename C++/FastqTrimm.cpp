// string::find
#include <iostream>       // std::cout
#include <string>         // std::string
#include <fstream>
#include "LineReader.h"


void ProcessFastqFile(const char*InputFName, const char*OutputFName, std::string TrimSeq){
    int nline = 0;

    io::LineReader in(InputFName);

    std::ofstream out;
    out.open(OutputFName);

    std::size_t trimseqlen = TrimSeq.length();


    // Parse all line of fastq file
    while(char*line = in.next_line()){
        nline += 1;
        std::size_t found_pos ;

        // Get the seq of read
        if (nline%4 == 2){
            std::string str_line = line;

            found_pos = str_line.find(TrimSeq);
            if (found_pos!=std::string::npos)
                out << str_line.substr (found_pos+trimseqlen, 20) << '\n';
            else {
                // search @ the end of seq if found not the primary primer
                found_pos = str_line.find("GTTTTAGAGCT");
                if (found_pos!=std::string::npos)
                    try {
                        out << str_line.substr (found_pos-20, 20) << '\n';
                    }
                    catch (std::out_of_range & ex)
                    {
                        out << line << '\n';
                    }
                else {
                    out << line << '\n';
                }
            }

        }
        // Get the qual of read
        else if (nline%4 == 0){
            std::string str_line = line;
            if (found_pos!=std::string::npos)
                out << str_line.substr (found_pos+trimseqlen, 20) << '\n';
            else {
                out << line << '\n';
            }
        }

        else {
            out << line << '\n';
        }

    }
    out.close();
}

int main(){
    // ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN1.R1.fastq",
    // "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN1.R1.PROCESS.fastq",
    // "GGAAAGGACGAAACACCG");

    // ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN2.R1.fastq",
    // "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN2.R1.PROCESS.fastq",
    // "GGAAAGGACGAAACACCG");

    // ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN3.R1.fastq",
    // "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN3.R1.PROCESS.fastq",
    // "GGAAAGGACGAAACACCG");
    //
    // ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN4.R1.fastq",
    // "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN4.R1.PROCESS.fastq",
    // "GGAAAGGACGAAACACCG");
    //
    ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN5.R1.fastq",
    "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN5.R1.PROCESS1.fastq",
    "GGAAAGGACGAAACACCG");
    //
    // ProcessFastqFile("/home/akopp/Documents/Crispr_DATA/LTBN6.R1.fastq",
    // "/home/akopp/Documents/Crispr_DATA/PROCESS/LTBN6.R1.PROCESS.fastq",
    // "GGAAAGGACGAAACACCG");

    return 0;
}
