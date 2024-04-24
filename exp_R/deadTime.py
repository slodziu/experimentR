ShelfBuffer=[6.3,
6.16,
6.18,
6.26,
6.19,
6.18,
6.17,
6.27,
6.23,
6.22,
]
ShelfHeight = [4.05,
3.54,
3.67,
3.6,
3.63,
3.49,
4.13,
3.77,
3.52,
3.45]
Sr90Eff =[0.74067,
0.71415,
0.63809,
0.56387,
0.50619,
0.45076,
0.40684,
0.37254]
Na22Eff = [0.0551593991576839,
0.051448638374181,
0.0487167273626712,
0.0480134006141706,
0.0547379970321099,
0.0571557533830993, 
0.0626210108541693,
0.0684786441354227]
OCount = [121,103,106]
PCount=[42,38,47]
import csv
import statistics
import numpy as np
def calculate_mean_and_std(values):
    numeric_values = [float(val) for val in values]
    mean = statistics.mean(numeric_values)
    std_dev = statistics.stdev(numeric_values)
    return mean, std_dev
def read_tsv_file(file_path):
    data_lists = []
    with open(file_path, 'r', newline='') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        # Transpose the rows to columns
        next(tsvreader)
        data_lists = list(map(list, zip(*tsvreader)))
    return data_lists
file_path = 'Data/DeadTimes204Tl.tsv'
data = read_tsv_file(file_path)[2]
data_background = read_tsv_file('Data/Background_data.tsv')[2]
data_al = read_tsv_file('Data/thick_Al.tsv')[2]
print(data_al)
nList=[]
dataRange = read_tsv_file('Data/Tl204_invSquare.tsv')[2]
print(len(dataRange))
for i in range(int(len(dataRange)/3)):
    nList.append(dataRange[i*3:(i+1)*3])
for item in nList:
    print('Data INVERSE SQUARE:')
    print(item)
    print(calculate_mean_and_std(item))
m1 = data[:6]
m = data[6:12]
m2 = data[12:]
vals = [m1,m2,m]
m_1 = calculate_mean_and_std(m1)[0]
m_2 = calculate_mean_and_std(m2)[0]
m_t = calculate_mean_and_std(m)[0]
def deadTimeCalc(m_1,m_2,m_tot):
    tau = 1/m_tot * (1-np.sqrt(1-m_tot/(m_1*m_2)*(m_1+m_2-m_tot)))
    return tau
def altDeadTime(m_1,m_2,m_tot):
    tau = (m_1+m_2-m_tot)/(2*m_1*m_2)
    return tau
print('Dead time is: '+str(deadTimeCalc(m_1,m_2,m_t)))
print('Resolving time is: '+str(altDeadTime(m_1,m_2,m_t)))
print('Recovery time is: '+ str())

print('SHELF BUFFER:')
print(calculate_mean_and_std(ShelfBuffer))
print('SHELF SHELF HEIGHT:')
print(calculate_mean_and_std(ShelfHeight))
print('SHELF THICKNESS MEAN:')
print(calculate_mean_and_std(ShelfBuffer)[0]+calculate_mean_and_std(ShelfHeight)[0])
print('SHELF THICKNESS STD:')
print(np.sqrt(calculate_mean_and_std(ShelfBuffer)[1]**2+calculate_mean_and_std(ShelfHeight)[1]**2))
print('BACKGROUND:')
print(calculate_mean_and_std(data_background))

print('EFFICIENCY SR90:')
print(calculate_mean_and_std(Sr90Eff))

print('EFFICIENCY NA22:')
print(calculate_mean_and_std(Na22Eff))

print('O COUNT:')
print(calculate_mean_and_std(OCount))

print('P COUNT:')
print(calculate_mean_and_std(PCount))