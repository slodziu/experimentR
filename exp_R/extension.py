import numpy as np
import statistics
import matplotlib.pyplot as plt
countRates = [3298.96006292056,
4063.01233159883,
4793.16571241913,
5838.30523934957,
7653.76750421364,
10787.4794927215,
17305.4198015451,
33130.6721360773]
for i in range(len(countRates)):
    countRates[i] = countRates[i]/300

SrActivity = 2093.4
NaActivity = 2915.5
def fracCalc(x):
    return 0.5 - x/(2*np.sqrt(x**2+(14.3E-3)**2))
def effCalcGraph(x,counts, activity):
    return (counts-0.3317)/(fracCalc(x)*activity)


def read_txt_file(txt_file):
    """
    Read a text file where each line contains one number and put each number into a list.
    
    Parameters:
        txt_file (str): Path to the input text file.
        
    Returns:
        list: List containing numbers read from the text file.
    """
    data = []
    with open(txt_file, 'r') as f:
        for line in f:
            data.append(float(line.strip()))
    return data
offsetVals = np.linspace(0, 0.015, 100)
def slopeAt(x):
    return 9.2+x*-0.00514
#Attenuation Coeff
def attenuation():

    thicknessData = read_txt_file("thickness.txt")
    thickArr = np.linspace(min(thicknessData),max(thicknessData),1000)
    LOBF = slopeAt(thickArr)
    thickCounts = read_txt_file("logCount.txt")
    thickCountErr = read_txt_file("logCountErr.txt")
    plt.plot(thicknessData,thickCounts, 'o', markersize = 3,color = "blue", label = "Experimental Data")
    plt.plot(thickArr,LOBF, label = r"Best Fit Line; $y=-0.00514x +9.2$", color = "black")
    plt.errorbar(thicknessData,thickCounts, yerr = thickCountErr,fmt = 'none',capsize=6,color = "blue")
    plt.xlabel(r"Mass Thickness (g/cm$^{2}$)")
    plt.ylabel("Logarithmic Counts")
    plt.legend()
    plt.savefig("attenuation.png",dpi=300)
attenuation()
Data = read_txt_file("extData.txt")
fracData = []
for i in range(len(Data)):
    fracData.append(fracCalc(Data[i]))
def effCalc(ndata,offset):
    pltData = []
    for i in range(len(ndata)):
        print(ndata[i])
        ndata[i] = ndata[i] - offset
        pltData.append(ndata[i])
        ndata[i] = 0.5 - ndata[i]/(2*np.sqrt(ndata[i]**2+(14.3E-3)**2))
        ndata[i] = (countRates[i]-0.3317)/(ndata[i]*2093.4)
    return ndata, pltData

effData = []
meanEff = []
for i in range(len(fracData)):
    effData.append((countRates[i]-0.3317)/(fracData[i]*2093.4))
for i in range(len(offsetVals)):
    Data = read_txt_file("extData.txt")
    effData,plotData = effCalc(Data,offsetVals[i])
    meanEff.append(max(effData)-min(effData))
    plt.plot(plotData,effData,label = "Offset: "+str(round(offsetVals[i],2))+ "m")
plt.legend()
plt.xlabel("Distance from Detector (m)")
plt.ylabel("Efficiency")
plt.savefig("extension.png",dpi=300)
plt.close()
print('Absolute Efficiency Max Value Differences: ')
print(max(meanEff))
index_min = meanEff.index(min(meanEff))
print("Offset Val for Min Efficiency Value Difference:")
print(offsetVals[index_min])
plt.plot(offsetVals,meanEff,label = "Largest Efficiency Value Difference")
plt.axvline(x=0.00552, color='r', linestyle='-',label = "Extrapolated Offset Value; $x=0.005524$m")
plt.axvline(x=0.0016666666666666666, color='green', linestyle='-',label = "Minimum Efficiency Value Difference Offset; $x=0.00167$m")
plt.xlabel("Detector Offset Value (m)")
plt.ylabel("Absolute Largest Efficiency Value Difference")
plt.legend()
plt.savefig("meanEff.png",dpi=300)



#Two axis inverse square law
def calculate_y(x):
    return 9.39776 * x**(-1.84833)
def calcNa(x):
    return 20.1 * x**(-0.8)
counts = read_txt_file("invSquareCount.txt")
NaCounts = read_txt_file("invSqSodiumCounts.txt")
NaDist = read_txt_file("invSqSodiumDist.txt")
NaXErr = []
for i in range(len(NaCounts)):
    NaXErr.append(2E-4*i)
NaErr = read_txt_file("invSqSodiumYErr.txt")
disances = read_txt_file("invSquareDistance.txt")
yErr = read_txt_file("invSquareErrCount.txt")
x_errors = read_txt_file("invSquareErrX.txt")
distArr = np.linspace(min(NaDist),max(disances),1000)
fitLine = calculate_y(distArr)
naFit = calcNa(distArr)
fig, ax1 = plt.subplots()

ax1.plot(distArr,fitLine,label = r"Thallium Best fit function; $y = 9.4x^{-1.848}$",color = "black")
ax1.plot(disances,counts, 'o', label = "Thallium Data", color = "blue")
ax1.errorbar(disances,counts, xerr=x_errors,yerr = yErr,fmt = 'none',capsize=6,color = "blue")
ax2 = ax1.twinx()
ax2.plot(distArr,naFit,label = r"Sodium Best fit function; $y = 20.1x^{-0.769}$", color = "green")
ax2.plot(NaDist,NaCounts, 'o', label = "Sodium Data", color = "red")
ax2.errorbar(NaDist,NaCounts, xerr=NaXErr, yerr = NaErr,fmt = 'none',capsize=6,color = "red")


