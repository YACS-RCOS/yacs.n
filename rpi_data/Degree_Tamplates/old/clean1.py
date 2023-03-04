import re

fin = open("majorData2022.txt", "r", encoding='UTF-8').read().replace("\n", " ").replace("\xa0", " ")
fout = open("majorDtaClean1.txt", "a", encoding='UTF-8')
fout.truncate(0)

importArray = re.split('< |> | Credit Hours: 4|:', fin)
for info in importArray:
    fout.write(info + "\n")
