

def quantile_normalization(anarray):
    """
    anarray with samples in the columns and probes across the rows
    import numpy as np
    """
    A=anarray
    AA = np.zeros_like(A)
    I = np.argsort(A,axis=0)
    AA[I,np.arange(A.shape[1])] = np.mean(A[I,np.arange(A.shape[1])],axis=1)[:,np.newaxis]
    return AA
