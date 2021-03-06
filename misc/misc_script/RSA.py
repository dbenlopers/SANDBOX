#!/usr/bin/env python3
# encoding: utf-8

import scipy.stats as ss
import numpy as np
import pandas as pd
import math
import argparse as arg

"""
usage: RSA.py [-h] [-l LB] [-u UB] [-r] [-o OUTPUT] [-R] [-g GENE] [-s SCORE]
              input

RSA prioritization of genes

positional arguments:
  input                 input file must a in CSV format

optional arguments:
  -h, --help            show this help message and exit
  -l LB, --lb LB        lower bound, defaults to 0
  -u UB, --ub UB        upper bound, defaults to 1
  -r, --reverse         reverse hit picking, the higher the score the better.
                        If -r flag is off, the lower the score the better
  -o OUTPUT, --output OUTPUT
                        output file name, STDOUT if not specified
  -R, --randomize       randomize score
  -g GENE, --gene GENE  column name for gene ID, default "Gene_ID"
  -s SCORE, --score SCORE
                        column name for score used for sorting, default
                        "Score"
  -b, --bonferroni      turn on Bonferroni correction, conceptually useful
                        when there are different number of siRNAs per gene.

Example

      RSA.py -l 0.2 -u 0.8 -o output.csv input.csv
      RSA.py -l 1.2 -u 2.0 -r -o output.csv input.csv

Input and Output Format:
========================
  Gene_ID,Score: columns from input spreadsheet
  LogP: OPI p-value in log10, i.e., -2 means 0.01;
  OPI_Hit: whether the well is a hit, 1 means yes, 0 means no;
  #hitWell: number of hit wells for the gene
  #totalWell: total number of wells for the gene
    if gene A has three wells w1, w2 and w3, and w1 and w2 are hits,
    #totalWell should be 3, #hitWell should be 2, w1 and w2 should have OPI_Hit set as 1
    and w3 should have OPI_Hit set as 0.
  OPI_Rank: ranking column to sort all wells for hit picking
  Cutoff_Rank: ranking column to sort all wells based on Score in the simple activity-based method

  Note: a rank value of 999999 means the well is not a hit. We put a large rank number here
  for the convenient of spreadsheet sorting.

  Examples A in output.csv:
  -------------------------
  1221200,0.0541,-6.810,1,3,3,1,33
  1221200,0.0626,-6.810,1,3,3,2,43
  1221200,0.0765,-6.810,1,3,3,3,72

  Gene ID 1221200 has three wells, 7_O20, 18_A21 and 41_A21. All show good scores.
  Therefore 3 out of 3 wells are hits (#totalWell=3, #hitWell=3, OPI_Hit=1 for all three wells)
  LogP is -6.810. These three wells are ranked as the best three wells by OPI.
  However, they are ranked as the 33th, 43th and 73th well by the traditional cutoff method.

  Examples B in output.csv:
  -------------------------
  3620,0.0537,-2.344,1,1,2,162,31
  3620,0.7335,-2.344,0,1,2,999999,4113

  Gene ID 3620 has two wells, 21_I17 is active, while 44_I17 is relative inactive.
  OPI decides that only 1 out of the 2 wells is a hit. Therefore one well has OPI_Hit set as 1,
  and the other 0. #totalWell=2, but #hitWell=1.
  The first well is the 162th hit by OPI, 31th by cutoff method.
  The second well is not a hit by OPI, 4113th by cutoff method.
"""

def error_msg(s_msg):
    print("ERROR> {}".format(s_msg))
    exit()

def lnbinomial(n, k):
    return math.lgamma(n+1)-math.lgamma(n-k+1)-math.lgamma(k+1)

def hyper(n, N, n1, n2, tolerance=1e-300, n_chunk=1000):
    '''
    N M_total: total number of objects in bin
    n1 n_white: total number of white objects in bin
    n2 N_pick: number of draws without replacement
    n x_white: x out of N_pick are white
    '''
    n_chunk=1000 if n_chunk<=0 else n_chunk
    min_idx=min(n1,n2)
    l_left=n*1.0/n1 < n2*1.0/N and n<min_idx-n+1
    term=1.0
    P=0.0 if l_left else 1.0 #when l_left, do not include pvalue2(N,n1,n2,n) itself
    if l_left:
        for x in range(n-1,-1,-n_chunk):
            ## vectorize in chunks of 1000
            ## in case N is huge, we stop when the remaining area is too small
            if term*(x+1)<tolerance: break # no need to run, too small already
            X=np.arange(x, max(-1, x-n_chunk), -1.0)
            X=(X+1)*(N-n1-n2+1+X)/(n1-X)/(n2-X)
            X=X.cumprod()*term
            term=X[-1]
            P+=X.sum()
    else:
        for x in range(n+1, min_idx+1, n_chunk):
            if term*(min_idx-x+1)<tolerance: break
            X=np.arange(x, min(min_idx+1, x+n_chunk), 1.0)
            X=(1+n1-X)*(1+n2-X)/X/(X+N-n1-n2)
            X=X.cumprod()*term
            term=X[-1]
            P+=X.sum()
    P*=math.exp(lnbinomial(n2,n)+lnbinomial(N-n2,n1-n)-lnbinomial(N,n1))
    return 1.0-P if l_left else P


