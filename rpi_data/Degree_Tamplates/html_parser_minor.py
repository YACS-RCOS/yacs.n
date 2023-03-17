filename = input("filename:")
fin = open(filename, "r")
fout = open("MinorURLlist.txt", "a")
fout.truncate(0)
for line in fin:
    if(line[0:2] == "<a"):
        fout.write("http://catalog.rpi.edu/" + line[9:61]+"\n")
