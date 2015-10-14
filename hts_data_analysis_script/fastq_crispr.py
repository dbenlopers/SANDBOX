#!/usr/bin/env python3
# encoding: utf-8

def mageckcount_processonefile(filename):
    '''
    Go through one fastq file
    Parameters
    ----------
    filename
    Fastq filename to be sequence
    genedict
    {sequence:(sgRNA_id,gene_id)} dictionary
    Return genedict
    '''
    SizeTable = {}
    ctab={}
    nline=0
    nreadcount=0
    for line in open(filename):
        nline=nline+1
        if nline%4 == 2:
            nreadcount+=1
            fseq=line.strip()
            if fseq not in ctab:
                ctab[fseq]=0
            ctab[fseq] += 1

            if len(fseq) not in SizeTable:
                SizeTable[len(fseq)] = 0
            SizeTable[len(fseq)] += 1
    print(SizeTable)
    return ctab

filename = "/home/arnaud/Downloads/HumanA_lentiCRISPRv2.fq"

countTable = mageckcount_processonefile(filename=filename)

sgRNA_File = "/home/arnaud/Downloads/human_geckov2_library_a_2.csv"

geneCnt = 0
MatchCnt = 0
MatchSum = 0

for line in open(sgRNA_File):
    field=line.strip().split(',')
    if len(field)<3:
        continue
    sgrnaseq = field[2].upper()
    geneid = field[0].upper()
    geneCnt += 1

    if sgrnaseq in countTable.keys():
        # print("Found {0} in countTable with {1} read, geneId is {2}".format(sgrnaseq, countTable[sgrnaseq], geneid))
        MatchCnt += 1
        MatchSum += countTable[sgrnaseq]

print("Number of different sequence in fastq file               : {}".format(len(countTable.keys())))
print("Number of sequence in fastq file                         : {}".format(sum(countTable.values())))
print("Number of match sgRNA in sequenced sequence              : {}".format(MatchCnt))
print("Number of different sgRNA                                : {}".format(geneCnt))
print("Sum of sequence that match with sgRNA                    : {}".format(MatchSum))
