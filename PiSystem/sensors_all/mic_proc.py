import numpy as np
import os
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile

class MicProc():
    def plot_signals(self, x, x_lab, fig_title):
        n = len(x)
        plt.subplot(1,1,1)
        plt.title(fig_title)
        
        for i in range(n):
            plt.plot(x[i][1], label=x_lab[i])

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
            plt.plot(x[i][1], 'b-')
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
            fcontents.append(scipy.io.wavfile.read(curfile, mmap=False))
            fnames.append(fname)
        return(fcontents, fnames)

'''
if __name__ == "__main__":
    mic_dir = "../data/mic/"
    mic_signals, mic_names = get_files(mic_dir)

    plot_signals(mic_signals, mic_names, "Microphone Signals")
    plot_each_signals(mic_signals, mic_names, "Individual Microphone Signals")
'''
