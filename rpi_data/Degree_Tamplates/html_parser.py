fin = open("URL2022FallRaw.txt", "r")
fout = open("majorURLlist2022FA.txt", "a")
fout.truncate(0)
for line in fin:
    if(line[0:2] == "<a"):
        fout.write("http://catalog.rpi.edu/" + line[9:61]+"\n")