ax1.set_ylabel("Thallium Counts", color='tab:blue')
ax1.set_xlabel("Distance from Detector (m)")
ax1.tick_params(axis='y', labelcolor='tab:blue') 
ax2.set_ylabel("Sodium Counts", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red') 
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')
plt.savefig("invSquare.png",dpi=300)
plt.xlabel("Distance from Detector (m)")


#Efficiency

NaEff = []
SrEFf = []
for i in range(len(NaCounts)):
    NaEff.append(effCalcGraph(NaDist[i],NaCounts[i],NaActivity))
for i in range(len(counts)):
    SrEFf.append(effCalcGraph(disances[i],counts[i],SrActivity))
NaEff = np.array(NaEff)
SrEFf = np.array(SrEFf)
NaEffErr = []
SrEffErr = []
for i in range(len(NaEff)):
    NaEffErr.append(1)
for i in range(len(SrEFf)):
    SrEffErr.append(0.7)
NaEffErr = np.array(NaEffErr)
SrEffErr = np.array(SrEffErr)
meanNaEff = np.mean(NaEff) 
meanNaEffErr = np.sqrt(np.sum(NaEffErr**2)/len(NaEff))
meanSrEff = np.mean(SrEFf)
meanSrEffErr = np.sqrt(np.sum(SrEffErr**2)/len(SrEFf))
fig, ax1 = plt.subplots()
ax1.plot(NaDist,NaEff,label = r"$\gamma$ Efficiency", color = "blue")
ax1.errorbar(NaDist,NaEff, xerr=NaXErr, yerr=NaEffErr,fmt = 'none',capsize=6,color = "blue")
ax2 = ax1.twinx()
ax2.plot(disances,SrEFf,label = r"$\beta^{-}$ Efficiency",color = "red")
ax2.errorbar(disances,SrEFf, xerr=x_errors,yerr=SrEffErr, fmt = 'none',capsize=6,color = "red")
ax1.set_ylabel(r"$\gamma$ Efficiency $\epsilon_{\gamma}$ ($\%$)", color='blue')
ax1.set_xlabel("Distance from Detector (m)")
ax1.tick_params(axis='y', labelcolor='blue') 
ax2.set_ylabel(r"$\beta^{-}$ Efficiency $\epsilon_{\beta^{-}}$($\%$)", color='red')
ax2.tick_params(axis='y', labelcolor='red') 
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.savefig("efficiency.png",dpi=300)



#Range
def slope1(x):
    return 18.229-x*3.856
def slope2(x):
    return 253.36-x*75.8
def find_intersections(func1, func2, x_range):
    """
    Find the x-coordinates of the intersection points of two functions within a given range.
    """
    intersections = []
    for x in x_range:
        y1_val = func1(x)
        y2_val = func2(x)
        if abs(y1_val - y2_val) < 1e-3:  # Check if the difference is within a small tolerance
            intersections.append(x)
    return intersections
intersect = find_intersections(slope1,slope2,np.linspace(2,5,100000))
print("Intersection Point: "+str(intersect))
RangePoint = [round(intersect[0],3), round(slope1(intersect[0]),3)]
plt.close()
plt.close(fig)
rangeWidths = read_txt_file("RangeWidth.txt")
rangeCounts = read_txt_file("RangeCounts.txt")
rangeCountsErr = read_txt_file("RangeCountErr.txt")
widthVals2= np.linspace(min(rangeWidths),3.3,1000)
widthVals1 = np.linspace(3.1,max(rangeWidths),1000)
line1 = slope1(widthVals1)
line2 = slope2(widthVals2)
fig2, ax3 = plt.subplots()
ax3.plot(RangePoint[0],RangePoint[1], 'o', markersize = 7,color = "red", label = f"Intersection Point; x={RangePoint[0]}mm",zorder=10)
ax3.plot(widthVals1,line1,label = r"Best fit function; $y = 18.229-3.856x$", color = "green")
ax3.plot(widthVals2,line2,label = r"Best fit function; $y = 253.36-75.8x$", color = "blue")
ax3.plot(rangeWidths,rangeCounts, 'o', markersize = 3,color = "black", label = "Experimental Data")
ax3.errorbar(rangeWidths,rangeCounts, yerr = rangeCountsErr,fmt = 'none',capsize=6,color = "black")
ax3.set_xlabel("Aluminium Width (mm)")
ax3.set_ylabel("Corrected Counts")
ax3.legend()
plt.savefig("range.png",dpi=300)
plt.show()


#Efficiency Print Statements
print("Mean Na Efficiency: ")
print(meanNaEff)
print("Mean Na Efficiency Error: ")
print(meanNaEffErr)
print("Mean Sr Efficiency: ")
print(meanSrEff)
print("Mean Sr Efficiency Error: ")
print(meanSrEffErr)
print("Na Eff Min Value: ")
print(min(NaEff))
print("Na Eff Max Value: ")
print(max(NaEff))
print("Sr Eff Min Value: ")
print(min(SrEFf))
print("Sr Eff Max Value: ")
print(max(SrEFf))