filename = "URL2022FallRaw.txt"  #URL2022FallRaw.txt
fin = open(filename, "r")
fout = open("majorURLlist2022FA.txt", "a")
fout.truncate(0)
for line in fin:
    if(line[0:2] == "<a"): #from <a href="preview_program.php?catoid=24&poid=6545&returnto=604"
        fout.write("http://catalog.rpi.edu/" + line[9:61]+"\n") #line[9:61] is link we want
