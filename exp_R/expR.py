import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm,chi2
from scipy.special import factorial
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
def chi_squared(data, Poiss=True):
    frequencies, bins = np.histogram(data, bins=10)
    binRange = bins[1]-bins[0]
    bin_centers = (bins[:-1] + bins[1:]) / 2
    newFreqs = []
    i=0
    if Poiss:
        for val in bin_centers:
            newFreqs.append(poisson.pmf(round(val),3.6)*400)
            i+=1
    else:
        for val in bin_centers:
            newFreqs.append(norm.cdf(val+0.5*binRange,194.16674,12.74861)*400-norm.cdf(val-0.5*binRange,194.16674,12.74861)*400)
            i+=1
    total = 0
    for i in range(len(bin_centers)):
        total += (frequencies[i]-newFreqs[i])**2/newFreqs[i]
    return total
def confidence_level(chi_squared, degrees_of_freedom=9):
    # Calculate the p-value using the chi-squared value and degrees of freedom
    p_value = 1 - chi2.cdf(chi_squared, degrees_of_freedom)
    # Calculate the confidence level
    confidence_level = 1 - p_value
    return round(confidence_level*100,2)

def plot_count_rate_histogram(theoMean,data, bins=10, Gauss=False, sigma=0):
    """
    Plot count rate data on a histogram.
    
    Parameters:
        data (array-like): The count rate data to plot.
        bins (int or sequence, optional): The number of bins or a sequence of bin edges.
            Defaults to 10.
    """

    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7, label = 'Count Rate Data')
    x = np.arange(0, int(theoMean*3) + 1)
    pmf = norm.pdf(x, loc=theoMean, scale=np.sqrt(theoMean))
    if Gauss:
        pmf = norm.pdf(x, loc=theoMean, scale=sigma)
    plt.plot(x,400*pmf,zorder=10, color = 'r', label = r'Poisson Distribution with mean $\mu = 3.6$')

    plt.title('Count Rate Histogram')
    plt.xlabel('Count Rate')
    plt.legend()
    plt.ylabel('Frequency')
    plt.savefig('PoissonHist.png',dpi=300)
    plt.show()
input_file = 'PoissonData.txt'  # Replace with your input file path

PData = read_txt_file(input_file)
GData = read_txt_file('GaussData.txt')
plot_count_rate_histogram(3.6,PData)
plt.hist(GData,bins=11,color='skyblue', edgecolor='black',label = 'Count Rate Data')
x = np.arange(min(GData), max(GData))
pmf = norm.pdf(x, loc=194.16674, scale=12.74861)
plt.plot(x,3300*pmf,color = 'r', label = r'Gaussian Distribution $\mu = 194.2$, $\sigma = 12.8$')
plt.legend(bbox_to_anchor=(0.95, 1.17))
plt.savefig('GaussHist.png',dpi=300)
plt.show()
#plot_count_rate_histogram(194.16674, GData, True)
print('The chi squared val for poissant is '+ str(chi_squared(PData))+'confidence level is: '+str(confidence_level(chi_squared(PData))))
print('The chi squared val for gauss is '+ str(chi_squared(GData,False))+'confidence level is: '+str(confidence_level(chi_squared(GData,False))))
print('p-val Poissant is: AA'+ str(100-confidence_level(chi_squared(PData))))
print('p-val Gauss is: '+ str(100-confidence_level(chi_squared(GData,False))))
