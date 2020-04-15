import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats
import statistics

class UltraProc():
    def plot_signals(self, x, x_lab, fig_title):
        plt.subplot(1,1,1)
        plt.title(fig_title)
        
        for i in range(len(x)):
            plt.plot(x[i], label=x_lab[i])
        plt.xlabel('time (s)')
        plt.ylabel('distance (cm)')
        plt.legend(loc='upper right', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
        plt.savefig('./all_ultra_signals.png')
        plt.show()

    def plot_each_signals(self, x, x_lab, fig_title):    
        n = len(x)
        plt.subplot(n,1,1)
        plt.title(fig_title)

        for i in range(n):
            # number of example digits to show
            plt.subplot(n, 1, i+1)
            plt.title(x_lab[i])
            plt.plot(x[i], 'b-')
        plt.xlabel('time (s)')
        plt.ylabel('distance (cm)')
        plt.legend(loc='upper right', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
        plt.savefig('./individual_ultra_signals.png')
        plt.show()

    def get_files(self, files):
        fcontents = []
        fnames = []
        for fname in files:
            curfile = fname
            with open(curfile, "r") as cf:
                cur = cf.readlines()
                cur.pop(0)
                curf = []
                for line in cur:
                    curf.append(float(line.strip()))

                fcontents.append(np.asarray(curf))
                fnames.append(fname)        
        return(fcontents, fnames)

    def isAnomaly(self, files):
        # read the data
        data, fname = self.get_files(files)
        data = data[0]

        # assume no anomaly
        isAnom = False

        # get the std and mean
        std = statistics.stdev(data)
        mean = statistics.mean(data)
        std_rat = std / mean

        if std_rat > .01:
            # find everything that is within 2 std of mean
            z = np.abs(stats.zscore(data))
            z_new = (z < 2)
            
            # find all points outside 2 std
            z_flip = []
            anom_indices = []
            for i,val in enumerate(z_new):
                if(val == True):
                    z_flip.append(False)
                else:
                    z_flip.append(True)
                    anom_indices.append(i)
                
            # select only outliars
            outliars = data[z_flip]
            
            # anom spacing of 1.5 seconds
            dist_thresh = 15
            chunks = []
            chunk = []
            for (i,val), outliar in zip(enumerate(anom_indices), outliars):
                if(len(chunk) == 0):
                    # initialize
                    prev = val
                    chunk.append(outliar)
                else:
                    # get distance from previous spike
                    distance = val - prev
                    if(distance < dist_thresh):
                        # if new spike is close add it to the chunk
                        chunk.append(outliar)
                    else:
                        # if spike is far, add it to different chunk
                        chunks.append(chunk[:])
                        
                        # reset our chunk
                        chunk = []
                        chunk.append(outliar)
                        
                if(i == len(anom_indices) -1):
                    chunks.append(chunk)
                prev = val

            # establish upper and lower bounds that are 4 standard deviations away
            thresh_up = mean + std*4
            thresh_down = mean - std*4

            # at least x consecutive samples needed
            count_thresh = 3

            # for every chunck of consecutive statistically significant data
            for chunk in chunks:
                # if we exceed count for consec, there is an anomaly
                if(len(chunk) >= count_thresh):
                    isAnom = True
        return isAnom
