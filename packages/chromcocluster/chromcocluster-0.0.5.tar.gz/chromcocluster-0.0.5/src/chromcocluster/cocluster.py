import chromcocluster.locus_cluster as lc
import chromcocluster.optimize_tree_cluster as optimize_tree_cluster
import chromcocluster.tree_cluster as tree_cluster

import igraph as ig
import matplotlib.pylab as plt
import os

import pandas as pd
import numpy as np
import seaborn as sns
import random


# @param matrix_file a csv file with header.  rows are loci,
# and columns are cell types.  Header row should contain
# cell type names
# @param graph_file a csv file containing two columns and a
# header (header is not used, but is assumed).
# Each row contains are start and end cell type
# (names must be in the header of matrix_file) that are
# connected by an edge
#
# @details The matrix and graph are restricted to shared
# cell types
class cocluster:

    def __init__(self,
                 graph_file,
                 matrix_file):


        df = pd.read_csv(matrix_file, header=0)

        e = pd.read_csv(graph_file, header=0)
        if e.shape[1] != 2:
            print("ERROR: edge file should contain exactly two colums!")
            return None
        # check that all nodes in graph are in the matrix
        # and vice verse
        df_names = set(df.columns)
        g_names = set(e.iloc[:,0]).union(e.iloc[:,1])

        joint_names = df_names.intersection(g_names)

        if len(joint_names) == 0:
            print("ERROR: graph nodes and matrix columns differ!")
            return None

        e.to_csv("temp_graph.csv", sep=" ", index=False,
                 header=False)
        g = ig.Graph.Read_Ncol("temp_graph.csv",
                               directed=True)
        os.remove("temp_graph.csv")

        g = g.induced_subgraph(joint_names)
        is_tree, root_ind = self.find_root(g)

        if not is_tree:
            print("ERROR: edges do not define a tree!")
            return None

        df = df.loc[:,g.vs["name"]]

        self.g = g
        self.m = df.to_numpy()

        self.locus_clusters = None
        self.cell_type_clusters = None
        self.cell_type_names = g.vs["name"]

        self.m_list = None
        self.m_list_approx = None
        self.locus_edges = None
        self.k = None

    # cluster methods

    def locus_cluster(self,
                      FDR=0.001,
                      min_accessible_cell_types=3,
                      max_accessible_cell_types=None,
                      min_cluster_size=30,
                      outfile=None):

        r = str(random.uniform(0,1))[2:12]
        null_directory = "temp_chromcocluster_null_distribution_" + r
        os.mkdir(null_directory)

        if max_accessible_cell_types is None:
            max_accessible_cell_types = self.m.shape[1] + 1 \
                                        - min_accessible_cell_types

        rc = lc.locus_cluster(self.m, FDR,
                        null_directory=null_directory,
                        min_accessible_cell_types=min_accessible_cell_types,
                        max_accessible_cell_types=max_accessible_cell_types,
                        min_cluster_size=min_cluster_size)

        os.environ["nd"] = null_directory
        os.system("rm -r $nd")

        self.locus_clusters = rc.clusters
        self.locus_edges = rc.edges
        self.m_list = rc.m_list
        
        if outfile is not None:
            self.locus_clusters.to_csv(outfile, sep=",", index=False)


    def cell_type_cluster(self, k, nCPU=1, ntrails=10,
                          outfile=None):

        if (k < 2):
            print("k must be greater than 2!")
            return None
        self.k = k

        if self.m_list is None:
            print("Locus clustering must be executed first.")
            return None

        otc = optimize_tree_cluster.optimize_tree_cluster(k=k,
                                                  g=self.g,
                                                  m_list=self.m_list,
                                                  nCPU=nCPU)
        otc.generate_starting_points(ntrails)
        otc.optimize()

        self.cell_type_clusters = otc.get_optimal_assignments()
        self.m_list_approx = self.form_cocluster_approximation()
        
        if outfile is not None:
          ctc = self.cell_type_clusters
          df = pd.DataFrame(ctc.reshape(-1, len(ctc)))
          df.columns = self.cell_type_names
          df.to_csv(outfile, index=False)
        

    # utility methods

    def find_root(self,g):
      # check that g is a tree
      parents = [len(g.neighbors(x, mode="IN")) for x in g.vs]
      if not set(parents) == set([0,1]):
          False, -1
      root_ind = np.where(np.array(parents)==0)[0]
      if not len(root_ind) == 1:
          False, -1

      return True, root_ind[0]


    def form_cocluster_approximation(self):

      k = self.k
      m_list = self.m_list
      assignments = self.cell_type_clusters

      nrc = len(m_list)
      ncc = k
      m_list_approx = []
      cocluster = np.zeros([nrc, len(assignments)])

      for r in range(nrc):
        approx_m = np.zeros(m_list[r].shape)
        for a in range(ncc):
          ind = (assignments==a)
          approx_m[:,ind] = approx_m[:,ind] + np.mean(m_list[r][:,ind])
          cocluster[r,ind] = np.mean(m_list[r][:,ind])
        m_list_approx.append(approx_m)

      return m_list_approx
  
    # public methods
  
    def load_clustering(self, 
                        locus_clusters_file, 
                        cell_type_clusters_file):
    
      locus_clusters = pd.read_csv(locus_clusters_file, sep=",")
      self.locus_clusters = locus_clusters
      m_list = []
      for cl in locus_clusters["cluster"].unique():
          c_lc = locus_clusters[locus_clusters["cluster"]==cl]
          c_lc.sort_values("row")
          m_list.append(self.m[c_lc["row"],:])
         
      self.m_list = m_list
      cell_type_clusters = pd.read_csv(cell_type_clusters_file).to_numpy()
      self.cell_type_clusters = cell_type_clusters.flatten()
      
      self.k = np.max(self.cell_type_clusters) + 1
      self.m_list_approx = self.form_cocluster_approximation()
       
    # visualization methods
    def plot_tree(self):

        if self.cell_type_clusters is None:
            print("Clustering has not been performed.")
            return None

        K = np.max(self.cell_type_clusters) + 1
        tc = tree_cluster.tree_cluster(K, self.g, self.m_list)
        tc.initialize_components(assignments=self.cell_type_clusters)

        tc.treeplot()

    def heatmap(self,
                cocluster_approximation=False,
                collapse_locus_clusters=False,
                outfile=None):

        if self.cell_type_clusters is None:
            print("Clustering has not been performed.")
            return None

        a = self.cell_type_clusters
        if cocluster_approximation:
            m_list = self.m_list_approx
        else:
            m_list = self.m_list

        if collapse_locus_clusters:
          m_list = [np.mean(x,0) for x in m_list]
          m = np.vstack(m_list)
        else:
          m = np.concatenate(m_list,0)

        # arrange by assignment order
        ct = pd.DataFrame({'index':range(len(a)),
                           'cluster':a})
        ct.sort_values("cluster",inplace=True)

        tb = pd.DataFrame(m[:,ct["index"]])
        tb.index = np.arange(m.shape[0])

        sns.clustermap(tb, row_cluster=False,
                       col_cluster=False)

        if outfile is None:
            plt.show()
        else:
            plt.savefig(outfile, bbox_inches='tight')

    # statistical methods
    def R2(self):

      m_list = self.m_list
      m_list_approx = self.m_list_approx
      mcc = [np.mean(x, 0) for x in m_list_approx]

      R2_total = []
      R2_column = []
      nr = len(m_list)

      for r in range(nr):

        m = m_list[r]
        mu = np.mean(m)
        mc_c = np.mean(m, axis=0)

        #total = np.var(m)
        within_ct = np.mean((m - mc_c)**2)
        # across_ct_captured
        across_ct_c = np.mean((mcc[r]-mu)**2)
        # across_ct_missed
        across_ct_m = np.mean((mc_c - mcc[r])**2)
        total_gen = within_ct + across_ct_c + across_ct_m

        R2_total.append(1 - (within_ct+across_ct_m)/total_gen)
        R2_column.append(1 - across_ct_m/(across_ct_c + across_ct_m))

      return pd.DataFrame({'locus_cluster':range(nr),
                        'R2_total':R2_total,
                        'R2_cell_type':R2_column})
