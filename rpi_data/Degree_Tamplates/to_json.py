f = open("majorDtaClean1.txt", "r", encoding='UTF-8')
fout = open("ideal.json", "w", encoding='UTF-8')
lines = f.readlines()
i = 0
required_finished = False
selective_not_finished = False
compatible_minor_not_finished = False
category_dict = {}
output_string = ""
current_array = ""
def is_course_code(line):
    if(len(line) < 10):
        return False
    return (line[0:4].isupper() & line[5:9].isnumeric()) | line[0:8].isupper()

for line in lines:
    line = line.strip()
    if(current_array == ""):
        current_array = "name"
        category_dict[current_array] = [line]
    elif(current_array == "Compatible minor"):
        if(category_dict[current_array] == None):
            category_dict[current_array] = []
        category_dict[current_array].append(line)
    elif(is_course_code(line)):
        if(category_dict[current_array] == None):
            category_dict[current_array] = []
        category_dict[current_array].append(line)
    else:
        if(("Choose" in line) & (line in category_dict.keys())):
            i = 2
            line = line+str(i)
            while(line in category_dict.keys()):
                line = line[:-1]+str(i)
                i += 1
        if(not line in category_dict.keys()):
            category_dict[line] = None
        current_array = line
#print(category_dict)   
output_string += "{\n"
for key in category_dict.keys():
    output_string += "\"" + key + "\"" + ":[\""
    tmp = ''
    if(category_dict[key] != None):
        tmp = "\",\"".join(category_dict[key])
    output_string += tmp + "\"],\n"
output_string = output_string[:-2]
output_string += "\n}"
fout.write(output_string)