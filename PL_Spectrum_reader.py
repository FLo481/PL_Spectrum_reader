import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

def Gauss_func(x, y0, a, Gamma, x0):

    return (y0 + a*np.exp(-(x-x0)**2/(2*Gamma**2)))

#def Multi_Lorentz(x, *params):

#    return sum([Lorentz_func(x, *params[i:i+3] ) for i in range(0, 18, 3)])

def Multi_Gauss(x, *params):

    y = np.zeros_like(x)

    for i in range(0, len(params), 4):
        y0 = params[i]
        a = params[i+1]
        Gamma = params[i+2]
        x0 = params[i+3]

        y = y + Gauss_func(x, y0, a, Gamma, x0)

    return y

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

def csv_writer (x_plt, y_plt, y_plt_err):

    with open('data.csv', 'w', newline='\n') as file:
        writer = csv.writer(file)
        for i in range(0, len(x_plt)):
            writer.writerow([str(x_plt[i]) + ";" + str(y_plt[i]) + ";" + str(y_plt_err[i])])

        print("Data written to file %s" % "data.csv")

    file.close()

def data_fit (x_min, x_max ,x_plt, y_plt, y_err):
    
    initial_values = []
    x_plt1 = np.empty([], dtype = float)
    y_plt1 = np.empty([], dtype = float)
    y_err1 = np.empty([], dtype = float)

    for i in range(0, 1044):
        if x_max > x_plt[i] > x_min:
            x_plt1 = np.append(x_plt, x_plt[i])
            y_plt1 = np.append(y_plt, y_plt[i])
            y_err1 = np.append(y_err, y_err[i])

    num = 7

    x0_int_vals = [575,588,603,620,638,658,674]

    for i in range(num):
        initial_values +=[0.01, 0.1, 5, x0_int_vals[i]]

    lower = [-0.5, 0, 0, x_min]*num
    upper = [0.5, 1, 200, x_max]*num
    bounds = (lower, upper)

    #bounds = ([1,1,510,1,1,550,1,1,556,1,1,632,1,1,646],[np.inf,150,516,np.inf,150,555,np.inf,150,576,np.inf,150,641,np.inf,150,669])

    params, params_cov = scipy.optimize.curve_fit(Multi_Gauss, x_plt1, y_plt1, p0 = initial_values, sigma = y_err1, bounds = bounds, absolute_sigma = True)
    plt.plot(x_plt, Multi_Gauss(x_plt, *params), label = 'Commulative Gauss fit')

    for i in range(0, len(params), 4):
        plt.plot(x_plt, Multi_Gauss(x_plt, *params[i:i+4]))
        print(params[i+3])

    #print(params)

    #perr = np.sqrt(np.diag(params_cov))/np.sqrt(len(x_plt1))
    #print("Maximum position : " + str(params[2]) + "+/-" + str(perr[2]))

    #calculation of red. chi squared

    fit = np.empty(len(x_plt1), dtype = float)
    chi_squared = 0
    fit[:] = Multi_Gauss(x_plt1, *params)

    for i in range(0, len(x_plt1)):
        chi_squared += (y_plt1[i] - fit[i])**2/(y_err1[i])**2

    print("red. Chi squared : ",chi_squared/(len(x_plt1)-4))


