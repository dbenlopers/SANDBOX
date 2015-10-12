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
            ctab[fseq]=ctab[fseq]+1
    return ctab

filename = "/home/arnaud/Downloads/HumanB_lentiGuidePuro.fq"

countTable = mageckcount_processonefile(filename=filename)

sgRNA_File = "/home/arnaud/Downloads/human_geckov2_library_a_2.csv"
for line in open(sgRNA_File):
    field=line.strip().split(',')
    if len(field)<3:
        continue
    sgrnaseq = field[2].upper()
    geneid = field[0].upper()
    if sgrnaseq in countTable.keys():
        print("Found {0} in countTable with {1} read, geneId is {2}".format(sgrnaseq, countTable[sgrnaseq], geneid))
