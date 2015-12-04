#include <iostream>
#include "LineReader.h"
#include <string>
#include <string.h>
#include <unordered_map>
#include "tokenize.h"
#include <vector>

/*
Read a Fastq file and populate unordered_map with count of each different seq found in fastq file

 -> @ wikipedia
@EAS139:136:FC706VJ:2:2104:15343:197393 1:Y:18:ATCACG
EAS139 	the unique instrument name
136 	the run id
FC706VJ 	the flowcell id
2 	flowcell lane
2104 	tile number within the flowcell lane
15343 	'x'-coordinate of the cluster within the tile
197393 	'y'-coordinate of the cluster within the tile
1 	the member of a pair, 1 or 2 (paired-end or mate-pair reads only)
Y 	Y if the read is filtered, N otherwise
18 	0 when none of the control bits are on, otherwise it is an even number
ATCACG 	index sequence

@M01855:124:000000000-A7W1V:1:1101:18707:1016 1:N:0:0
CCTGACTGGCTTATCTGAAC
+
GGGGGGGGGGGGGGGGGGGG
@M01855:124:000000000-A7W1V:1:1101:19446:1017 1:N:0:0
TGTCATTCAGCCGTTCTAAG
+
GFGGGGGGGGGGGGGGGGGF


file_name : file path
ctab : unordered_map (dict) key are seq and value are count
trim : if seq must be trim at some position
*/
void ReadFastqFile(const char*file_name, std::unordered_map<std::string,int> &ctab, int trim){
    int nline = 0;
    int nreadcount = 0;
    io::LineReader in(file_name);

    // Parse all line of fastq file
    while(char*line = in.next_line()){
        nline += 1;

        // Get the id of read
        // if (nline%4 == 1){
        //     std::string readId = line;
        //
        //     std::vector<std::string> vec;
        //     tokenize(line, ": ", vec);
        //
        //     // for (auto i : vec)
        //     //     std::cout << i << " ";
        //     // std::cout << std::endl;
        //
        // }

        // Get the sequence of read
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

/*
Read a csv file for Crispr library (gecko)

gene_id,UID,seq
A1BG,HGLibA_00001,GTCGCTGAGCTCCGATTCGA
A1BG,HGLibA_00002,ACCTGTAGTTGCCGGCGTGC

file_name : file path
ctab : unordered_map populated by readfastqfile
trim : if seq must be trim at some position
*/
void ReadCripsrLib(const char*file_name, const std::unordered_map<std::string,int> &ctab, int trim){
    io::LineReader in(file_name);
    while(char*line = in.next_line()){
        // std::cout << line << std::endl;

        std::vector<std::string> vec;
        tokenize(line, ",", vec);

        auto __sgrna_pos = 2;
        auto __geneid_pos = 0;
        auto sgrnaseq = vec[__sgrna_pos];
        auto geneid = vec[__geneid_pos];

        // Print data of vec
        // for (auto i : vec)
        //     std::cout << i << " ";
        // std::cout << std::endl;

        // Try catch error if seq is smaller than trim
        try{
            sgrnaseq = sgrnaseq.substr(trim);
        }catch(const exception & e){
            std::cerr << sgrnaseq << " " << e.what() << std::endl;
        }

        // search seq in map, print gene, seq and cout if match
        auto search = ctab.find(sgrnaseq);
        if(search != ctab.end()) {
            std::cout << geneid << " " << sgrnaseq << " : " << search->second << std::endl;
        }
    }
}

int main(){
    auto trim = 0;
    std::unordered_map<std::string,int> ctab;

    auto File_Path = "/home/akopp/Documents/Crispr_Test/GeCKO_NatureMethods2014_fastq/HumanA_lentiCRISPRv2.fq";
    std::cout << "Read : " << File_Path << std::endl;
    ReadFastqFile(File_Path, ctab, trim);

    File_Path = "/home/akopp/Documents/Crispr_Test/GeCKO_NatureMethods2014_fastq/HumanB_lentiCRISPRv2.fq";
    std::cout << "Read : " << File_Path << std::endl;
    ReadFastqFile(File_Path, ctab, trim);

    // for (auto &itr : ctab){
    //         std::cout << itr.first << " : " << itr.second << std::endl;
    // }
    ReadCripsrLib("/home/akopp/Documents/Crispr_Test/Human_GeCKOv2_Library_A_09Mar2015.csv", ctab, trim);

    return 0;
}
