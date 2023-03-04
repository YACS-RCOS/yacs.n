filename = "URLraw.txt"  #URL2022FallRaw.txt
fin = open(filename, "r",encoding='UTF-8')
fout = open("temp/majorURL.txt", "a",encoding='UTF-8')
fout.truncate(0)
for line in fin:
    if(line[0:2] == "<a"): #from <a href="preview_program.php?catoid=24&poid=6545&returnto=604"
        #print("http://catalog.rpi.edu/" + line[9:61]+"\n") #line[9:61] is link we want
        fout.write("http://catalog.rpi.edu/" + line[9:61]+"\n") #line[9:61] is link we want
