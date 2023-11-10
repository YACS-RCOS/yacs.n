import json
from pdfminer.high_level import extract_text


def parse_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        text = extract_text(pdf_file)
        
    return text

'''
Provide the PDF file path
To use it on your local machine, just replcae the direcotry with the directory
of where your final exam schedule PDF is. 
'''
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


#Had a separate text file to help look for patterns.

with open('file_format.txt', 'w') as f:
    
    for word in format_file:
        f.write(word)
        for x in range(2):
            f.write("\n")

f.close()


# Create the list to be formatted after modification
finals = format_file[:]

# JSON list to be dumped into the JSON file
data_list = []

multiple_course = []
possible_locs = []


# Get the final exam schedule year.
exam_year = finals[0].split()[1]



for x in range(len(finals)):
    
    possible_string = ""
    if "BY SUBJECT" in finals[x] and x < len(finals) - 4:
        
        courses = finals[x+2].split("\n")
        
        loc = finals[x+3].split("\n")
    
    #print(courses)
    
    for y in range(len(courses)):
        
        k = 0
        while(y+1 < len(courses) and courses[y] != courses[y+1]):
            
            if (k == 0):
                print(courses[y])
                k += 1
            
            courses.pop(y+1)
            
            y += 1
    
    
    
             

            
 
        
        

exit
for i in range(len(finals)):
    
    if "BY SUBJECT" in finals[i] and i < len(finals) - 4:
        
        department = finals[i+1].split("\n")

        courses = finals[i+2].split("\n")
        
        location = finals[i+3].split("\n")
        
        date = finals[i+4].split("\n")
        
        
        for j in range(len(department)):
            
            
            
            '''
            If we automate getting the final exam schedule (logging into Box) then 
            the if statements (checking the month) will be of use to get the semesters. 
            Currently have to get final schedule manually from box.
            
            If Final is in December, then its Fall Sem, otherwise its Spring Sem
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
            
            # Split the Course (NAME/ID) and the Section
            split_course = courses[j].strip().split(" ")

            
            '''
            Need an if statement because of the class 
            Department: PHYSICS, Course: ENGR / CHEM / ISCI / PHYS 1600
            Seems to be the only one without a section
            The last element seems to be the only of size 4, 
            so hardcoding it like this should fix the abnormality.
            
            Also there are parts like "(SEC 9 - 12)" so the if statements
            account for that. 
            '''
            
            
            # This takes care of the weird Physics Class Case
            if len(split_course[-1]) == 4:
                section = "(ALL SECTIONS)"
                new_course = " ".join(split_course)
            
            # This takes care of the weird case of (ALL) besides
            # of (ALL SECTIONS). 
            elif "(ALL)" in split_course:
                section = "(ALL SECTIONS)"
                split_course.pop()
                new_course = " ".join(split_course)
                
            # This takes care of the sections that are numbers
            elif len(split_course[-1]) == 2:
                section = split_course[-1]
                split_course.pop()
                new_course = " ".join(split_course)
            
            # This should take care of everything else
            else: 
                new_course = split_course[0] + " " + split_course[1]
                split_course.pop(0)
                split_course.pop(0)
                section = " ".join(split_course).strip()
                           
        
            
            entry = {
                
                "Department": department[j],
                "Course": new_course,
                "Section": section,
                "Location": location[j],
                "Date": new_date,
                "Time": time,
                "Semester": sem,
                "Year": exam_year
            }
            
            data_list.append(entry)
        
            #with open('final_schedule.json', 'a') as json_file:
                
                #json_file.write(json.dumps(entry) + '\n')
            

#json_file.close()


'''
{
    
    Department:
    Course:
    Year: 
    Semester:
    
}

'''