import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.optimize
#from scipy.odr import ODR, Model, Data, RealData

def Lorentz_func(x, a, Gamma, x_0):

    return a*Gamma/(2*(x-x_0)**2+2*(1/2*Gamma)**2)

#def Lorentz_func(B, x):

#    return 1/(math.pi*2)*B[0]*B[1]/((x-B[2])**2+(1/2*B[1])**2)

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

def data_fit (x_min, x_max, x_temp, y_temp):
    
    x_temp1 = []
    y_temp1 = []
    x_plt = np.empty(len(x_temp), dtype = float)
    y_plt = np.empty(len(y_temp), dtype = float)

    x_plt[:] = x_temp
    y_plt[:] = y_temp

    for i in range(0, 1044):
        if x_max > float(x_temp[i]) > x_min:
            x_temp1.append(x_temp[i])
            y_temp1.append(y_temp[i])

    
    del x_temp
    del y_temp

    x_plt1 = np.empty(len(x_temp1), dtype = float)
    y_plt1 = np.empty(len(y_temp1), dtype = float)

    x_plt1[:] = x_temp1
    y_plt1[:] = y_temp1

    del x_temp1
    del y_temp1

    #data = RealData(x_plt1, y_plt1)
    #model = Model(Lorentz_func)
    #myodr = ODR(data, model, beta0=[1, 1, x_min])
    #myoutput = myodr.run()
    #plt.plot(x_plt, Lorentz_func(myoutput.beta, x_plt))

    params, params_cov = scipy.optimize.curve_fit(Lorentz_func, x_plt1, y_plt1,bounds=([0,0,x_min],[np.inf, np.inf, x_max]), sigma = None, absolute_sigma = True, method = 'trf')
    plt.plot(x_plt, Lorentz_func(x_plt, params[0], params[1], params[2]), label= r"Lorentz fit")
    perr = np.sqrt(np.diag(params_cov))/np.sqrt(len(x_plt1))
    print("Maximum position : " + str(params[2]) + "+/-" + str(perr[2]))


def plot_spectrum ():

    x_plt_temp = []
    y_plt_temp1 = []
    y_plt_temp2 = []
    y_plt_temp = []
    l = 1044 #number of recorded values
    x_plt = np.empty(l, dtype = float)
    y_plt = np.empty(l, dtype = float)

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
        y_plt_temp.append(float(y_plt_temp1[i]) - float(y_plt_temp2[i]))

    y_max = max(y_plt_temp)

    for i in range(0,l):
        y_plt_temp[i] = y_plt_temp[i]/(y_max)
    
    x_plt[:] = x_plt_temp
    y_plt[:] = y_plt_temp

    #create .csv file

    #with open('data.csv', 'w', newline='\n') as file:
    #    writer = csv.writer(file)
    #    for i in range(0, len(x_plt_temp)):
    #        writer.writerow([str(x_plt_temp[i]) + ";" + str(y_plt_temp[i])])

    plt.errorbar(x_plt, y_plt, yerr = None, fmt = 'o', markersize = .5)

    data_fit(507, 517, x_plt_temp, y_plt_temp)
    data_fit(545, 555, x_plt_temp, y_plt_temp)
    data_fit(555, 580, x_plt_temp, y_plt_temp)
    data_fit(633, 641.276, x_plt_temp, y_plt_temp)
    data_fit(645, 1000, x_plt_temp, y_plt_temp)

    del x_plt_temp
    del y_plt_temp

    plt.xlabel("Wavelength [nm]", fontsize=16)
    plt.ylabel("Photoluminescence intensity [a.u.]", fontsize=16)
    plt.grid()

    plt.show()
    plt.clf()

def main():
    plot_spectrum()

if __name__ == "__main__" :
    main()