#######################################################################################################################
#                        LEGACY CODE

def hyper_previous(n, N, n1, n2):
    '''
    N M_total: total number of objects in bin
    n1 n_white: total number of white objects in bin
    n2 N_pick: number of draws without replacement
    n x_white: x out of N_pick are white
    '''
    min_idx=min(n1,n2)
    l_left=n*1.0/n1 < n2*1.0/N and n<min_idx-n+1
    term=1.0
    P=0.0 if l_left else 1.0 #when l_left, do not include pvalue2(N,n1,n2,n) itself
    if l_left:
        for x in range(n-1,-1,-1):
            term*=(x+1.0)*(N-n2-n1+x+1.0)/(n1-x)/(n2-x)
            P+=term
    else:
        for x in range(n+1, min_idx+1):
            term*=(n1-x+1.0)*(n2-x+1.0)/x/(N-n2-n1+x)
            P+=term
    P*=math.exp(lnbinomial(n2,n)+lnbinomial(N-n2,n1-n)-lnbinomial(N,n1))
    return 1.0-P if l_left else P

def hyper_(x_white, M_total, n_white, N_pick):
    """This version is too slow"""
    '''
    M_total: total number of objects in bin
    n_white: total number of white objects in bin
    N_pick: number of draws without replacement
    x_white: x out of N_pick are white
    '''
    return ss.hypergeom.sf(x_white-1, M_total, n_white, N_pick)

#######################################################################################################################

def RSA_score(I_rank,N,i_min=None,i_max=None,l_BonferroniCorrection=False):
    cutoff=0
    logP_min=1.0
    n=len(I_rank);
    if i_max is None: i_max=n-1
    if i_min is None: i_min=0
    i_scale=(i_max-i_min+1) if l_BonferroniCorrection else 1
    for i in range(i_min,i_max+1):
        #print i, N, n, I_rank[i]
        #print ">>>>>>>", hyper(i+1, N, n, I_rank[i])*i_scale
        if (i<i_max) and (I_rank[i]==I_rank[i+1]): continue
        logP=math.log(np.max(hyper(i+1, N, n, I_rank[i]+1)*i_scale, 1e-100), 10)
        if (logP < logP_min):
            logP_min=logP
            cutoff=i
    return {'logP':logP_min, 'cutoff':cutoff}

