import numpy as np
import igraph as ig

def find_root(g):
     # check that g is a tree
    parents = [len(g.neighbors(x, mode="IN")) for x in g.vs]
    if not set(parents) == set([0,1]):
        False, -1
    root_ind = np.where(np.array(parents)==0)[0]
    if not len(root_ind) == 1: 
        False, -1
        
    return True, root_ind[0]