import csv
import os
import matplotlib.pyplot as plt
import numpy as np
#import math

def reader (dirName):
    
    intensity = []
    wavelength = []
    #i = 0 #counts the files
    j = 0 #for skipping the first few lines
    #line = 0 #counts the lines in a file

    #for root, dirs, files in os.walk(dirName):
    #    for file in files:
    #        if file.endswith(".txt"):
    #            files.append(os.path.join(root, file))
    #            print(os.path.join(root, file))
    
     
    for root, dirs , files in os.walk(dirName):
        for file in files:
            if file.endswith(".txt"):
                print("Reading in file " + os.path.join(root, file))
                with open(os.path.join(root, file)) as f:
                    reader = csv.reader(f, delimiter = '\t')
                    for row in reader:
                        if j > 13:
                            #print(row[0])
                            #print(row[1])
                            intensity.append(row[1])
                            wavelength.append(row[0])
                        j += 1
                j = 0

    f.close()

    #for i in range(len(intensity)):
    #    print(intensity[i] + " ; " + wavelength[i])

    return intensity, wavelength

def plot_spectrum ():

    x_plt_temp = []
    y_plt_temp1 = []
    y_plt_temp2 = []
    y_plt_temp = []
    l = 1044 #number of recorded values
    x_plt = np.empty(1044, dtype = float)
    y_plt = np.empty(1044, dtype = float)

    PLspectrum = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum"
    PLbackground = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum_background"
    intensity_temp1, wavelength_temp1 = reader(PLspectrum)
    intensity_temp2, wavelength_temp2 = reader(PLbackground)
    
    #subtracting the background
    
    for i in range(0,l):
        y_plt_temp1.append(float(intensity_temp1[i]) + float(intensity_temp1[i+l]))
        x_plt_temp.append(wavelength_temp1[i])


    for i in range(0,l):
        y_plt_temp2.append(float(intensity_temp2[i]) + float(intensity_temp2[i+l]) + float(intensity_temp2[i+2*l]))

    for i in range(0,l):
        y_plt_temp.append(float(y_plt_temp1[i]) - float(y_plt_temp2[i]))


    x_plt[:] = x_plt_temp
    y_plt[:] = y_plt_temp

    plt.errorbar(x_plt, y_plt, yerr = None, fmt='x', markersize=.5)
    plt.xlabel("Wavelength [nm]", fontsize=16)
    plt.ylabel("Photoluminescence intensity [a.u.]", fontsize=16)
    plt.grid()

    plt.show()
    plt.clf()

def main():
    plot_spectrum()

if __name__ == "__main__" :
    main()