import json
from pdfminer.high_level import extract_text


def parse_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        text = extract_text(pdf_file)
        
    return text

# Provide the PDF file path
pdf_path = r'C:\Users\sundaj\Dropbox\PC\Desktop\final_subject.pdf'

# Extract text from the PDF using PDFMiner
extracted_text = parse_pdf(pdf_path)

sep_extract = extracted_text.split("\n\n")
format_file = sep_extract[:]

#remove unnesscary words, so the pattern is consistent through out list
if "COURSE" in format_file:
    format_file.remove("COURSE")
if "LOCATION" in format_file:
    format_file.remove("LOCATION")
if "GRADES DUE " in format_file:
    format_file.remove("GRADES DUE ")

for i in range(len(format_file)):
    if "DEPARTMENT" in format_file[i]:
        format_file[i] = format_file[i].replace('DEPARTMENT\n', '', 1)
    if "DATE" in format_file[i]:
        format_file[i] = format_file[i].replace('DATE\n', '', 1)


with open('file_format.txt', 'w') as f:
    
    for word in format_file:
        f.write(word)
        for x in range(2):
            f.write("\n")

f.close()

finals = format_file[:]

data_list = []

print(finals)


with open('list_output.txt', 'w') as file:
    
    for i in range(len(finals)):
        
        if "BY SUBJECT" in finals[i] and i < len(finals) - 3:
            
            department = finals[i+1].split("\n")

            courses = finals[i+2].split("\n")
            
            location = finals[i+3].split("\n")
            
            date = finals[i+4].split("\n")
            
            
            for j in range(len(department)):
                
                '''
                if "December" in date[j]:
                    sem = "Fall"
                else:
                    sem = "Spring"
                '''
                
                entry = {
                    
                    "Department": department[j],
                    "Course": courses[j],
                    "Location": location[j],
                    "Date": date[j],
                    #"Semester": sem
                }
                
                data_list.append(entry)
            
                with open('final_schedule.json', 'a') as json_file:
                        
                    json_file.write(json.dumps(entry) + '\n')
                

            

'''
{
    
    Department:
    Course:
    Year: 
    Semester:
    
}

'''