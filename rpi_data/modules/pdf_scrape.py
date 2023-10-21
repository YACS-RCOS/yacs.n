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

format_file = extracted_text.split("\n\n")

# Remove unnesscary words, so the pattern is consistent through out list
if "COURSE" in format_file:
    format_file.remove("COURSE")
    
if "LOCATION" in format_file:
    format_file.remove("LOCATION")
    
if "GRADES DUE " in format_file:
    format_file.remove("GRADES DUE ")


# Removes Department and Date from the PDF table (it was attached to the string rather than being its own string)
for i in range(len(format_file)):
    
    if "DEPARTMENT" in format_file[i]:
        format_file[i] = format_file[i].replace('DEPARTMENT\n', '', 1)
        
    if "DATE" in format_file[i]:
        format_file[i] = format_file[i].replace('DATE\n', '', 1)

''' 
Had a separate text file to help look for patterns.

with open('file_format.txt', 'w') as f:
    
    for word in format_file:
        f.write(word)
        for x in range(2):
            f.write("\n")

f.close()
'''

# Create the list to be formatted after modification
finals = format_file[:]

# JSON list to be dumped into the JSON file
data_list = []



for i in range(len(finals)):
    
    if "BY SUBJECT" in finals[i] and i < len(finals) - 3:
        
        department = finals[i+1].split("\n")

        courses = finals[i+2].split("\n")
        
        location = finals[i+3].split("\n")
        
        date = finals[i+4].split("\n")
        
        
        for j in range(len(department)):
            
            '''
            
            If we automate getting the final exam schedule (logging into Box) then 
            this will be of use to get the semesters. Currently have to get final
            schedule manually.
            
            '''
            
            if "December" in date[j]:
                sem = "Fall"
            else:
                sem = "Spring"

            # Split date to get Exam Time separate.
            split_date = date[j].split(" ")
            
            # Time is the last index of the list.
            time = split_date[-1]
            
            # Remove it from the split date
            split_date.pop()
            
            # Join the list back together without the Time component.
            new_date = " ".join(split_date)
            
            entry = {
                
                "Department": department[j],
                "Course": courses[j],
                "Location": location[j],
                "Date": new_date,
                "Time": time,
                "Semester": sem
            }
            
            data_list.append(entry)
        
            with open('final_schedule.json', 'a') as json_file:
                
                json_file.write(json.dumps(entry) + '\n')
            


json_file.close()

'''
{
    
    Department:
    Course:
    Year: 
    Semester:
    
}

'''