import numpy as np
import os
import matplotlib.pyplot as plt

def plot_signals(x, x_lab, fig_title):
    plt.subplot(1,1,1)
    plt.title(fig_title)
    
    for i in range(len(x)):
        plt.plot(x[i], label=x_lab[i])
    plt.xlabel('time (s)')
    plt.ylabel('distance (cm)')
    plt.legend(loc='upper right', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
    plt.savefig('./all_ultra_signals.png')
    plt.show()

    
def plot_each_signals(x, x_lab, fig_title):    
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

def get_files(dname):
    fcontents = []
    fnames = []
    files = os.listdir(dname)
    for fname in files:
        curfile = dname + fname
        with open(curfile, "r") as cf:
            cur = cf.readlines()
            cur.pop(0)
            curf = []
            for line in cur:
                curf.append(float(line.strip()))

            fcontents.append(np.asarray(curf))
            fnames.append(fname)
            
    return(fcontents, fnames)
    
if __name__ == "__main__":
    ultra_dir = "../data/ultra/"
    ultra_signals, ultra_names = get_files(ultra_dir)

    plot_signals(ultra_signals, ultra_names, "Ultrasonic Sensor Signals")
    plot_each_signals(ultra_signals, ultra_names, "Individual Ultrasonic Sensor Signals")
