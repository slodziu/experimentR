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

PData = read_txt_file('PoissonData.txt')
GData = read_txt_file('GaussData.txt')

def plotGauss():
    plt.figure(figsize=(8, 6))
    plt.hist(GData, bins=10, color='skyblue', edgecolor='black', alpha=0.7, label = 'Count Rate Data')
    x = np.arange(0, int(194.16674*3) + 1)
    pmf = norm.pdf(x, loc=194.16674, scale=12.74861)
    plt.plot(x, pmf*400, 'r-', lw=2, label = 'Gaussian Fit')
    plt.title('Gaussian Fit of Count Rate Data')
    plt.xlabel('Count Rate')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()