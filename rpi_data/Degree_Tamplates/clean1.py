import re

fin = open("pathwayData.txt", "r").read().replace(
    "\n", " ").replace("\xa0", " ")
fout = open("pathDtaClean1.txt", "a")
fout.truncate(0)

importArray = re.split('< |> | Credit Hours: 4|:', fin)
for info in importArray:
    fout.write(info + "\n")