def RSA(T, s_gene="GeneID", s_score="Score", l_reverse=False, LB=0.2, UB=0.8, l_randomize=False, l_BonferroniCorrection=False):
    t=T.copy()
    S=list(t.columns.values)
    #S=util.header(t)
    if t[s_gene].dtype is not np.dtype(object):
        t[s_gene]=t[s_gene].astype(str)
    t=t[ (pd.notnull(t[s_gene])) & (t[s_gene]!="") & (pd.notnull(t[s_score])) ]
    N=len(t)
    R_logP=np.zeros(N)
    R_bestActivity=np.zeros(N)
    I_hit=np.zeros(N).astype(int)
    I_totWell=np.zeros(N).astype(int)
    I_hitWell=np.zeros(N).astype(int)
    if l_randomize:
        R=t[s_score].values
        R=R[np.random.permutation(len(R))]
        t[s_score]=R
    t.sort_values(by=s_score, ascending=(not l_reverse), inplace=True)
    c_gene=dict()
    c_rank=dict()
    # we need to hash the max rank of a given score.
    # if t is a membership matrix, there are lots of ties, obtaining
    # c_rank can be the bottleneck
    c_score=dict()
    R_score=t[s_score].values
    for i in range(N):
        c_score[R_score[i]]=i

    for i in range(len(t)):
        s=t.iloc[i][s_gene]
        if s not in c_gene:
            c_gene[s]=[] # store the exact index for this gene
            c_rank[s]=[] # modify the rank, in case there are ties
        # updated on 10/19/2012
        c_gene[s].append(i)
        # the following can be the slowest part, if there are lots of ties
        #for j in xrange(i+1, N):
        #    if t[s_score].iloc[j]!=t[s_score].iloc[i]: break
        #c_rank[s].append(j-1)
        c_rank[s].append(c_score[R_score[i]])
    for s in c_gene:
        #if s!='19218': continue
        I_rank=c_rank[s]
        i_max=None
        i_min=None
        for k in range(len(I_rank)):
            if l_reverse:
                if R_score[I_rank[k]]>=LB: i_max=k
                if R_score[I_rank[k]]>=UB: i_min=k
                if (R_score[I_rank[k]]<LB and i_max is None): i_max=k-1
            else:
                if R_score[I_rank[k]]<=UB: i_max=k
                if R_score[I_rank[k]]<=LB: i_min=k
                if (R_score[I_rank[k]]>UB and i_max is None): i_max=k-1
        rslt=RSA_score(I_rank,N,i_min,i_max,l_BonferroniCorrection=l_BonferroniCorrection)
        logP=rslt['logP']
        cutoff=rslt['cutoff']
        I_idx=c_gene[s]
        for k in range(len(I_idx)):
            R_logP[I_idx[k]]=logP
            R_bestActivity[I_idx[k]]=R_score[I_idx[0]]
            I_hitWell[I_idx[k]]=cutoff+1
            I_totWell[I_idx[k]]=len(I_idx)
            if (k<=cutoff): I_hit[I_idx[k]]=1

    t["LogP"]=R_logP
    t["BestActivity"]=R_bestActivity
    t["RSA_Hit"]=I_hit
    t["#hitWell"]=I_hitWell
    t["#totalWell"]=I_totWell
    t.sort_values(by=['LogP',s_gene,s_score], ascending=[True, True, not l_reverse], inplace=True)
    #t["LogP"]=util.rarray2sarray(t["LogP"], s_format='%.4f')
    t["RSA_Rank"]=np.zeros(N).astype(int)+999999
    cnt=0
    for k in range(N):
        if t["RSA_Hit"].values[k]>0:
            cnt+=1
            t["RSA_Rank"].values[k]=cnt
    return t

if __name__=="__main__":
    opt=arg.ArgumentParser(description='RSA prioritization of genes')
    opt.add_argument('-l','--lb', type=float, default=0, help='lower bound, defaults to 0')
    opt.add_argument('-u','--ub', type=float, default=1, help='upper bound, defaults to 1')
    opt.add_argument('-r','--reverse', default=False, action='store_true', help='reverse hit picking, the higher the score the better. If -r flag is off, the lower the score the better')
    opt.add_argument('-o', '--output', help='output file name, STDOUT if not specified')
    opt.add_argument('-R', '--randomize', action='store_true', help='randomize score')
    opt.add_argument('-g','--gene', default='Gene_ID', help='column name for gene ID, default "Gene_ID"')
    opt.add_argument('-s','--score', default='Score', help='column name for score used for sorting, default "Score"')
    opt.add_argument('-b', '--bonferroni', default=False, action='store_true', help='turn on Bonferroni correction, conceptually useful when there are different number of siRNAs per gene.')
    opt.add_argument('input', nargs=1, help='input file must a in CSV format')

    args=opt.parse_args()
    geneColumn = args.gene
    scoreColumn= args.score
    if not args.input:
        error_msg("Input file must be specified!")
    s_outfile=args.output

    s_infile=args.input[0]
    t=pd.read_csv(s_infile)
    header=list(t.columns.values)
    if geneColumn not in header:
        error_msg("Missing column named %s!" % geneColumn)
    if scoreColumn not in header:
        error_msg("Missing column named %s!" % scoreColumn)

    #print args.reverse,  args.lb, args.ub, args.randomize
    T=RSA(t, s_gene=geneColumn, s_score=scoreColumn, l_reverse=args.reverse, LB=args.lb, UB=args.ub, l_randomize=args.randomize, l_BonferroniCorrection=args.bonferroni)
    T.LogP=T.LogP.apply(lambda x: '%.3f' % x)
    if s_outfile:
        T.to_csv(s_outfile, index=False)
    else:
        import cStringIO
        output = cStringIO.StringIO()
        T.to_csv(output, index=False)
        print(output.getvalue())
