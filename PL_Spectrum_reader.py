import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.optimize

def Lorentz_func(x, *P):

    return P[0]*P[1]/(2*(x-P[2])**2+2*(1/2*P[1])**2)

def Multi_Lorentz(x, *params):

    return sum([Lorentz_func(x, *params[i:i+3] ) for i in range(0, 12, 3)])

def reader (dirName):
    
    intensity = []
    wavelength = []
    j = 0 #for skipping the first few lines
    
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

def csv_writer (x_plt_temp, y_plt_temp):

    with open('data.csv', 'w', newline='\n') as file:
        writer = csv.writer(file)
        for i in range(0, len(x_plt_temp)):
            writer.writerow([str(x_plt_temp[i]) + ";" + str(y_plt_temp[i])])

def data_fit (x_min, x_max ,x_temp, y_temp, y_err_temp):
    
    x_temp1 = []
    y_temp1 = []
    y_err_temp1 = []
    initial_values = []
    x_plt = np.empty(len(x_temp), dtype = float)
    y_plt = np.empty(len(y_temp), dtype = float)

    x_plt[:] = x_temp
    y_plt[:] = y_temp

    for i in range(0, 1044):
        if x_max > float(x_temp[i]) > x_min:
            x_temp1.append(x_temp[i])
            y_temp1.append(y_temp[i])
            y_err_temp1.append(y_err_temp[i])

    
    del x_temp
    del y_temp
    #del y_err_temp

    x_plt1 = np.empty(len(x_temp1), dtype = float)
    y_plt1 = np.empty(len(y_temp1), dtype = float)
    y_err_plt1 = np.empty(len(y_temp1), dtype = float)

    x_plt1[:] = x_temp1
    y_plt1[:] = y_temp1
    y_err_plt1[:] = y_err_temp1

    del x_temp1
    del y_temp1

    num = 5

    for i in range(num):
        initial_values +=[1, 10, x_min+i*18]

    lower = (0, 0, x_min)*num
    upper = (np.inf, 150, x_max)*num
    bounds = (lower, upper)

    #bounds = ([1,1,510,1,1,550,1,1,556,1,1,632,1,1,646],[np.inf,150,516,np.inf,150,555,np.inf,150,576,np.inf,150,641,np.inf,150,669])

    params, params_cov = scipy.optimize.curve_fit(Multi_Lorentz, x_plt, y_plt, p0 = initial_values, bounds = bounds, sigma = y_err_temp, absolute_sigma = True, method = 'dogbox', maxfev=9999)
    #plt.plot(x_plt, Multi_Lorentz(x_plt, *params[3:]))
    #plt.plot(x_plt, Multi_Lorentz(x_plt, *params[:3]))
    plt.plot(x_plt, Multi_Lorentz(x_plt, *params))

    for i in range(0,len(params),3):
        print(params[i+2])

    #perr = np.sqrt(np.diag(params_cov))/np.sqrt(len(x_plt1))
    #print("Maximum position : " + str(params[2]) + "+/-" + str(perr[2]))


def plot_spectrum ():

    x_plt_temp = []
    y_plt_temp1 = []
    y_plt_temp2 = []
    y_plt_temp3 = []
    y_plt_temp = []
    y_plt_err_temp = []
    l = 1044 #number of recorded values
    x_plt = np.empty(l, dtype = float)
    y_plt = np.empty(l, dtype = float)
    y_plt_err = np.empty(l, dtype = float)

    PLspectrum = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum"
    PLbackground = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum_background"
    intensity_temp1, wavelength_temp1 = reader(PLspectrum)
    intensity_temp2, wavelength_temp2 = reader(PLbackground)
    
    #subtracting the background
    
    for i in range(0,l):
        y_plt_temp1.append(float(intensity_temp1[i]) + float(intensity_temp1[i+l]))
        x_plt_temp.append(wavelength_temp1[i])
        y_plt_temp2.append(float(intensity_temp2[i]) + float(intensity_temp2[i+l]) + float(intensity_temp2[i+2*l]))

    for i in range(0,l):
        y_plt_temp3.append(float(y_plt_temp1[i]) - float(y_plt_temp2[i]))

    y_max = max(y_plt_temp3) 
    y_max_err = y_max/(np.sqrt(y_max))

    for i in range(0,l):
        y_plt_temp.append(y_plt_temp3[i]/(y_max))
        if float(y_plt_temp3[i]) >= 0.0:
            y_plt_err_temp.append(y_plt_temp[i]/(np.sqrt(y_plt_temp[i])))
        elif float(y_plt_temp3[i]) < 0.0:
            y_plt_err_temp.append(0)
        y_plt_err[i] = y_plt_temp[i]*np.sqrt((y_max_err/y_max)**2+(y_plt_err_temp[i]/y_plt_temp3[i])**2)

   
    x_plt[:] = x_plt_temp
    y_plt[:] = y_plt_temp

    #csv_writer(x_plt_temp, y_plt_temp)

    #plot the spectrum

    plt.errorbar(x_plt, y_plt, yerr = y_plt_err, fmt = 'o', markersize = .5)

    #fitting and plotting the fits

    data_fit(500, 950, x_plt_temp, y_plt_temp, y_plt_err)

    del x_plt_temp
    del y_plt_temp
    del y_plt_temp1
    del y_plt_temp2
    del y_plt_temp3

    plt.xlabel("Wavelength [nm]", fontsize=16)
    plt.ylabel("Photoluminescence intensity [a.u.]", fontsize=16)
    plt.grid()

    plt.show()
    plt.clf()

def main():
    plot_spectrum()

if __name__ == "__main__" :
    main()