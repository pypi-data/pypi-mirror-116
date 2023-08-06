import os
import sys
import pandas as pd
import numpy as np
import random 


# @param bed_directory path to directory containing .bed files.
# All files with .bed suffix will be used in contstructing the
# accessibility matrix

# @param bad_column_indices a list of 5 ints specifying the columns
# (using 0-indexing) in the bed files that correspond to
# chr, chrStart, chrEnd, summit, and q.  
class accessibility_matrix:

    def __init__(self,
                 bed_directory,
                 bed_column_indices):


        if len(bed_column_indices) != 5:
            print("Four bed columns must be specified for",
                  "chr", "chrStart", "chrEnd", "summit", "q")
        self.bed_column_indices = bed_column_indices

        if not os.path.isdir(bed_directory):
            sys.exit("bed directory does not exist!")


        all_files = os.listdir(bed_directory)
        bd_files = [x for x in all_files if ".bed" in x]

        if len(bd_files) == 0:
          sys.exit("No .bed files in bed directory!")
        else:
          print("Detected", len(bd_files), "bed files")
        self.bed_files = [bed_directory + "/" + x for x in bd_files]

        peaks_list = []
        cell_type_names = []
        for f in self.bed_files:
         print("reading", f)
         p_df = pd.read_csv(f, sep="\t").iloc[:,self.bed_column_indices]
         p_df.columns = ["chr", "chrStart", "chrEnd", "summit", "q"]
         peaks_list = peaks_list + [p_df]
         cell_type_names = cell_type_names + [f[len(bed_directory)+1:len(f)-4]]

        self.peaks_list = peaks_list
        self.cell_type_names = cell_type_names
        self.m = None
        self.master_peaks = None


    def create_master_peak_list(self, 
                                master_bed_file,
                                window_radius=250):

      print("Gathering peaks across bed files...")
      master_peaks = pd.concat(self.peaks_list, 0)
      st = master_peaks["chrStart"]
      summit = master_peaks["summit"]
      
      d = pd.DataFrame({'chr':master_peaks["chr"],
                        'chrStart':st+summit-window_radius,
                        'chrEnd':st+summit+window_radius,
                        'q':master_peaks["q"]})
      d = d.sort_values(["chr", "chrStart"], 0)
      d.index = range(d.shape[0])

      merged_indices = []
      start_indices = []
      end_indices = []
      
      print("Building non-intersecting windows to cover peaks.")
      print("This may take a while!")
      

      all_chr = d["chr"].unique().tolist()
      for chr in all_chr:
        
        print("Building windows for", chr + "...")
        cd = d.loc[d["chr"] == chr]
        si = 0
        N = len(cd)
        while (si < N):
            #print([chr, si, N, cd.iloc[si]["chrStart"]])
            ei = self.find_intersection_range(cd, si, N)
            sub_cd_q = cd.iloc[si:ei]["q"]
            q_vals = sub_cd_q.idxmax()
            q_vals_i = si + np.argmax(sub_cd_q)

            merged_indices.append(q_vals)
            start_indices.append(si)
            end_indices.append(ei)
            si = self.find_intersection_range(cd, q_vals_i, N)

      d_filtered = d.iloc[merged_indices]
      d_filtered = d_filtered.sort_values(["chr", "chrStart"], 0)
      d_filtered.to_csv(master_bed_file, header=None, sep="\t", index=False)

      self.master_peaks = d_filtered

    def find_intersection_range(self, d, i, N):
      end_val = d.iloc[i]["chrEnd"]
      j = i+1
      while (j < N and d.iloc[j]["chrStart"] <= end_val):
          j = j + 1

      return (j)

    def create_accessibility_matrix(self,
                                    master_bed_file,
                                    matrix_csv_file,
                                    bedtools_path):


       r = str(random.uniform(0,1))[2:12]
       current_b = "temp_" + r + ".bed"
       current_s_b =  "temp_sorted_" + r + ".bed"
       current_c_b =  "temp_closest_" + r + ".bed"

       os.environ['mbf'] = master_bed_file
       os.environ['bedp'] = bedtools_path
       # cell type bed file
       os.environ["cb"] =  current_b
       # then sorted
       os.environ["csb"] = current_s_b
       # then with distance to master peaks
       os.environ["ccb"] = current_c_b

       nct = len(self.cell_type_names)
       loci_states = []
       for i in range(nct):

         print("processing cell type",
               self.cell_type_names[i] + ",",
               i+1, "of", nct)
         df = self.peaks_list[i]

         df.to_csv(current_b, sep="\t", header=None, index=False)
         os.system("sort -k1,1 -k2,2n -k3,3n $cb > $csb")

         os.system("$bedp closest -a $mbf -b $csb -d -t first > $ccb")
         df_cl = pd.read_csv(current_c_b, sep="\t", header=None)
         distances = df_cl.iloc[:,9]
         loci_states = loci_states + [np.int32(distances == 0)]

       os.system("rm $cb $csb $ccb")
       m = np.stack(loci_states).transpose()
       m_df = pd.DataFrame(m, columns=self.cell_type_names)

       m_df.to_csv(matrix_csv_file, index=False)
       self.m = m
