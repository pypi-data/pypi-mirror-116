import numpy as np
import pandas as pd
import os
from scipy.stats import hypergeom

            
# Constructs null distribution for row clustering
#
# dist(k, n, N) = probability of k overlaps between two rows with n and
# N 1's, respectively.
#
# @param ncell number of cell types in accessibility matrix
# @param null_directory directory in which null distributions will be saved,
# this directory is created if it does not exist.
#
# This class computes the value dist(k,n,N) over all k,n,N from 0,1,2,...ncell
# The two-d array for dist(-,n,-) is saved to a file for each value of n
# in null_directory.
class null_locus_cluster:
    #null_peak_cluster_directory = conf.DATA_DIR + "null_row_cluster/"
   
    def __init__(self, ncell, null_directory):
      
        self.max_val = ncell
        self.null_directory = null_directory
        
        if not os.path.isdir(self.null_directory):
            os.mkdir(self.null_directory)   
        print("computing null distribution...")
        self.create_distance_distribution_matrices()
        
    # Compute distribution of hamming distance for two rows with n and N 1's,
    # respectively, under the null hypergeometric
    #    
    # k ~ hypergeometric(M, n, N) gives number of 1's that agree
    # notation follows python hypergeom parameters
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html
    # M = number of cell types 
    # n = number of 1's in one row
    # N = number of 1's in other row
            
    # k = number of shared 1's between the two rows
    # hamming distance = (n - k) + (N-k)
    def compute_distance_distribution(self, M, n, N):
        allk = range(M+1)
        pmf = hypergeom.pmf(allk, M, n, N)
        
        dist = np.zeros(M+1)
        for k in range(np.min([M, n+N])):
            hamming_dist = np.int32((n-k) + (N-k))
            if hamming_dist > M:
                hamming_dist = M
            if hamming_dist < 0:
                hamming_dist = 0
            dist[hamming_dist] = dist[hamming_dist] + pmf[k]
            
        return dist
    
    # compute dist(-,n,-) over all n
    def compute_distance_distribution_matrix(self, N):
        M = self.max_val
        distm = np.zeros([M,M+1])
        for n in range(M):
            distm[n,:] = self.compute_distance_distribution(M, n, N)
            
        return distm
            
    def create_distance_distribution_matrices(self):
        for N in range(self.max_val+1):
            #print(["creating distance matrix", N])
            d = self.compute_distance_distribution_matrix(N)
          
            cls = ["dist" + str(i) for i in range(d.shape[1])]
            tb = pd.DataFrame(d, columns=cls)
            
            outf = self.null_directory \
                        + "/distance_distribution_" + str(N) + ".csv"
            tb.to_csv(outf, sep=",", index=False)
            
    def load_distribution(self, N):
         outf = self.null_directory \
                        + "/distance_distribution_" + str(N) + ".csv"
         return pd.read_csv(outf, sep=",").to_numpy()
    
            
    
    
    
  