def plot_spectrum ():

    x_plt_temp = []
    y_plt_temp = []
    y_plt_temp1 = []
    y_plt_temp2 = []
    y_plt_temp3 = []
    y_plt_err_temp = []
    y_plt_err_temp1 = []
    y_plt_err_temp2 = []
    y_plt_err_temp3 = []
    intensity_err1_1 = []
    intensity_err1_2 = []
    intensity_err2_1 = []
    intensity_err2_2 = []
    intensity_err2_3 = []
    l = 1044 #number of recorded values
    x_plt = np.empty(l, dtype = float)
    y_plt = np.empty(l, dtype = float)
    y_plt_err = np.empty(l, dtype = float)

    PLspectrum = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum"
    PLbackground = r"C:\Users\Flo\Desktop\F Praktikum\ODMR\Daten\PL_spectrum_background"
    intensity_temp1, wavelength_temp1 = reader(PLspectrum)
    intensity_temp2, wavelength_temp2 = reader(PLbackground)

    #calculating y uncertainties (Poisson uncertainties)

    intensity_temp1 = list(map(float, intensity_temp1 ))
    intensity_temp2 = list(map(float, intensity_temp2 ))

    for i in range(0,l):
        if intensity_temp1[i] > 0.0:
            intensity_err1_1.append(intensity_temp1[i]/(np.sqrt(intensity_temp1[i])))
        elif intensity_temp1[i] < 0.0:
            intensity_err1_1.append(0)
        if intensity_temp1[i+l] > 0.0:
            intensity_err1_2.append(intensity_temp1[i+l]/(np.sqrt(intensity_temp1[i+l])))
        elif intensity_temp1[i+l] < 0.0:
            intensity_err1_2.append(0)
        if intensity_temp2[i] > 0.0:
            intensity_err2_1.append(intensity_temp2[i]/(np.sqrt(intensity_temp2[i])))
        elif intensity_temp2[i] < 0.0:
            intensity_err2_1.append(0)
        if intensity_temp2[i+l] > 0.0:
            intensity_err2_2.append(intensity_temp2[i+l]/(np.sqrt(intensity_temp2[i+l])))
        elif intensity_temp2[i+l] < 0.0:
            intensity_err2_2.append(0)
        if intensity_temp2[i+2*l] > 0.0:
            intensity_err2_3.append(intensity_temp2[i+2*l]/(np.sqrt(intensity_temp2[i+2*l])))
        elif intensity_temp2[i+2*l] < 0.0:
            intensity_err2_3.append(0)
    
    #subtracting the background
    
    for i in range(0,l):
        y_plt_temp1.append(intensity_temp1[i] + intensity_temp1[i+l])
        x_plt_temp.append(wavelength_temp1[i])
        y_plt_temp2.append(intensity_temp2[i] + intensity_temp2[i+l] + intensity_temp2[i+2*l])

    for i in range(0,l):
        y_plt_temp3.append(y_plt_temp1[i] - y_plt_temp2[i])


    #error propagation
        
    for i in range(0,l):
        y_plt_err_temp1.append(np.sqrt((intensity_err1_1[i])**2 +(intensity_err1_2[i])**2))
        y_plt_err_temp2.append(np.sqrt((intensity_err2_1[i])**2+(intensity_err2_2[i])**2+(intensity_err2_3[i])**2))

    for i in range(0,l):
        y_plt_err_temp3.append(np.sqrt((y_plt_err_temp1[i])**2+(y_plt_err_temp2[i])**2))


    y_max = max(y_plt_temp3) 
    y_max_err = y_max/(np.sqrt(y_max))

    for i in range(0,l):
        y_plt_temp.append(y_plt_temp3[i]/(y_max))
        y_plt_err_temp.append(y_plt_temp[i]*np.sqrt((y_max_err/y_max)**2+(y_plt_err_temp3[i]/y_plt_temp3[i])**2))

   
    x_plt[:] = x_plt_temp
    y_plt[:] = y_plt_temp
    y_plt_err[:] = y_plt_err_temp

    #csv_writer(x_plt, y_plt, y_plt_err)

    #plot the spectrum

    plt.errorbar(x_plt, y_plt, yerr = y_plt_err, fmt = 'x', markersize = .5, label = '')

    #fitting and plotting the fits

    data_fit(555, 800, x_plt, y_plt, y_plt_err)

    del x_plt_temp
    del y_plt_temp
    del y_plt_temp1
    del y_plt_temp2
    del y_plt_temp3

    plt.xlabel("Wavelength [nm]", fontsize=16)
    plt.ylabel("PL intensity [arbitrary units]", fontsize=16)
    plt.grid()
    plt.legend()
    plt.xlim(500,900)

    plt.show()
    plt.clf()

def main():
    plot_spectrum()

if __name__ == "__main__" :
    main()