import chromcocluster.null_locus_cluster as nrc

import numpy as np
import pandas as pd
from sknetwork.clustering import Louvain
from scipy.sparse import csr_matrix

# Create row clusters from a binary master
#
# @param m a binary matrix
# @param FDR the FDR with which edges are called between rows
# @param null_directory a work directory in which files
# providing the null distribution will be written,
# @param homo_cutoff only consider rows with more than this many 1's
# and 0's.  Rows with < homo_cutoff 1's are ignored.  Rows with >
# m.shape[1] - homo_cutoff 1's are grouped together in a single
# cluster
class locus_cluster:

    def __init__(self, m, FDR,
                 null_directory="null_distribution_files",
                 min_accessible_cell_types=3,
                 max_accessible_cell_types=None,
                 min_cluster_size=20):

        self.np = nrc.null_locus_cluster(m.shape[1], null_directory)
        if max_accessible_cell_types is None:
          max_accessible_cell_types = m.shape[1] - (min_accessible_cell_types - 1)

        # binary matrix
        self.m = m.astype("float")
        self.FDR = FDR
        self.min_accessible_cell_types = min_accessible_cell_types
        self.max_accessible_cell_types = max_accessible_cell_types

        self.min_cluster_size = min_cluster_size

        self.edges = self.compute_edges()
        self.clusters = self.compute_clusters(self.edges)

        df = self.clusters
        cluster_numbers = df["cluster"].unique()
        m_list = []
        for clust in cluster_numbers:
           cluster_rows = df[df["cluster"]==clust]["row"]
           m_list = m_list + [m[cluster_rows,:]]
        self.m_list = m_list

    # computation methods
    def compute_edges_between_blocks(self, n1, n2, FDR):

        m = self.m
        nc = m.shape[1]

        ind1 = (np.where(np.sum(m, 1) == n1))[0]
        mm1 = m[ind1,:]
        N1 = len(mm1)

        ind2 = (np.where(np.sum(m, 1) == n2))[0]
        mm2 = m[ind2,:]
        N2 = len(mm2)

        dist_m = np.dot(mm1, np.transpose(1 - mm2)) \
                 + np.dot(1-mm1, np.transpose(mm2))
        if n1 == n2:
          np.fill_diagonal(dist_m, nc)

        # get the sampled distance counts
        dc = np.zeros([N1, nc+1])
        for k in range(N1):
          cc = np.unique(dist_m[k,:], return_counts=True)
          ind = np.int32(cc[0])
          dc[k,ind] = dc[k,ind] + cc[1]

        null_dist_pmf = self.np.load_distribution(n2)[n1,:]
        null_dc = N2*null_dist_pmf
        null_cumsum = np.cumsum(null_dc)

        cutoffs = np.zeros(N1)

        for i in range(N1):
            sample_cumsum = np.cumsum(dc[i,:])
            pass_FDR = np.where((null_cumsum <= sample_cumsum*FDR) &
                                (sample_cumsum > 0))[0]
            if len(pass_FDR) == 0:
                cutoffs[i] = -1
            else:
                cutoffs[i] = np.max(pass_FDR)

        e1 = []
        e2 = []

        for i in range(N1):
            ce2 = np.where(dist_m[i,:] <= cutoffs[i])[0]
            if not len(ce2) == 0:
                e1 = e1 + np.repeat(i, len(ce2)).tolist()
                e2 = e2 + ce2.tolist()

        if len(e1) == 0:
            return None

        edge_d = pd.DataFrame({'e1':ind1[e1], 'e2':ind2[e2]})
        if  n1 == n2:
           edge_d = edge_d.loc[edge_d["e1"] < edge_d["e2"]]

        return edge_d


    def compute_edges(self):

        print("computing graph for Louvain clustering...")
        FDR = self.FDR
        nc = self.m.shape[1]

        min_n = self.min_accessible_cell_types
        max_n = self.max_accessible_cell_types

        edges = []
        for n1 in range(min_n, max_n+1):
          for delta in [0,1]:
           n2 = n1 + delta
           if n2 <= max_n:
             if n1 == n2:
              print("computing edges between loci accessible in",
               n1, "cell types.")
             else:
              print("computing edges between loci accessible in",
               n1, "and", n2, "cell types.")
             ce = self.compute_edges_between_blocks(n1, n2, FDR)
             if not ce is None:
               print("found", len(ce), "edges.")
               edges.append(ce)
             else:
               print("found", 0, "edges.")

        all_edges = pd.concat(edges)
        return all_edges


    def louvain(self, edges):

        unique_edges = set(edges.iloc[:,0].to_list() +
                           edges.iloc[:,1].to_list())
        unique_edges = sorted(unique_edges)
        nv = len(unique_edges)
        ud = pd.DataFrame({'e1':unique_edges})
        ud = ud.reset_index(drop=False)

        e1_list = edges.merge(ud, how="left")["index"].to_list()
        ud = ud.rename({'e1':'e2'}, axis=1)
        e2_list = edges.merge(ud, how="left")["index"].to_list()

        values = np.repeat(1, len(edges))

        m = csr_matrix((values, (e1_list, e2_list)),
                       shape=(nv, nv))

        louvain = Louvain(verbose=True)
        labels = louvain.fit_transform(m)

        cluster_d = pd.DataFrame({'row':unique_edges,
                          'cluster':labels}).sort_values(["cluster","row"])

        return cluster_d


    def compute_clusters(self, edges, homo_cutoff=2):

        print("calling Louvain function from sknetwork...")
        cluster_d = self.louvain(edges)
        print("Louvain algorithm complete.")

        # get rows that are mostly open
        m = self.m
        homo_open = np.where(np.sum(m, 1) > self.max_accessible_cell_types)[0]
        d_homo = pd.DataFrame({'row':homo_open,'cluster':-1})

        cluster_d.loc[~cluster_d["row"].isin(homo_open)]

        joint = d_homo.append(cluster_d)
        joint["cluster"] = joint["cluster"] + 1
        joint = joint.sort_values("cluster")

        # find big clusters
        clust_counts = joint["cluster"].value_counts()
        min_c = self.min_cluster_size
        big_clusters = clust_counts[clust_counts > min_c].index
        joint = joint[joint["cluster"].isin(big_clusters)]

        return joint
