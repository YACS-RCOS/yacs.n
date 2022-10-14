f = open("majorData2022.txt", "r")
fout = open("majorData2022.json", "w")
lines = f.readlines()

output_string = ""
year = 1

fout.write("[\n")

i = 0
ipre = -1
for line in lines:
    ipre = i
    #line type
    if line[0] != " " and line.find(':') != -1:
        i = 0 #name
    if line[0:1] == " " and line.find('Year:') != -1:
        i = 1 #year
    if line[0:2] == "  " and line.find('Sem:') != -1:
        i = 2 #sem
    if line[0:3] == "   ":
        i = 3 #course

    line = line.strip()
    if line != "":
        if line == 'End':
            fout.write('],\n  }\n]\n')
            break
        if line.find('footnote') != -1:
            continue
        if line.find('Program for Graduates') != -1:
            continue
        if  i == 0:
            if ipre == 3:
                fout.write(']\n },\n')
            fout.write(' {\n')
            output_string = line
            output_string = output_string.replace(':','')
            output_string = '   "Major": "' + output_string + '",\n'
            fout.write(output_string) # write name
        if  i == 1:
            if ipre ==  3:
                fout.write('],\n') # complete pre sem
            if line.find('First') != -1:
                year = 1
                output_string = '   "Y1": "First Year",\n'
            if line.find('Second') != -1:
                year = 2
                output_string = '   "Y2": "Second Year",\n'
            if line.find('Third') != -1:
                #print('3'+line) #use to test
                year = 3
                output_string = '   "Y3": "Third Year",\n'
            if line.find('Fourth') != -1:
                year = 4
                output_string = '   "Y4": "Fourth Year",\n'
            fout.write(output_string) # write year
        if  i == 2:
            if ipre ==  3:
                fout.write('],\n') # complete pre sem
            if year == 1:
                if line.find('Fall') != -1:
                    output_string = '   "Y1S1": [ "Fall"'
                if line.find('Spring') != -1:
                    output_string = '   "Y1S2": [ "Spring"'
            if year == 2:
                if line.find('Fall') != -1:
                    output_string = '   "Y2S1": [ "Fall"'
                if line.find('Spring') != -1:
                    output_string = '   "Y2S2": [ "Spring"'
            if year == 3:
                if line.find('Arch') != -1 or line.find('Summer') != -1:
                    output_string = '   "Y3S1": [ "The Arch Semester"'
                if line.find('Fall') != -1:
                    output_string = '   "Y3S1": [ "Fall"'
                if line.find('Spring') != -1:
                    output_string = '   "Y3S2": [ "Spring"'
            if year == 4:
                if line.find('Arch') != -1 or line.find('Summer') != -1:
                    output_string = '   "Y4S1": [ "The Arch Semester"'
                if line.find('Fall') != -1:
                    output_string = '   "Y4S1": [ "Fall"'
                if line.find('Spring') != -1:
                    output_string = '   "Y4S2": [ "Spring"'
            fout.write(output_string) # write sem

        if  i == 3:
            output_string = ',"' + line +'"'
            fout.write(output_string) # write course



#major data 2022 glitch:
#line 753: no info for Chemistry - Chemical Biology Track
#line 1225: newline for 'or'
#line 1388-1391: unknown school year