#store all the data in list
listCollect = list()
listEach = []
listSeperate = []
word = ""
#store all the final data in the dictionary
#dictTitle = {"course_name": 0, "description": 0, "prerequisites": 0, "corequisites": 0}

#hold 1000 dictionary
holder = []
for i in range(2489):
    holder.append({})

final = [] #collect all the dictionary in the list
#txt = "spring-2023_Spring.txt"
txt = "a.txt"
data = open(txt,"r")
count = 0 #to calculate the number of words
countL = [] #to collect the count in countL, and append countL everytime 
while True:
    content = data.readline()
    if (content == "DONEREAD"):
        break
    else:
        #print(content)
        for i in content:
            word += i
            if (i == "," or i == "\n"):
                count += 1
                listEach.append(word)
                listSeperate.append(listEach)
                word = ""          
                listEach = []  
            if (i == "\n"):
                countL.append(count)
                listSeperate.append(countL)
                listCollect.append(listSeperate)
                listSeperate = []
                count = 0
                countL = []
#print(listCollect)
#collect all the dictionary in the holder
holderIndex = 0
for i in listCollect:
    for j in range(i[-1][0]):
        if (j == 0):
            holder[holderIndex]["course_name"] = i[j][0]
        elif (j == 18 and "ADMN-" in i[j][0]):
            holder[holderIndex]["description"] = ""
        elif (j == i[-1][0] - 3):
            if (i[j][0] == ","):
                holder[holderIndex]["prerequisites"] = ""
            else:
                holder[holderIndex]["prerequisites"] = i[j][0]
        elif (j == i[-1][0] - 2):
            if (i[j][0] == ","):
                holder[holderIndex]["corequisites"] = ""
            else:
                holder[holderIndex]["corequisites"] = i[j][0]
    final.append(holder[holderIndex])
    holderIndex += 1
print(final)