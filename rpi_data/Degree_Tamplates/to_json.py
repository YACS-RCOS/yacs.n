f = open("pathDtaClean1.txt", "r")
fout = open("ideal.json", "w")
fout.write('{\n')
lines = f.readlines()
i = 0
required_finished = False
selective_not_finished = False
compatible_minor_not_finished = False
output_string = ""
for line in lines:
    line = line.strip()
    if(i == 0):
        output_string += "\"name\":\n\"" + line
    elif("Required" in line):
        output_string += "\",\n\"Required\":[\n"
    elif("Choose" in line):
        output_string = output_string[:-2]
        output_string += "],\n\""+line+"\":[\n"
    elif("Compatible minor" in line):
        output_string = output_string[:-2]
        output_string += "],\n\""+line+"\":\n"
    else:
        output_string += "\"" + line + "\",\n"
    i += 1
output_string = output_string[:-2]
output_string += "\n}"
fout.write(output_string)

output_string = output_string[:-2]
output_string += "\n}"
fout.write(output_string)