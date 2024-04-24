import matplotlib.pyplot as plt
import numpy as np

def expDecay(x ,mu):
    return np.exp(-mu*x)

widthVals = np.linspace(2.7, 3.4, 100)
counts = expDecay(widthVals, 13.8)
for i in range(len(counts)):
    if counts[i] < 0.01e-16:
        rangePoint = widthVals[i]
        break
plt.plot(widthVals, counts, label = r"Exponential Decay; $\mu = 13.8$m$^{-1}$", color = "black")
plt.axvline(x= rangePoint, color = "red", label = r"Range of $\beta$ when counts fall to $0.01\times I/I_0$")
plt.xlabel("Aluminium Thickness (mm)")
plt.ylabel(r"Relative Counts $I/I_0$")
plt.legend()
print(rangePoint)
plt.savefig("expDecay.png",dpi=300)
plt.show()