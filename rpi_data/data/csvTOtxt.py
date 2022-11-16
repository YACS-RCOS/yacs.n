'''
import csv
data = csv.reader(open("spring-2021.csv"))
for i in data:
    print(i)
'''
import os
#data = input("Type the csv file we want to use: \n")
data = "spring-2021.csv"
dataU = open(data,"r")
list1 = []
for i in dataU:
    content = dataU.readlines()
    list1.append(content)
#print(list1)
writein = open("spring-2023_Spring.txt","w")
for i in list1:
    for j in i:
        writein.write(j)
os.system("python get2023S.py")