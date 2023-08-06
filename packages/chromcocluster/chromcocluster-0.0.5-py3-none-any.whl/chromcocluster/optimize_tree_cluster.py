import sys, os
import pandas as pd
import numpy as np
import multiprocessing
import copy

import chromcocluster.tree_cluster as tclust
import chromcocluster.utilities as utilities

# Optimize tree clustering
#
# public methods
# generate_starting_points : generate random and smart starting points
# optimize : runs an optimization using each starting point
# save : saves either starting points or fits to a file
# get_starting_points
# get_fits
#
# fits and starting points are given as a list of dictionaries.
# Dictionaries include "assignments" (1d array giving clustering),
# residual, generated (either "random", "smart" or "optimization")
#
# @param k number of clusters in tree
# @param g igraph object, must be a tree with one root
# @param m_list list of binary matrices to be column

class optimize_tree_cluster:

    def __init__(self, k, g, m_list, nCPU=1, random_seed=123):

        np.random.seed(random_seed)

        # check that g is a tree
        istree, root_node = utilities.find_root(g)
        if not istree:
            sys.exit("g does not describe a tree")
        self.rootnode = root_node

        self.nCPU = nCPU
        self.num_clusters = k
        self.ncol = m_list[0].shape[1]

        self.g = g
        self.m_list = m_list
        self.starting_points = None
        self.fits = None

        self.tree_cluster = tclust.tree_cluster(self.num_clusters,
                                                self.g,
                                                m_list)


    def generate_starting_points(self, n_random):
        rand_results = []
        treecluster = self.tree_cluster

        for i in range(n_random):
          treecluster.initialize_components()
          sp = {'assignments':treecluster.get_assignments(),
                'residual':treecluster.compute_residual2(),
                'generated':"random"}
          rand_results.append(sp)

        self.starting_points = rand_results
        self.fits = None

    def load_starting_points(self, infile):
        tb = pd.read_csv(infile, sep=",")

        res = tb["residual"].tolist()
        gen = tb["generated"].tolist()

        tb = tb.drop("residual", axis=1)
        tb = tb.drop("generated", axis=1)

        m = tb.values
        self.starting_points = [{'assignments':m[i,:],
                                 'residual':res[i],
                                 'generated':gen[i]} for i in range(len(tb))]
        self.fits = None

    def optimize(self):

        ic = self.get_starting_points()
        initial_assignments = np.array([r["assignments"] for r in ic])
        m_list = self.m_list

        packed_results = []
        if self.nCPU == 1:
          print("serial optimization...")
          for i in range(initial_assignments.shape[0]):
            packed_results.append(optimizeCluster(initial_assignments[0,:],
                        self.g, self.m_list, self.num_clusters))
        else:
          print("parallelizing optimization...")
          p = multiprocessing.Pool(processes=self.nCPU)
          gl = [copy.deepcopy(self.g) for i in range(len(ic))]
          m_list_l = [copy.deepcopy(m_list) for i in range(len(ic))]
          packed_results = p.starmap(optimizeCluster,
                                     zip(initial_assignments,
                                         gl,
                                         m_list_l,
                                         np.repeat(self.num_clusters,len(ic))))


        # need to unpack results...
        results = []
        for pr in packed_results:

          residual2 = pr[0]
          assignments = pr[1]

          # debug
          if np.any(assignments == -1):
              sys.exit("a column has not been assigned to a cluster!")

          results.append({'assignments':assignments,
                           'residual':residual2,
                           'generated':'optimization'})

        self.fits = results


    # accessor methods
    def get_starting_points(self, as_dataFrame=False):
        if  not as_dataFrame:
          out =  self.starting_points
        else:
          temp_file = "temp_sp_" + str(np.random.uniform()) + ".csv"
          self.save(temp_file, starting_points=True)
          out = pd.read_csv(temp_file, sep=",")
          os.remove(temp_file)

        return out

    def get_fits(self, as_dataFrame=False):
        if  not as_dataFrame:
          out =  self.fits
        else:
          temp_file = "temp_sp_" + str(np.random.uniform()) + ".csv"
          self.save(temp_file, fits=True)
          out = pd.read_csv(temp_file, sep=",")
          os.remove(temp_file)

        return out

    def get_optimal_assignments(self):

        if self.fits is None:
            print("Optimization has not been run")
            return None

        all_res = [x["residual"] for x in self.fits]
        best_fit_ind = np.argmin(all_res)

        return self.fits[best_fit_ind]["assignments"]

    # save either starting points or fits depending on flags
    def save(self, outfile, starting_points=False, fits=False):
        if not starting_points and not fits:
            sys.exit("one of starting ponts or fits flags must be set True")

        if starting_points:
            results = self.get_starting_points()
        else:
            results = self.get_fits()
        assign_m = np.array([r["assignments"] for r in results])
        res = [r["residual"] for r in results]
        gen = [r["generated"] for r in results]

        tb = pd.DataFrame(assign_m,
                          columns=self.g.vs["name"])
        tb.insert(tb.shape[1], "residual", res)
        tb.insert(tb.shape[1], "generated", gen)

        tb.to_csv(outfile,
                  sep=",",
                  index=False)




######################################################
# computational methods
# def computeCluster(cut_edges,g,m_list,num_clusters):
#     tc = tclust.tree_cluster(num_clusters, g, m_list)
#     tc.initialize_components(initial_cutedges = cut_edges)
#     return tc.compute_residual2(), tc.assignments

def optimizeCluster(assignments,g,m_list,num_clusters):
    tc = tclust.tree_cluster(num_clusters, g, m_list)
    tc.optimize(assignments = assignments)
    return tc.compute_residual2(), tc.assignments
