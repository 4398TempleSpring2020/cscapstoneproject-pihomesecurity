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
        data = []
        with open(files[0], "r") as sfile:
            lines = sfile.readlines()
            for(line in lines):
               data.append(int(line.strip())) 
        
        isAnom = False
        std = statistics.stdev(data)
        mean = statistics.mean(data)

        z = np.abs(stats.zscore(data))
        z_new = (z < 3).all(axis=0)
        
        return isAnom
