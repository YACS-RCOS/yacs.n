-- Adminer 4.7.6 PostgreSQL dump

DROP TABLE IF EXISTS "majorTemplates";
CREATE TABLE "public"."majorTemplates" (
    "Major" text NOT NULL,
    "Year" text NOT NULL,
    "Semester" text NOT NULL,
    "Courses" text[]
) WITH (oids = false);

INSERT INTO "majorTemplates" ("Major", "Year", "Semester", "Courses") VALUES
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'First Year',	'Fall',	'{"Science Core Elective Credit Hours: 4
	(See footnote 6 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","STSO 1110 - Science, Technology, and Society Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'First Year',	'Spring',	'{"Science Core Elective Credit Hours: 4
	(See footnote 6 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Intermediate STS course Credit Hours: 4
	(See footnote 2 below)","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Science Core Elective Credit Hours: 4
	(See footnote 6 below)","CAS Course Credit Hours: 4
	(See footnote 7 below)","STSO 2100 - Investigating Society Credit Hours: 4"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Second Year',	'Spring',	'{"CAS Course Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Science Core Elective Credit Hours: 4
	(See footnote 6 below)","Advanced STS Course Credit Hours: 4
	(See footnote 3 below)"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Third Year',	'Fall',	'{"CAS Course Credit Hours: 4","Advanced STS Course Credit Hours: 4","STSO 4980 - Research Design Credit Hours: 4"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Third Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","CAS Course Credit Hours: 4","STSO 4990 - STS and Sustainability Senior Project Credit Hours: 4"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Fourth Year',	'Fall',	'{"Federal Civil Procedure Credit Hours: 4","Contracts Credit Hours: 3","Property I Credit Hours: 2","Torts Credit Hours: 4","Introduction to Lawyering Credit Hours: 3"}'),
('Accelerated Science, Technology, and Society (Law) B.S./J.D.',	'Fourth Year',	'Spring',	'{"Constitutional Law Credit Hours: 4
	(Course applied to HASS Core Elective)","Criminal Law Credit Hours: 3","Property II Credit Hours: 4","Introduction to Lawyering Credit Hours: 3","Contracts Credit Hours: 2"}'),
('Aeronautical Engineering Curriculum',	'First Year',	'Fall Semester (17 credits)',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Aeronautical Engineering Curriculum',	'First Year',	'Spring Semester (17 credits)',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","CHEM 1100 - Chemistry I Credit Hours: 4","MANE 1060 - Fundamentals of Flight Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Aeronautical Engineering Curriculum',	'Second Year',	'Fall Semester (16 credits)',	'{"SoE 2…. Engineering Design Elective
	(See footnotes 1, 5, and 6 below)","ENGR 1300 - Engineering Processes Credit Hours: 1","ENGR 2530 - Strength of Materials Credit Hours: 4","MANE 2710 - Thermodynamics Credit Hours: 3","MATH 2400 - Introduction to Differential Equations Credit Hours: 4"}'),
('Aeronautical Engineering Curriculum',	'Second Year',	'Spring Semester (17 credits)',	'{"HASS Core Elective  Credit Hours: 4
	(See footnote 3 below)","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MANE 2110 - Numerical Methods and Programming for Engineers Credit Hours: 3","MANE 2720 - Fluid Mechanics Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Aeronautical Engineering Curriculum',	'Third Year',	'The Arch Summer Semester* (16 credits)',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","ENGR 2090 - Engineering Dynamics Credit Hours: 4","MANE 4060 - Aerospace Structures and Materials Credit Hours: 4","MANE 4070 - Aerodynamics Credit Hours: 4"}'),
('Aeronautical Engineering Curriculum',	'Third Year',	'Fall or Spring Semester (16 credits)',	'{"Free Elective Credit Hours: 4 
	(See footnotes 6 and 9 below) ","STSS 4100 Professional Development II Credit Hours: 2
	(See footnote 1, 6, and 7 below)","MANE 4500 - Modeling and Control of Dynamic Systems Credit Hours: 3","MANE 4900 - Aeroelasticity and Structural Vibrations Credit Hours: 3","MANE 4910 - Fluid Dynamics Laboratory Credit Hours: 2","MANE 4920 - Aerospace Structures Laboratory Credit Hours: 2"}'),
('Aeronautical Engineering Curriculum',	'Fourth Year',	'Fall Semester (16 credits)',	'{"MANE 4…. Computation Elective Credit Hours: 3 
	(See footnotes 1, 6, and 10 below)","MANE 4…. Flight Mechanics Elective Credit Hours: 4
	(See footnotes 9 and 11 below)","Free Elective Credit Hours: 4","MANE 4080 - Propulsion Systems Credit Hours: 3","MANE 4510 - Control Systems Laboratory Credit Hours: 2"}'),
('Aeronautical Engineering Curriculum',	'Fourth Year',	'Spring Semester (15 credits)',	'{"Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	​(See footnote 3 below) ","MANE 4…. Capstone Design Elective Credit Hours: 3
	(See footnotes 9 and 12 below)","MANE 4…. Aerospace Technical Elective Credit Hours: 3
	(See footnotes 1 and 13 below)","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1"}'),
('Applied Physics',	'First Year',	'Fall',	'{"HASS Elective Credit Hours: 4
	(See footnote 1 below)","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1150 - Honors Physics I Credit Hours: 4"}'),
('Applied Physics',	'First Year',	'Spring',	'{"Free Elective","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1250 - Honors Physics II Credit Hours: 4"}'),
('Applied Physics',	'Second Year',	'Fall',	'{"HASS Elective, Credit Hours: 4
	​(See footnote 1 below.)","CHEM 1100 - Chemistry I Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 2210 - Quantum Physics I Credit Hours: 4"}'),
('Applied Physics',	'Second Year',	'Spring',	'{"HASS Elective Credit Hours: 4
	(See footnote 1 below.)","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","PHYS 2220 - Quantum Physics II Credit Hours: 4","PHYS 4330 - Theoretical Mechanics Credit Hours: 4"}'),
('Chemical Engineering',	'First Year',	'Fall',	'{"HASS Elective Credit Hours: 4","CHME 1010 - Introduction to Chemical Engineering Credit Hours: 1","CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Applied Physics',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Elective Credit Hours: 4
	(See footnotes 1 and 8 below.)","Free Elective Credit Hours: 4
	(See footnote 8 below.)","PHYS 2962Computing for Physicists Free Elective Credit Hours: 2
	(See footnote 6 below.)","PHYS 2963 Mathematical Physics Free Elective Credit Hours: 2
	(See footnote 7 below.)","PHYS 2350 - Experimental Physics Credit Hours: 4"}'),
('Applied Physics',	'Third Year',	'Fall OR Spring*',	'{"Technical Elective Credit Hours: 4
	(See footnote 4 below.)","MATH 4600 - Advanced Calculus Credit Hours: 4","PHYS 4210 - Electromagnetic Theory Credit Hours: 4","PHYS 4420 - Thermodynamics and Statistical Mechanics Credit Hours: 4"}'),
('Applied Physics',	'Fourth Year',	'Fall',	'{"Culminating Experience Credit Hours: 4
	(See footnote 5 below.)","Technical Elective Credit Hours: 4
	(See footnote 4 below.)","Technical Elective Credit Hours: 4
	(See footnote 4 below.)","HASS Elective Credit Hours: 4
	(See footnote 1 below.)"}'),
('Applied Physics',	'Fourth Year',	'Spring',	'{"Technical Elective Credit Hours: 4
	(See footnote 4 below.)","Free Elective Credit Hours: 4","HASS Elective Credit Hours: 4
	(See footnote 1 below.)"}'),
('Architecture',	'First Year',	'Fall',	'{"ARCH 2150 - The Ethos of Architecture Credit Hours: 3","ARCH 2160 - Architectural Media Credit Hours: 2","ARCH 2510 - Materials and Design Credit Hours: 2","ARCH 2520 - Digital Constructs 1 Credit Hours: 2","ARCH 2800 - Architectural Design Studio 1 Credit Hours: 5","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4"}'),
('Architecture',	'First Year',	'Spring',	'{"HASS Approved Inquiry and Communication Intensive Course Credit Hours: 4
	(See footnote 1 below)","ARCH 2370 - Energy, Comfort, and Ecology Credit Hours: 2","ARCH 2530 - Digital Constructs 2 Credit Hours: 2","ARCH 2810 - Architectural Design Studio 2 Credit Hours: 5","ARCH 4090 - Architectural Case Studies Credit Hours: 2","ARCH 4100 - An Architectural Genealogy Credit Hours: 3"}'),
('Architecture',	'Second Year',	'Fall',	'{"ARCH 2330 - Structures 1 Credit Hours: 3","ARCH 2350 - Construction Systems Credit Hours: 2","ARCH 2540 - Digital Constructs 3 Credit Hours: 2","ARCH 2820 - Architectural Design Studio 3 Credit Hours: 5","ARCH 4050 - Cities and Their Territories Credit Hours: 2","ARCH 4120 - Cloud Atlas: 20th Century Architecture, Culture and Civilization Credit Hours: 3"}'),
('Architecture',	'Second Year',	'Spring',	'{"ARCH 2360 - Environmental and Ecological Systems Credit Hours: 4","ARCH 2550 - Digital Constructs 4 Credit Hours: 2","ARCH 2830 - Architectural Design Studio 4 Credit Hours: 5","ARCH 4150 - Contemporary Design Approaches Credit Hours: 3","PHYS 1050 - General Physics Credit Hours: 4"}'),
('Architecture',	'Third Year',	'Fall',	'{"HASS Elective Credit Hours: 4","MATH Elective Credit Hours: 4","ARCH 4330 - Structures 2 Credit Hours: 3","ARCH 4560 - Materials and Enclosures Credit Hours: 2","ARCH 4820 - Integrated Design Schematic Credit Hours: 5"}'),
('Architecture',	'Third Year',	'Spring',	'{"Science Elective Credit Hours: 4","ARCH 4540 - Professional Practice 1 Credit Hours: 2","ARCH 4590 - Entrepreneurship and Architecture Credit Hours: 2","ARCH 4740 - Building Systems and Environment Credit Hours: 4","ARCH 4830 - Integrated Design Development Credit Hours: 5"}'),
('Architecture',	'Fourth Year',	'The Arch Summer Semester*',	'{"HASS Elective Credit Hours: 4","HASS Elective Credit Hours: 4","Science Elective Credit Hours: 4","ARCH 4770 - Architectural Design Studio 5 Credit Hours: 5"}'),
('Architecture',	'Fourth Year',	'Fall OR Spring',	'{"Professional Elective Credit Hours: 2","Professional Elective Credit Hours: 2","Elective Credit Hours: 4","HASS Elective Credit Hours: 4","ARCH 4550 - Professional Practice 2 Credit Hours: 2","ARCH 4780 - Architectural Design Studio 6 Credit Hours: 5"}'),
('Biological Neuroscience',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","BIOL 1010 - Introduction to Biology Credit Hours: 3","(see footnote 1 below)","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Biological Neuroscience',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","BIOL 2120 - Introduction to Cell and Molecular Biology Credit Hours: 3","(see footnote 1 below)","BIOL 2125 - Introduction to Cellular and Molecular Biology Laboratory Credit Hours: 1","CHEM 1200 - Chemistry II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Biological Neuroscience',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","BIOL 2500 - Genetics and Evolution Credit Hours: 4","CHEM 2250 - Organic Chemistry I Credit Hours: 3","CHEM 2230 - Organic Chemistry Laboratory I Credit Hours: 1","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Biological Neuroscience',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","BIOL 4620 - Molecular Biology Credit Hours: 4","CHEM 2260 - Organic Chemistry II Credit Hours: 3","CHEM 2240 - Organic Chemistry Laboratory II Credit Hours: 1","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Biological Neuroscience',	'Third Year',	'The Arch Summer Semester',	'{"HASS Core Neuroscience Elective Credit Hours: 4","Advanced Biology Laboratory Option Credit Hours: 6","Free Elective Credit Hours: 2","BIOL 4760 - Molecular Biochemistry I Credit Hours: 4","(see footnote 7 below)"}'),
('Biological Neuroscience',	'Third Year',	'Spring',	'{"HASS Core Neuroscience Elective Credit Hours: 4","Free Elective Credit Hours: 4","BIOL 4100 - From Neuron to Behavior Credit Hours: 4","(see footnote 8 below)","BIOL 4200 - Biostatistics Credit Hours: 4","(see footnote 8 below)"}'),
('Biological Neuroscience',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4​","BIOL 4260 - Advanced Cell Biology Credit Hours: 4","BIOL 4270 - Human Physiology Credit Hours: 4","(see footnote 8 below)"}'),
('Biological Neuroscience',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4​","BIOL 4150 - Cellular Neuroscience Credit Hours: 4","(see footnote 6 below)","BIOL 4250 - Developmental Biology Credit Hours: 4","(see footnote 8 below)"}'),
('Biology',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Biology',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","BIOL 2120 - Introduction to Cell and Molecular Biology Credit Hours: 3","BIOL 2125 - Introduction to Cellular and Molecular Biology Laboratory Credit Hours: 1","CHEM 1200 - Chemistry II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Biology',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","BIOL 2500 - Genetics and Evolution Credit Hours: 4","CHEM 2230 - Organic Chemistry Laboratory I Credit Hours: 1","CHEM 2250 - Organic Chemistry I Credit Hours: 3","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Biology',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","BIOL 4620 - Molecular Biology Credit Hours: 4","CHEM 2240 - Organic Chemistry Laboratory II Credit Hours: 1","CHEM 2260 - Organic Chemistry II Credit Hours: 3","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Biology',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)"}'),
('Biology',	'Third Year',	'Fall or Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)"}'),
('Biology',	'Fourth Year',	'Fall',	'{"BIOL - Biology Elective Credit Hours: 4
	(See footnote 4 below)","Elective Credit Hours: 4","Elective Credit Hours: 4","Elective Credit Hours: 4"}'),
('Biology',	'Fourth Year',	'Spring',	'{"BIOL - Biology Elective Credit Hours: 4
	(See footnote 4 below)","BIOL - Biology Elective Credit Hours: 4
	(See footnote 4 below)","Elective Credit Hours: 4","Elective Credit Hours: 4"}'),
('Biomedical Engineering',	'First Year',	'Fall',	'{" HASS Elective Credit Hours:4
	(See footnote 1 below)","CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Biomedical Engineering',	'First Year',	'Spring',	'{"HASS Elective- Credit Hours: 4
	(See footnote 1 below)","BIOL 2120 - Introduction to Cell and Molecular Biology Credit Hours: 3","BIOL 2125 - Introduction to Cellular and Molecular Biology Laboratory Credit Hours: 1","ENGR 1300 - Engineering Processes Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Biomedical Engineering',	'Second Year',	'Fall',	'{"BMED 2050 - Programming for BME Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Biomedical Engineering',	'Second Year',	'Spring',	'{"BMED 2100 - Biomaterials Science and Engineering Credit Hours: 4","BMED 2300 - Bioimaging and Bioinstrumentation Credit Hours: 4","BMED 2540 - Biomechanics Credit Hours: 4","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3"}'),
('Biomedical Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Elective - Credit Hours:  4
	(See footnote 1 below)","Free Elective  - Credit Hours: 3
	(See footnote 4 below)","BMED 4200 - Modeling of Biomedical Systems Credit Hours: 3","BMED 4250 - Biomedical Transport Phenomena Credit Hours: 4","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1"}'),
('Biomedical Engineering',	'Third Year',	'Fall OR Spring',	'{"BME Tech Elective I - Credit Hours: 3","Free Elective - Credit Hours: 3
	(See footnote 4 below)","BMED 4500 - Advanced Systems Physiology Credit Hours: 4","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2","(see footnote 2 below)","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4"}'),
('Biomedical Engineering',	'Fourth Year',	'Fall',	'{"BME Tech Elective II - Credit Hours: 3 ","Free Elective- Credit Hours: 3
	(See footnote 4 below)","HASS Elective - Credit Hours: 4","BMED 4010 - Biomedical Engineering Laboratory Credit Hours: 4","BMED 4260 - Biomedical Product Development and Commercialization Credit Hours: 3"}'),
('Biomedical Engineering',	'Fourth Year',	'Spring',	'{"BME Tech Elective III - Credit Hours: 3","BME Tech Elective IV - Credit Hours: 3","Free Elective  - Credit Hours: 3","HASS Elective  - Credit Hours: 4
	(See footnote 1 below)","BMED 4600 - Biomedical Engineering Design Credit Hours: 3"}'),
('Biotechnology and Health Economics',	'First Year',	'Fall',	'{"BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","IHSS 1200 - Principles of Economics Credit Hours: 4","[See Footnote 1]"}'),
('Biotechnology and Health Economics',	'First Year',	'Spring',	'{"BIOL 2120 - Introduction to Cell and Molecular Biology Credit Hours: 3","CHEM 1200 - Chemistry II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","ECON 2010 - Intermediate Microeconomic Theory Credit Hours: 4"}'),
('Biotechnology and Health Economics',	'Second Year',	'Fall',	'{"Free Elective Credit Hours: 4","CHEM 2250 - Organic Chemistry I Credit Hours: 3","CHEM 2230 - Organic Chemistry Laboratory I Credit Hours: 1","ECON 4170 - Health Economics and Policy Credit Hours: 4"}'),
('Biotechnology and Health Economics',	'Second Year',	'Spring',	'{"Biotech and Health Economics Concentration Course #1 Credit Hours: 4 [See Footnote 2]","Free Elective Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4","ECON 4270 - Behavioral Economics Credit Hours: 4"}'),
('Biotechnology and Health Economics',	'Third Year',	'Summer',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","ECON 4570 - Econometrics Credit Hours: 4","BCBP 4760 - Molecular Biochemistry I Credit Hours: 4"}'),
('Biotechnology and Health Economics',	'Third Year',	'Fall or Spring',	'{"Biotech and Health Economics Concentration Course #2 Credit Hours: 4 [See Footnote 2]","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","ECON 4290 - Economics of Biotech and Medical Innovations Credit Hours: 4"}'),
('Biotechnology and Health Economics',	'Fourth Year',	'Fall',	'{"Biotech and Health Economics Concentration Course #3 Credit Hours: 4 [See Footnote 2]","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","ECON 4940 - Readings in Economics Credit Hours: 3 to 4","Research in Biotechnology and Health Economics (Credit Hours: 4)"}'),
('Biotechnology and Health Economics',	'Fourth Year',	'Spring',	'{"Biotech and Health Economics Concentration Course #4 Credit Hours: 4 [See Footnote 2]","Free Elective Credit Hours: 4","Free Elective Credit Hours: 2","BCBP 4710 - Biochemistry Laboratory Credit Hours: 6"}'),
('Building Sciences B.S.',	'First Year',	'Fall',	'{"ARCH 2150 - The Ethos of Architecture Credit Hours: 3","ARCH 2160 - Architectural Media Credit Hours: 2","ARCH 2510 - Materials and Design Credit Hours: 2","ARCH 2520 - Digital Constructs 1 Credit Hours: 2","ARCH 2800 - Architectural Design Studio 1 Credit Hours: 5","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4"}'),
('Building Sciences B.S.',	'First Year',	'Spring',	'{"ARCH 2370 - Energy, Comfort, and Ecology Credit Hours: 2","ARCH 2850 - Building Performance Studio 1 Credit Hours: 5","ARCH 4090 - Architectural Case Studies Credit Hours: 2","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","PHYS 1050 - General Physics Credit Hours: 4"}'),
('Building Sciences B.S.',	'Second Year',	'Fall',	'{"Concentration 1 Credit Hours: 4","ARCH 2330 - Structures 1 Credit Hours: 3","ARCH 2350 - Construction Systems Credit Hours: 2","ARCH 2860 - Building Performance Studio 2 Credit Hours: 5","ARCH 4560 - Materials and Enclosures Credit Hours: 2"}'),
('Building Sciences B.S.',	'Second Year',	'Spring',	'{"Concentration 2 Credit Hours: 4","Science Elective Credit Hours: 4","ARCH 2360 - Environmental and Ecological Systems Credit Hours: 4","ARCH 4550 - Professional Practice 2 Credit Hours: 2","ARCH 4740 - Building Systems and Environment Credit Hours: 4"}'),
('Building Sciences B.S.',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Building Sciences B.S.',	'Third Year',	'Fall OR Spring',	'{"Concentration 3 Credit Hours: 4","HASS Core Elective Credit Hours: 4 ","Professional Elective Credit Hours: 2","Free Elective Credit Hours: 4","ARCH 4330 - Structures 2 Credit Hours: 3","This course is required in either Fall Third year or Fall Fourth year.","ARCH 4510 - Construction Industry Seminar 1 Credit Hours: 2","This course is required in either Fall Third year or Fall Fourth year."}'),
('Building Sciences B.S.',	'Fourth Year',	'Fall',	'{"Concentration 4 Credit Hours: 4","Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ARCH 4330 - Structures 2 Credit Hours: 3","If If this course was not taken in Fall Third year then it must be taken in Fall Fourth year.","ARCH 4510 - Construction Industry Seminar 1 Credit Hours: 2","If this course was not taken in Fall Third year then it must be taken in Fall Fourth year."}'),
('Building Sciences B.S.',	'Fourth Year',	'Spring',	'{"Elective Credit Hours: 4","Science Elective Credit Hours: 4","ARCH 4520 - Construction Industry Seminar 2 Credit Hours: 2","ARCH 4530 - Building Sciences Capstone Credit Hours: 4"}'),
('Business Analytics',	'First Year',	'Fall',	'{"HASS Science, Technology and Society Options Credit Hours: 4
	(See footnote 3 below)","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MATH 1010 - Calculus I Credit Hours: 4","MGMT 1100 - Management in the Digital Age Credit Hours: 4"}'),
('Business Analytics',	'First Year',	'Spring',	'{"HASS or Science Elective Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","IHSS 1200 - Principles of Economics Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Business Analytics',	'Second Year',	'Fall',	'{"CSCI 1200 - Data Structures Credit Hours: 4","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","MGMT 1240 - Management Professional Development 1 Credit Hours: 2","MGMT 2100 - Statistical Methods Credit Hours: 4"}'),
('Business Analytics',	'Second Year',	'Spring',	'{"HASS or Science Core Elective Credit Hours: 4","MGMT 2300 - Financial Accounting in the Digital Age Credit Hours: 4","MGMT 2430 - Marketing Principles Credit Hours: 4"}'),
('Business Analytics',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MGMT 2320 - Managerial Finance Credit Hours: 4","MGMT 4140 - Computer Information Systems Credit Hours: 4","MGMT 4850 - Organizational Behavior in High Performance Organizations Credit Hours: 4"}'),
('Business Analytics',	'Third Year',	'Fall or Spring',	'{"Elective Credit Hours: 4","MGMT 4100 - Quantitative Methods for Business Credit Hours: 4","MGMT 4110 - Operations Management Credit Hours: 4","MGMT 4170 - Data Resource Management Credit Hours: "}'),
('Business Analytics',	'Fourth Year',	'Fall',	'{"HASS Ethics Option Credit Hours: 4
	(See footnotes 1 and 3 below)","Elective Credit Hours: 4 ","MGMT 4190 - Introduction to Machine Learning Applications Credit Hours: 4"}'),
('Business Analytics',	'Fourth Year',	'Spring',	'{"HASS or Science Elective Credit Hours: 2","Elective Credit Hours: 4","Capstone Credit Hours: 4
	(See footnote 3 below)","MGMT 4870 - Strategy and Policy Credit Hours: 4"}'),
('Business and Management',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MATH 1010 - Calculus I Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","MGMT 1100 - Management in the Digital Age Credit Hours: 4","MGMT 2510 - Introduction to Data Management and Analytics Credit Hours: 4"}'),
('Business and Management',	'First Year',	'Spring',	'{"IHSS 1200 - Principles of Economics Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","MGMT 1260 - Business Law and Ethics Credit Hours: 4"}'),
('Business and Management',	'Second Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MGMT 1240 - Management Professional Development 1 Credit Hours: 2","MGMT 2100 - Statistical Methods Credit Hours: 4","MGMT 2300 - Financial Accounting in the Digital Age Credit Hours: 4"}'),
('Business and Management',	'Second Year',	'Spring',	'{"Elective Credit Hours: 4","MGMT 1250 - Management Professional Development 2 Credit Hours: 2","MGMT 2430 - Marketing Principles Credit Hours: 4","MGMT 4100 - Quantitative Methods for Business Credit Hours: 4","MGMT 4110 - Operations Management Credit Hours: 4"}'),
('Business and Management',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MGMT 2320 - Managerial Finance Credit Hours: 4","MGMT 4140 - Computer Information Systems Credit Hours: 4","MGMT 4850 - Organizational Behavior in High Performance Organizations Credit Hours: 4"}'),
('Business and Management',	'Third Year',	'Fall or Spring',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MGMT 4860 - Human Resources in High Performance Organizations Credit Hours: 4"}'),
('Business and Management',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","Elective Credit Hours: 4","Elective Credit Hours: 4"}'),
('Business and Management',	'Fourth Year',	'Spring',	'{"Elective Credit Hours: 4","Elective Credit Hours: 4","MGMT 4870 - Strategy and Policy Credit Hours: 4"}'),
('Chemical Engineering',	'First Year',	'Spring',	'{"HASS Elective Credit Hours: 4","CHME 1100 - Fundamentals of Chemical Engineering Credit Hours: 4","BIOL 2120 - Introduction to Cell and Molecular Biology Credit Hours: 3","BIOL 2125 - Introduction to Cellular and Molecular Biology Laboratory Credit Hours: 1","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","ENGR 1400 - Engineering Communications Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Chemical Engineering',	'Second Year',	'Fall',	'{"CHME 2010 - Material, Energy, and Entropy Balances Credit Hours: 3","CHEM 2250 - Organic Chemistry I Credit Hours: 3","ENGR 1010 - Professional Development: Group Dynamics Credit Hours: 1","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Chemical Engineering',	'Second Year',	'Spring',	'{"HASS Elective Credit Hours: 4","CHME 2020 - Energy, Entropy, and Equilibrium Credit Hours: 3","CHME 4010 - Transport Phenomena I Credit Hours: 4","CHEM 2260 - Organic Chemistry II Credit Hours: 3","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3"}'),
('Chemical Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Elective Credit Hours: 4","Free Elective I Credit Hours: 4","CHME 2050 - Introduction to Computational Chemical Engineering Credit Hours: 3","CHME 4020 - Transport Phenomena II Credit Hours: 4","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Chemical Engineering',	'Third Year',	'Fall OR Spring',	'{"CHME 4XXX Chemical Engineering Elective Credit Hours: 3
	(See footnote 5 below)","HASS Elective Credit Hours: 4","CHME 4040 - Chemical Engineering Separations Credit Hours: 3","CHME 4500 - Chemical Reactor Design Credit Hours: 3","CHEM 4530 - Modern Techniques in Chemistry Credit Hours: 4"}'),
('Chemical Engineering',	'Fourth Year',	'Fall',	'{"Engineering Elective Credit Hours: 3
	(See footnote 6 below)","CHME 4030 - Chemical Process Dynamics and Control Credit Hours: 4","CHME 4050 - Chemical Process Design: Fundamentals Credit Hours: 3","CHME 4150 - Chemical Engineering Laboratory I Credit Hours: 3","CHEM 4420 - Microscopic Physical Chemistry Credit Hours: 3"}'),
('Chemical Engineering',	'Fourth Year',	'Spring',	'{"Free Elective II Credit Hours: 4","Free Elective III Credit Hours: 4","CHME 4060 - Chemical Process Design: Applications Credit Hours: 3","CHME 4160 - Chemical Engineering Laboratory II Credit Hours: 3","CHME 4170 - Bioprocessing Laboratory Course Credit Hours: 3","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1"}'),
('Chemistry ',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4","CHEM 1900 - Chemistry for Life Credit Hours: 1"}'),
('Chemistry ',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","CHEM 1200 - Chemistry II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Chemistry ',	'Second Year',	'Fall',	'{"HASS  Core Elective Credit Hours: 4","CHEM 2110 - Equilibrium Chemistry and Quantitative Analysis Credit Hours: 3","CHEM 2120 - Experimental Chemistry I: Analytical Techniques Credit Hours: 2","CHEM 2250 - Organic Chemistry I Credit Hours: 3","MATH 2400 - Introduction to Differential Equations Credit Hours: 4"}'),
('Chemistry ',	'Second Year',	'Spring',	'{"Elective Credit Hours: 4","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CHEM 2030 - Inorganic Chemistry I Credit Hours: 3","CHEM 2260 - Organic Chemistry II Credit Hours: 3","CHEM 2290 - Experimental Chemistry II: Synthesis and Characterization Credit Hours: 3"}'),
('Chemistry ',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","CHEM 4010 - Inorganic Chemistry II Credit Hours: 3","CHEM 4410 - Macroscopic Physical Chemistry Credit Hours: 3","CHEM 4760 - Molecular Biochemistry I Credit Hours: 4"}'),
('Chemistry ',	'Third Year',	'Fall* OR Spring',	'{"HASS Core Elective Credit Hours: 4","Elective Credit Hours: 6","CHEM 4020 - Experimental Chemistry III: Inorganic and Physical Methods Credit Hours: 3","CHEM 4420 - Microscopic Physical Chemistry Credit Hours: 3"}'),
('Chemistry ',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Electives Credit Hours: 7","CHEM 4110 - Instrumental Methods of Analysis Credit Hours: 3","CHEM 4900 - Professional Development Seminar Credit Hours: 1","CHEM 4950 - Senior Experience Credit Hours: 2"}'),
('Chemistry ',	'Fourth Year',	'Spring',	'{"Electives Credit Hours: 9","CHEM 4120 - Experimental Chemistry IV: Physical and Instrumental Methods Credit Hours: 3","CHEM 4620 - Introduction to Polymer Chemistry Credit Hours: 3"}'),
('Chemistry - Industrial Chemistry Track',	'First Year',	'Fall',	'{"CHEM 1110 - Chemistry I with Advanced Lab Credit Hours: 4","CHEM 1900 - Chemistry for Life Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Chemistry - Industrial Chemistry Track',	'First Year',	'Spring',	'{"CHEM 1200 - Chemistry II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Chemistry - Industrial Chemistry Track',	'Second Year',	'Fall',	'{"CHEM 2110 - Equilibrium Chemistry and Quantitative Analysis Credit Hours: 3","CHEM 2120 - Experimental Chemistry I: Analytical Techniques Credit Hours: 2","CHEM 2250 - Organic Chemistry I Credit Hours: 3","CHME 2010 - Material, Energy, and Entropy Balances Credit Hours: 3","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","This course may be deferred until Spring and replaced by a HASS core elective."}'),
('Chemistry - Industrial Chemistry Track',	'Second Year',	'Spring',	'{"CHEM 2030 - Inorganic Chemistry I Credit Hours: 3","CHEM 2260 - Organic Chemistry II Credit Hours: 3","CHEM 2290 - Experimental Chemistry II: Synthesis and Characterization Credit Hours: 3","CHEM 4200 - Industrial Chemistry Credit Hours: 3","CHME 4010 - Transport Phenomena I Credit Hours: 4","If MATH-2400 was deferred to this semester, CHME-4010 should be deferred until the Summer Arch semester."}'),
('Chemistry - Industrial Chemistry Track',	'Third Year',	'Summer Arch Semester',	'{"BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CHEM 4410 - Macroscopic Physical Chemistry Credit Hours: 3"}'),
('Chemistry - Industrial Chemistry Track',	'Third Year',	'Fall* OR Spring',	'{"HASS Core Elective Credit Hours: 4","Elective Credit Hours: 4","CHEM 4030 - Experimental Chemistry III Abridged: Physical Methods Credit Hours: 2","CHEM 4420 - Microscopic Physical Chemistry Credit Hours: 3","CHEM 4760 - Molecular Biochemistry I Credit Hours: 4"}'),
('Chemistry - Industrial Chemistry Track',	'Fourth Year',	'Fall',	'{"CHEM 4110 - Instrumental Methods of Analysis Credit Hours: 3","CHEM 4900 - Professional Development Seminar Credit Hours: 1","CHEM 4950 - Senior Experience Credit Hours: 2"}'),
('Chemistry - Industrial Chemistry Track',	'Fourth Year',	'Spring',	'{"CHEM 4120 - Experimental Chemistry IV: Physical and Instrumental Methods Credit Hours: 3","CHEM 4620 - Introduction to Polymer Chemistry Credit Hours: 3"}'),
('Civil Engineering',	'First Year',	'Fall',	'{"HASS Elective Credit Hours: 4 (see footnote 2 below)","CHEM 1100 - Chemistry I Credit Hours: 4","CIVL 1200 - Engineering Graphics for Civil Engineers Credit Hours: 1","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Civil Engineering',	'First Year',	'Spring',	'{"HASS Elective Credit Hours: 4 (see footnote 2 below)","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MATH 1020 - Calculus II Credit Hours: 4","CIVL 1100 - Introduction to Civil and Environmental Engineering Credit Hours: 1","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Civil Engineering',	'Second Year',	'Fall',	'{"ENGR 2530 - Strength of Materials Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4","CIVL 2050 - Fluid Mechanics for Civil and Environmental Engineering Credit Hours: 4"}'),
('Civil Engineering',	'Second Year',	'Spring',	'{"CIVL 2030 - Introduction to Transportation Engineering Credit Hours: 4","CIVL 2630 - Introduction to Geotechnical Engineering Credit Hours: 4","CIVL 2670 - Introduction to Structural Engineering Credit Hours: 4","CIVL 2060 - Water Resources Engineering Credit Hours: 4"}'),
('Civil Engineering',	'Third Year',	'The Arch Summer Semester* ',	'{"HASS Elective Credit Hours: 4 (see footnote 2 below)","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","ENGR 4760 - Engineering Economics Credit Hours: 3","ENVE 4370 - Applied Hydrology and Design Credit Hours: 4"}'),
('Civil Engineering',	'Third Year',	'Fall OR Spring*',	'{"CE Design Elective Credit Hours: 3 
	(See footnote 6 below)","Free Elective Credit Hours: 4","ENGR 2090 - Engineering Dynamics Credit Hours: 4","CIVL 1300 - Beginning Programming in Civil and Environmental Engineering Credit Hours: 1","Credits / Units: 1","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2","Credits / Units: 2"}'),
('Civil Engineering',	'Fourth Year',	'Fall',	'{"CE Design Elective Credit Hours: 3
	(See footnote 6 below)","CE Technical Elective Credit Hours: 3
	(See footnote 6 below)","Free Elective Credit Hours: 4","Math and Science Elective Credit Hours: 4
	(See footnote 7 below)","HASS Elective Credit Hours: 4 (See footnote 2 below)"}'),
('Civil Engineering',	'Fourth Year',	'Spring',	'{"Basic Science Elective Credit Hours: 4
	(See footnote 8 below)","HASS Elective Credit Hours: 4 (See footnote 2 below)","Free Elective Credit Hours: 4","CIVL 4920 - Civil Engineering Capstone Design Credit Hours: 3","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1"}'),
('Cognitive Science',	'First Year',	'Fall',	'{"Free Elective, Credit Hours: 4","IHSS 1140 - Minds and Machines Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Cognitive Science',	'First Year',	'Spring',	'{"Free Elective Credit Hours: 4","COGS 2120 - Introduction to Cognitive Science Credit Hours: 4","CSCI 1200 - Data Structures Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Cognitive Science',	'Second Year',	'Fall',	'{"Free Elective Credit Hours: 4","CSCI 2200 - Foundations of Computer Science Credit Hours: 4","COGS 2340 - Introduction to Linguistics Credit Hours: 4","PHIL 2140 - Introduction to Logic Credit Hours: 4","[See Footnote 1]"}'),
('Cognitive Science',	'Second Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","CSCI 2300 - Introduction to Algorithms Credit Hours: 4","PSYC 4410 - Sensation and Perception Credit Hours: 4"}'),
('Cognitive Science',	'Third Year',	'The Arch Summer Semester*',	'{"Cognitive Science Elective Credit hours: 4 (See list of approved electives below)","Free Elective Credit Hours: 4","PSYC 2310 - Research Methods and Statistics I Credit Hours: 4"}'),
('Cognitive Science',	'Third Year',	'Fall OR Spring',	'{"Free Elective Credit Hours: 4"}'),
('Cognitive Science',	'Fourth Year',	'Fall',	'{"Cognitive Science Elective Credit Hours: 4 (see list of approved electives below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Cognitive Science',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Communication, Media, and Design',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4","Math Elective Credit Hours: 4"}'),
('Communication, Media, and Design',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4","Math Elective Credit Hours: 4","WRIT 2110 - Strategic Writing Credit Hours: 4"}'),
('Communication, Media, and Design',	'Second Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","Major Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","COMM 2660 - Introduction to Graphic Design Credit Hours: 4"}'),
('Communication, Media, and Design',	'Second Year',	'Spring',	'{"Major Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","Science Core Elective Credit Hours: 4","COMM 2520 - Communication Theory and Practice Credit Hours: 4"}'),
('Communication, Media, and Design',	'Third Year',	'The Arch Summer Semester*',	'{"Major Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Communication, Media, and Design',	'Third Year',	'Fall or Spring',	'{"HASS Core Elective Credit Hours: 4","Major Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Communication, Media, and Design',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","COMM 4930 - Pro-Seminar in Communication, Media, and Design Credit Hours: 4"}'),
('Communication, Media, and Design',	'Fourth Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Major Elective Credit Hours: 4"}'),
('Computer and Systems Engineering',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","ECSE 1010 - Introduction to Electrical, Computer, and Systems Engineering Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Computer and Systems Engineering',	'First Year',	'Spring',	'{"ECSE 2610 - Computer Components and Operations Credit Hours: 4","CSCI 1200 - Data Structures Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Computer and Systems Engineering',	'Second Year',	'Fall',	'{"ENGR 2350 - Embedded Control Credit Hours: 4","CSCI 2200 - Foundations of Computer Science Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Computer and Systems Engineering',	'Second Year',	'Spring',	'{"Science Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ECSE 2010 - Electric Circuits Credit Hours: 4","CSCI 2300 - Introduction to Algorithms Credit Hours: 4"}'),
('Computer Science',	'Fourth Year',	'Spring',	'{"CS Option/Capstone Credit Hours 4","Free Elective or Computer Science Option/Capstone Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Computer and Systems Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","ECSE 2660 - Computer Architecture, Networks, and Operating Systems Credit Hours: 4","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Computer and Systems Engineering',	'Third Year',	'Fall OR Spring',	'{"HASS Core Elective Credit Hours: 4","ECSE 2050 - Introduction to Electronics Credit Hours: 4","ECSE 2410 - Signals and Systems Credit Hours: 3","ECSE 2500 - Engineering Probability Credit Hours: 3","ECSE 2900 - ECSE Enrichment Seminar Credit Hours: 1","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Computer Science',	'First Year',	'Fall',	'{"HASS Core Elective  Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Computer Science',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","CSCI 1200 - Data Structures Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Computer Science',	'Second Year',	'Fall',	'{"Mathematics Option I Credit Hours: 4","HASS Core Elective Credit Hours: 4","CSCI 2200 - Foundations of Computer Science Credit Hours: 4","CSCI 2500 - Computer Organization Credit Hours: 4"}'),
('Computer Science',	'Second Year',	'Spring',	'{"Mathematics Option II Credit Hours: 4","HASS Core Elective Credit Hours: 4","CSCI 2300 - Introduction to Algorithms Credit Hours: 4","CSCI 2600 - Principles of Software Credit Hours: 4"}'),
('Computer Science',	'Third Year',	'The Arch Summer Semester*',	'{"Computer Science Option/Capstone or Free Elective Credit Hours: 4
	(See footnote 5 below)","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","CSCI 4210 - Operating Systems Credit Hours: 4"}'),
('Computer Science',	'Third Year',	'Fall OR Spring',	'{"Science Option Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","CSCI 4430 - Programming Languages Credit Hours: 4","Or CS Option/Capstone"}'),
('Computer Science',	'Fourth Year',	'Fall',	'{"Computer Science Option/Capstone Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","CSCI 4430 - Programming Languages Credit Hours: 4","Or CS Option/Capstone"}'),
('Computer Science',	'Fourth Year',	'Spring',	'{"CS Option/Capstone Credit Hours 4","Free Elective or Computer Science Option/Capstone Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Design, Innovation, and Society',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4
	(See footnote 1 below)","IHSS 1610 - Design and Innovation Studio I Credit Hours: 4","STSO 1110 - Science, Technology, and Society Credit Hours: 4"}'),
('Design, Innovation, and Society',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","​Science Core Elective Credit Hours: 4
	(See footnote 1 below)","STSO 2610 - Design and Innovation Studio II Credit Hours: 4","STSO 2210 - Design, Culture, and Society Credit Hours: 4"}'),
('Design, Innovation, and Society',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4
	(See footnote 1 below)","Complementary Area of Study Credit Hours: 4
	(See footnote 2 below)   ","ENGR 2020 - Design and Innovation Studio III Credit Hours: 4"}'),
('Design, Innovation, and Society',	'Second Year',	'Spring',	'{"Design Elective Credit Hours: 4
	(See footnote 3 below)   ","STS Advanced Option Credit Hours: 4
	(See footnote 4 below)   ","Science Core Elective Credit Hours: 4
	(See footnote 1 below)","Complementary Area of Study Credit Hours: 4
	(See footnote 2 below)"}'),
('Design, Innovation, and Society',	'Third Year',	'The Arch Summer Semester*',	'{"STS Advanced Option Credit Hours: 4
	(See footnote 4 below)   ","HASS Core Elective Credit Hours: 4","Complementary Area of Study Credit Hours: 4
	(See footnote 2 below)","STSO 4600 - Design and Innovation Studio A Credit Hours: 4","(see footnote 5 below)"}'),
('Design, Innovation, and Society',	'Third Year',	'Fall OR Spring',	'{"Science Core Elective Credit Hours: 4
	(See footnote 1 below)   ","HASS Core Elective Credit Hours: 4","Complementary Area of Study Credit Hours: 4
	(See footnote 2 below)","STSO 4605 - Design and Innovation Studio B Credit Hours: 4","STSO 4610 - Design and Innovation  Studio C Credit Hours: 4","(see footnote 5 below)"}'),
('Design, Innovation, and Society',	'Fourth Year',	'Fall',	'{"Science Core Elective Credit Hours: 4
	(See footnote 1 below)  ","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","STSO 4970 - Design and Innovation Senior Project Credit Hours: 4"}'),
('Design, Innovation, and Society',	'Fourth Year',	'Spring',	'{"Capstone Design Elective Credit Hours: 4
	(See footnote 6 below)   ","Free Elective Credit Hours: 4  ","Free Elective Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'First Year',	'Fall',	'{"CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","IHSS 1610 - Design and Innovation Studio I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","STSO 1110 - Science, Technology, and Society Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'First Year',	'Spring',	'{"ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1300 - Engineering Processes Credit Hours: 1","STSO 2610 - Design and Innovation Studio II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","STSO 2210 - Design, Culture, and Society Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Second Year',	'Fall',	'{"ENGR 2020 - Design and Innovation Studio III Credit Hours: 4","ENGR 2530 - Strength of Materials Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Second Year',	'Spring',	'{"Engineering Design Elective Credit Hours: 4
	(See footnotes 2, 4, and 5 below)","MANE 2110 - Numerical Methods and Programming for Engineers Credit Hours: 3","MANE 2710 - Thermodynamics Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"PDI Studio Advanced Option Credit Hours: 4
	(See footnotes 6, 7, and 8 below)","ENGR 2090 - Engineering Dynamics Credit Hours: 4","MANE 2720 - Fluid Mechanics Credit Hours: 3","MANE 4030 - Elements of Mechanical Design Credit Hours: 4"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Third Year',	'Fall OR Spring',	'{"PDI Studio Advanced Option Credit Hours: 4
	(See footnotes 6, 7, and 8 below)","ENGR 2300 - Electronic Instrumentation Credit Hours: 4","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MANE 4020 - Thermal and Fluids Engineering Laboratory Credit Hours: 2","MANE 4730 - Heat Transfer Credit Hours: 3"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Fourth Year',	'Fall',	'{"STS Advanced Option Credit Hours: 4
	(See footnotes 1, 2, and 10 below)","MANE Technical Elective Credit Hours: 3
	(See footnotes 2 and 11 below)","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","MANE 4040 - Mechanical Systems Laboratory Credit Hours: 2","STSO 4970 - Design and Innovation Senior Project Credit Hours: 4","MANE 4500 - Modeling and Control of Dynamic Systems Credit Hours: 3"}'),
('Design, Innovation, and Society/Mechanical Engineering',	'Fourth Year',	'Spring',	'{"STS Advanced Option Credit Hours: 4
	(See footnotes 1 and 2 below)","MANE Computation Elective Credit Hours: 3
	(See footnotes 2 and 11 below)","ENGR 1600 - Materials Science Credit Hours: 4","MANE 4260 - Multidisciplinary Capstone Design Credit Hours: 3","MANE 4510 - Control Systems Laboratory Credit Hours: 2"}'),
('Economics',	'First Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","MATH 1010 - Calculus I Credit Hours: 4","IHSS 1200 - Principles of Economics Credit Hours: 4"}'),
('Economics',	'First Year',	'Spring',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","Free Elective Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Economics',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","Free Elective Credit Hours: 4","ECON 2010 - Intermediate Microeconomic Theory Credit Hours: 4","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Economics',	'Second Year',	'Spring',	'{"Economics Elective Credit Hours: 4","Statistics Option Credit Hours: 4","Free Elective Credit Hours: 4","ECON 2020 - Intermediate Macroeconomic Theory Credit Hours: 4"}'),
('Economics',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4 (if Statistics Option did not count toward the Science Core)
	or Free Elective Credit Hours: 4 (if Statistics Option did count toward the Science Core)","Free Elective Credit Hours: 4","ECON 4570 - Econometrics Credit Hours: 4"}'),
('Economics',	'Third Year',	'Fall OR Spring',	'{"Economics Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Economics',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Culminating Experience Credit Hours: 4
	​(See list below)"}'),
('Economics',	'Fourth Year',	'Spring',	'{"Economics Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Electrical Engineering',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","ECSE 1010 - Introduction to Electrical, Computer, and Systems Engineering Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Electrical Engineering',	'First Year',	'Spring',	'{"Science Elective Credit Hours: 4","ENGR 2350 - Embedded Control Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Electrical Engineering',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","ECSE 2610 - Computer Components and Operations Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Electrical Engineering',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","ECSE 2010 - Electric Circuits Credit Hours: 4","ECSE 2500 - Engineering Probability Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Electrical Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 3-4
	(See footnote 2 below)","ECSE 2110 - Electrical Energy Systems Credit Hours: 3","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Electrical Engineering',	'Third Year',	'Fall OR Spring',	'{"Math/Science Elective Credit Hours: 4
	(See footnote 7 below)","ECSE 2050 - Introduction to Electronics Credit Hours: 4","ECSE 2100 - Fields and Waves I Credit Hours: 4","ECSE 2410 - Signals and Systems Credit Hours: 3","ECSE 2900 - ECSE Enrichment Seminar Credit Hours: 1"}'),
('Electronic Arts',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","Studio Elective Credit Hours: 4","Science Elective Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Hydrogeology',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4","ENVE 2110 - Introduction to Environmental Engineering Credit Hours: 4","ERTH 4070 - Sedimentology/Stratigraphy Credit Hours: 4","ERTH 4710 - Groundwater Hydrology Credit Hours: 4"}'),
('Electronic Arts',	'First Year',	'Spring',	'{"History/Theory Elective Credit Hours: 4","Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4"}'),
('Electronic Arts',	'Second Year',	'Fall',	'{"Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","Science Core Elective Credit Hours: 4","Studio Elective Credit Hours: 4"}'),
('Electronic Arts',	'Second Year',	'Spring',	'{"Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","Science Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Electronic Arts',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Electronic Arts',	'Third Year',	'Fall OR Spring',	'{"Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Electronic Arts',	'Fourth Year',	'Fall',	'{"Focus Area Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ARTS 4840 - Creative Seminar I Credit Hours: 4"}'),
('Electronic Arts',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ARTS 4850 - Creative Seminar II Credit Hours: 4"}'),
('Engineering Core Curriculum',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Engineering Core Curriculum',	'First Year',	'Spring',	'{" Science Elective Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","ENGR 1300 - Engineering Processes Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Engineering Core Curriculum',	'Second Year',	'Fall',	'{"Engineering Elective Credit Hours: 4","Engineering Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Engineering Core Curriculum',	'Second Year',	'Spring',	'{"Engineering Elective Credit Hours: 4","Engineering Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4"}'),
('Environmental Engineering',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","CIVL 1200 - Engineering Graphics for Civil Engineers Credit Hours: 1","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Environmental Engineering',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4","CHEM 1200 - Chemistry II Credit Hours: 4","CIVL 1100 - Introduction to Civil and Environmental Engineering Credit Hours: 1"}'),
('Environmental Engineering',	'Second Year',	'Fall',	'{"Biological Science Elective Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4","CIVL 2050 - Fluid Mechanics for Civil and Environmental Engineering Credit Hours: 4"}'),
('Environmental Engineering',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","ENVE 2110 - Introduction to Environmental Engineering Credit Hours: 4","CIVL 1300 - Beginning Programming in Civil and Environmental Engineering Credit Hours: 1","CIVL 2060 - Water Resources Engineering Credit Hours: 4"}'),
('Environmental Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","Free Elective I Credit Hours: 4","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","ENVE 4370 - Applied Hydrology and Design Credit Hours: 4"}'),
('Environmental Engineering',	'Third Year',	'Fall OR Spring*',	'{"Technical Elective Credit Hours: 3
	 (See footnote 8 below)","Professional Development -Technical Issues and Solutions Credit Hourse: 2
	 (See footnote 6 below)","Multidisciplinary Eng, Elective Credit Hours: 3
	 (See footnote 7 below)","ENVE 4320 - Environmental Chemodynamics Credit Hours: 4","ENVE 4340 - Physicochemical Processes in Environmental Engineering Credit Hours: 4"}'),
('Environmental Engineering',	'Fourth Year',	'Fall',	'{"Technical Elective Credits Hours: 3
	(See footnote 8 below)","Free Elective II Credit Hours: 4","ENVE 4330 - Introduction to Air Quality Credit Hours: 3","ENVE 4350 - Biological Processes in Environmental Engineering Credit Hours: 4"}'),
('Environmental Engineering',	'Fourth Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","Free Elective III Credit Hours: 4","Earth Science Elective
	(See footnote 9 below)","ENVE 4180 - Environmental Process Design Credit Hours: 3"}'),
('Environmental Science',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 1 below)","CHEM 1100 - Chemistry I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","ERTH 1100 - Geology I: Earth’s Interior Credit Hours: 3","ERTH 1150 - Geology I: Earth’s Interior Lab Credit Hours: 1"}'),
('Environmental Science',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","CHEM 1200 - Chemistry II Credit Hours: 4","ERTH 1200 - Geology II: Earth’s Surface Credit Hours: 3","ERTH 1250 - Geology ll: Earth’s Surface Lab Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Environmental Science',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 2250 - Organic Chemistry I Credit Hours: 3","ERTH 2160 - Introduction to Geobiology Credit Hours: ","ERTH 2210 - Field Methods Credit Hours: 3"}'),
('Environmental Science',	'Second Year',	'Spring',	'{"Concentration Course or Free Elective Credit Hours: 4","IENV 1910 - Environmental Seminar Credit Hours: 2","PHYS 1100 - Physics I Credit Hours: 4","ERTH 2200 - Environmental Data Analysis Credit Hours: 4"}'),
('Environmental Science',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 8","Concentration Course or Free Elective Credit Hours: 4","ERTH 4190 - Environmental Measurements Credit Hours: 4","(see footnote 4 below)"}'),
('Environmental Science',	'Third Year',	'Fall or Spring',	'{"Concentration Course or Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","BIOL 4880 - Global Environmental Change Credit Hours: 4","ERTH 4500 - Earth’s Climate: Past, Present, and Future Credit Hours: 4"}'),
('Environmental Science',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Culminating Experience Credit Hours: 4
	(See footnote 4 below) ","Concentration Course or Free Elective Credit Hours: 4","ERTH 4750 - Geographic Information Systems in the Sciences Credit Hours: 4"}'),
('Environmental Science',	'Fourth Year',	'Spring',	'{"Concentration Course and Free Elective Credit Hours: 16"}'),
('Games and Simulation Arts and Sciences',	'First Year',	'Fall',	'{"GSAS 1040 - Art for Interactive Media Credit Hours: 4","GSAS 2510 - Introduction to Game Design Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","GSAS 2540 - Introduction to Game Programming Credit Hours: 4","CSCI 1200 - Data Structures Credit Hours: 4","or Science Core Elective Credit Hours: 4 (CSCI 1200 Data Structures is required for only the CSCI & COGS concentrations)
","Science Core Elective Credit Hours: 4 (CSCI 1200 Data Structures is required for only the CSCI & COGS concentrations)","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","Science Core Elective Credit Hours: 4 (CSCI 1200 Data Structures is required for only the CSCI & COGS concentrations)"}'),
('Games and Simulation Arts and Sciences',	'Second Year',	'Fall',	'{"GSAS Concentration Course Credit Hours: 4","GSAS Concentration Course Credit Hours: 4","GSAS 2520 - Introduction to Game Storytelling Credit Hours: 4","GSAS 4520 - Game Development I Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'Second Year',	'Spring',	'{"GSAS Concentration Course​ Credit Hours: 4","GSAS Concentration Course​ Credit Hours: 4","GSAS 1600 - History and Culture of Games Credit Hours: 4","GSAS 4540 - Game Development II Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Science Core Elective Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'Third Year',	'Fall OR Spring',	'{"GSAS Concentration Course​ Credit Hours: 4","GSAS Concentration Course​ Credit Hours: 4","GSAS 4510 - Experimental Game Design Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4","PHYS 1050 - General Physics Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'Fourth Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","GSAS Concentration Course​ Credit Hours: 4","Free Elective Credit Hours: 4","GSAS 4990 - GSAS Capstone Credit Hours: 4"}'),
('Games and Simulation Arts and Sciences',	'Fourth Year',	'Spring',	'{"GSAS Concentration Course Credit Hours: 4","GSAS Concentration Course Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Geology',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","ERTH 1100 - Geology I: Earth’s Interior Credit Hours: 3","ERTH 1150 - Geology I: Earth’s Interior Lab Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Geology',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","CHEM 1200 - Chemistry II Credit Hours: 4","ERTH 1200 - Geology II: Earth’s Surface Credit Hours: 3","ERTH 1250 - Geology ll: Earth’s Surface Lab Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Geology',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","ERTH 2330 - Earth Materials Credit Hours: 4","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Geology',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","ERTH 2100 - Introduction to Geophysics Credit Hours: 4","ERTH 2140 - Introduction to Geochemistry Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Geology',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Elective Credit Hours: 8 credits","Free Elective: 4 credits","ERTH 4190 - Environmental Measurements Credit Hours: 4"}'),
('Geology',	'Third Year',	'Fall or Spring',	'{"Biology Requirement Credit Hours: 4
	(See footnotes 2 and 4 below)","Elective Credit Hours: 8","ERTH 4XXX selected from the ERTH Electives: (4 credits)"}'),
('Geology',	'Fourth Year',	'Fall',	'{"Electives Credit Hours: 8","ERTH Electives Credit Hours: 4","ERTH 2120 - Structural Geology Credit Hours: 4"}'),
('Geology',	'Fourth Year',	'Spring',	'{"Culminating Experience Credit Hours: 3-4
	(See footnote 3 below)","Electives Credit Hours: 6-7 ","ERTH 4970 - Out-of-Classroom Experience in Earth Sciences Credit Hours: 2 to 4","ERTH 4980 - Undergraduate Research Thesis Credit Hours: 2 to 4"}'),
('Hydrogeology',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","ERTH 1100 - Geology I: Earth’s Interior Credit Hours: 3","ERTH 1150 - Geology I: Earth’s Interior Lab Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Hydrogeology',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","CHEM 1200 - Chemistry II Credit Hours: 4","ERTH 1200 - Geology II: Earth’s Surface Credit Hours: 3","ERTH 1250 - Geology ll: Earth’s Surface Lab Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Hydrogeology',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CSCI XXXX  Computer Science Elective Credit Hours: 4
	(See footnote 2 below)","ERTH 2120 - Structural Geology Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Hydrogeology',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","ERTH 2100 - Introduction to Geophysics Credit Hours: 4","ERTH 2140 - Introduction to Geochemistry Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Hydrogeology',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 8","Free Elective Credit Hours: 4","ERTH 4190 - Environmental Measurements Credit Hours: 4"}'),
('Hydrogeology',	'Third Year',	'Fall or Spring',	'{"Elective Credit Hours: 8","Biology Requirement Credit Hours: 4
	(See footnote 1 below)","MATH 2400 - Introduction to Differential Equations Credit Hours: 4"}'),
('Hydrogeology',	'Fourth Year',	'Spring',	'{"Culminating Experience Credit Hours: 4
	(See footnote 3 below)","Electives Credit Hours: 8","ERTH 4970 - Out-of-Classroom Experience in Earth Sciences Credit Hours: 2 to 4","ERTH 4980 - Undergraduate Research Thesis Credit Hours: 2 to 4"}'),
('Industrial and Management Engineering',	'First Year',	'Fall',	'{"HASS Core Elective I Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1300 - Engineering Processes Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Industrial and Management Engineering',	'First Year',	'Spring',	'{"HASS Core Elective II Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4"}'),
('Industrial and Management Engineering',	'Second Year',	'Fall',	'{"HASS Core Elective III Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","ISYE 2530 - Information and Data Systems Credit Hours: 4"}'),
('Industrial and Management Engineering',	'Second Year',	'Spring',	'{"ISYE 2210 - Production and Operations Management Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","ISYE 4140 - Statistical Analysis Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Industrial and Management Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective IV Credits Hours: 4","ENGR 4760 - Engineering Economics Credit Hours: 3","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","ISYE 4600 - Operations Research Methods Credit Hours: 4"}'),
('Industrial and Management Engineering',	'Third Year',	'Fall OR Spring',	'{"Technical Elective I  Credit Hours: 3","Technical Elective II  Credit Hours: 3
	(See footnote 7 below)","HASS Core Elective V Credit Hours: 4","Management Elective I Credit Hours: 4","ISYE 4290 - Discrete Event Simulation Modeling and Analysis Credit Hours: 4"}'),
('Industrial and Management Engineering',	'Fourth Year',	'Fall',	'{"Technical Elective III  Credit Hours: 3
	(See footnote 7 below) ","Free Elective I Credit Hours: 4","Science Elective Credit Hours: 4","ISYE 4210 - Design and Analysis of Supply Chains Credit Hours: 3"}'),
('Industrial and Management Engineering',	'Fourth Year',	'Spring',	'{"Technical Elective IV Credit Hours:3
	(See footnote 7 below)","Free Elective II Credit Hours: 4","Free Elective III Credit Hours: 4","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","ISYE 4270 - Multidisciplinary Capstone Design Credit Hours: 3"}'),
('Information Technology and Web Science',	'First Year',	'Fall',	'{"Concentration Course Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","ITWS 1100 - Introduction to Information Technology and Web Science Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Information Technology and Web Science',	'First Year',	'Spring',	'{"Math Elective Credit Hours: 4","Physical-Science Elective Credit Hours: 4","CSCI 1200 - Data Structures Credit Hours: 4","ITWS 1220 - IT and Society Credit Hours: 4"}'),
('Information Technology and Web Science',	'Second Year',	'Fall',	'{"Technical Track Course #1 (see chart in previous section)","Concentration Course Credit Hours:  4","HASS Elective Credit Hours: 4
	(See footnote 1 below)","ITWS 2110 - Web Systems Development Credit Hours: 4"}'),
('Information Technology and Web Science',	'Second Year',	'Spring',	'{"Technical Track Course #2 (see chart in previous section)","HASS Elective Credit Hours: 4
	(See footnote 1 below)","ITWS 2210 - Introduction to Human Computer Interaction Credit Hours: 4","ITWS 4500 - Web Science Systems Development Credit Hours: 4"}'),
('Information Technology and Web Science',	'Third Year',	'The Arch Summer Semester*',	'{"Concentration Course Credit Hours: 4","Concentration Course Credit Hours: 4","Life Science Elective: Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Information Technology and Web Science',	'Third Year',	'Fall OR Spring',	'{"Technical Track Course #3 (see chart in previous section)","HASS Elective Credit Hours: 4 (see footnote 1 below)","ITWS 4310 - Managing IT Resources Credit Hours: 4"}'),
('Information Technology and Web Science',	'Fourth Year',	'Fall',	'{"ITWS 4100 - Information Technology and Web Science Capstone Credit Hours: 4
	(Professional track)
	or","ITWS 4990 - Senior Thesis Credit Hours: 3
	(Research track)","Concentration Course Credit Hours: 4","Concentration Course Credit Hours: 4","Free Elective  Credit Hours:  4"}'),
('Information Technology and Web Science',	'Fourth Year',	'Spring',	'{"ITWS 4990 - Senior Thesis  Credit Hours: 3
(Research track only)
","Concentration Capstone Course/Experience Credit Hours: 4","Concentration Course Credit Hours: 4","HASS Elective Credit Hours: 4
(See footnote 1 below)
","Free Elective Credit Hours: 4"}'),
('Materials Engineering',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MTLE 1200 - Introduction to Materials Engineering Credit Hours: 1"}'),
('Materials Engineering',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","ENGR 1600 - Materials Science Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Materials Engineering',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","MTLE 2100 - Structure of Engineering Materials Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Materials Engineering',	'Second Year',	'Spring',	'{"Science Elective, Credit Hours 4","CSCI 1190 - Beginning Programming for Engineers Credit Hours: 1","ENGR 2050 - Introduction to Engineering Design Credit Hours: 4","ENGR 2250 - Thermal and Fluids Engineering I Credit Hours: 4","MTLE 4200 - Electrical and Optical Properties of Materials Credit Hours: 4"}'),
('Materials Engineering',	'Third Year',	'The Arch Summer Semester*',	'{"Restricted Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MTLE 2500 - Materials Laboratory Skills Credit Hours: 1","MTLE 4250 - Mechanical Properties of Materials Credit Hours: 4"}'),
('Music',	'Third Year',	'The Arch Summer Semester*',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Materials Engineering',	'Third Year',	'Fall OR Spring*',	'{"HASS Core Elective Credit Hours: 4","Free Elective I Credit Hours: 4","MTLE 4100 - Thermodynamics of Materials Credit Hours: 4","MTLE 4910 - Materials Selection Credit Hours: 3","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Materials Engineering',	'Fourth Year',	'Fall',	'{"Materials Elective I Credit Hours: 3
	(See footnote 1 below)","Free Elective II Credit Hours: 4
	(See footnote 1 below)","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","MTLE 4150 - Kinetics in Materials Systems Credit Hours: 4","MTLE 4500 - Computational Materials Design Credit Hours: 3"}'),
('Materials Engineering',	'Fourth Year',	'Spring',	'{"Materials Elective II","Free Elective III ","MTLE 4400 - Materials Synthesis and Processing Credit Hours: 4","MTLE 4920 - Multidisciplinary Capstone Design Credit Hours: 3"}'),
('Mathematics',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MATH 1900 - Art and Science of Mathematics I Credit Hours: 1","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Mathematics',	'First Year',	'Spring',	'{"Elective Credit Hours: 4","Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Mathematics',	'Second Year',	'Fall',	'{"Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Mathematics',	'Second Year',	'Spring',	'{"Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","MATH 4xxx Math Core I Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4"}'),
('Mathematics',	'Third Year',	'The Arch Summer Semester*',	'{"MATH Option Credit Hours: 4","Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","MATH 4xxx Math Core II Credit Hours: 4"}'),
('Mathematics',	'Third Year',	'Fall OR Spring',	'{"Capstone I","Elective Credit Hours: 4","Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Mathematics',	'Fourth Year',	'Fall',	'{"Capstone II","Elective Credit Hours: 4","Elective Credit Hours: 4","Math Option Credit Hours: 4"}'),
('Mathematics',	'Fourth Year',	'Spring',	'{"Capstone III","Elective Credit Hours: 4","Elective Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'First Year',	'Fall (17 credits)',	'{"
HASS Core Elective Credit Hours: 4 
	(See footnote 3 below)
","CHEM 1100 - Chemistry I Credit Hours: 4","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'First Year',	'Spring (17 credits)',	'{"HASS Core Elective Credit Hours: 4
	 (See footnote 3 below)","ENGR 1300 - Engineering Processes Credit Hours: 1","ENGR 1600 - Materials Science Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'Second Year',	'Fall (17 credits)',	'{"STSS 4100 - Professional Development II Credit Hours: 2
	(See footnotes 1 and 4 below)","ENGR 2530 - Strength of Materials Credit Hours: 4","MANE 2710 - Thermodynamics Credit Hours: 3","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'Second Year',	'Spring (15 credits)',	'{"SoE-2….  Engineering Design Elective Credit Hours: 4 
	(See footnotes 1, 5, and 6 below)","ENGR 2300 - Electronic Instrumentation Credit Hours: 4","MANE 2110 - Numerical Methods and Programming for Engineers Credit Hours: 3","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'Third Year',	'The Arch Summer Semester* (15 credits)',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","ENGR 2090 - Engineering Dynamics Credit Hours: 4","MANE 2720 - Fluid Mechanics Credit Hours: 3","MANE 4030 - Elements of Mechanical Design Credit Hours: 4"}'),
('Mechanical Engineering Curriculum',	'Third Year',	'Fall OR Spring (17 credits)',	'{"Free Elective Credit Hours: 4
	(See footnote 6 below)","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MANE 4500 - Modeling and Control of Dynamic Systems Credit Hours: 3","MANE 4730 - Heat Transfer Credit Hours: 3","MANE 4040 - Mechanical Systems Laboratory Credit Hours: 2","MANE 4740 - Thermal and Fluids Engineering Laboratory Credit Hours: 2"}'),
('Mechanical Engineering Curriculum',	'Fourth Year',	'Fall  (16 credits)',	'{"HASS Core Elective Credit hours:  4
	 (See footnote 3 below)","MANE 4…. Technical Elective Credit hours:  3
	 (See footnotes 1 and 9 below)","MANE 4…. Computation Elective Credit hours:  3 
	(See footnotes 1 and 9 below)","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","MANE 4260 - Multidisciplinary Capstone Design Credit Hours: 3","MANE 4510 - Control Systems Laboratory Credit Hours: 2"}'),
('Mechanical Engineering Curriculum',	'Fourth Year',	'Spring 15 credits)',	'{"SoE/SoS-4…. Technical Elective II Credit hours:  3
	( See footnotes 1 and 9 below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective  Credit Hours: 4
	 (See footnote 3 below) ​"}'),
('Music',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1, 2 below)","Private Music Lesson or Ensemble Credit Hours: 1
	(See footnote 3 below)","ARTS 2020 - Music and Technology I Credit Hours: 4","ARTS 2380 - Music and Sound I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4"}'),
('Music',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1, 2 below)","Private Music Lesson or Ensemble Credit Hours: 1
	(See footnote 3 below)","ARTS 4160 - Music and Technology II Credit Hours: 4","ARTS 4380 - Music and Sound II Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4"}'),
('Music',	'Second Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Private Music Lesson or Ensemble Credit Hours: 1
	(See footnote 3 below)","ARTS 2540 - The Multimedia Century Credit Hours: 4"}'),
('Music',	'Second Year',	'Spring',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Private Music Lesson or Performance Ensemble Credit Hours: 1
	(See footnote 3 below)"}'),
('Music',	'Third Year',	'Fall OR Spring',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4","ARTS 4390 - Composition Seminar Credit Hours: 4 (course can be repeated multiple times for additional credit)","ARTS 4880 - Interdisciplinary Research Seminar Credit Hours: 4"}'),
('Music',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Music',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Nuclear Engineering Curriculum',	'First Year',	'Fall ',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","ENGR 1100 - Introduction to Engineering Analysis Credit Hours: 4","ENGR 1200 - Engineering Graphics and CAD Credit Hours: 1","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1100 - Physics I Credit Hours: 4"}'),
('Nuclear Engineering Curriculum',	'First Year',	'Spring ',	'{"HASS Core Elective Credit Hours: 4
	 (See footnote 3 below)","CHEM 1100 - Chemistry I Credit Hours: 4","MANE 1100 - Introduction to Nuclear Engineering Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1200 - Physics II Credit Hours: 4"}'),
('Nuclear Engineering Curriculum',	'Second Year',	'Fall ',	'{"MANE 2710 - Thermodynamics Credit Hours: 3","MANE 2830 - Nuclear Phenomena for Engineering Applications Credit Hours: 4","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","STSO 4100 - Professional Development  2 –Technical Issues and Solutions Credit Hours: 2"}'),
('Nuclear Engineering Curriculum',	'Second Year',	'Spring ',	'{"Materials Science Elective Credit Hours: 4 
	(See footnotes 1, 5, and 7 below)","MANE 2110 - Numerical Methods and Programming for Engineers Credit Hours: 3","MANE 2400 - Fundamentals of Nuclear Engineering Credit Hours: 4","MANE 2720 - Fluid Mechanics Credit Hours: 3","MANE 4350 - Nuclear Instrumentation and Measurement Credit Hours: 3"}'),
('Nuclear Engineering Curriculum',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 3 below)","SoE 2…. Engineering Design Elective  Credit Hours: 4 
	(See footnote 8 below)","ENGR 2600 - Modeling and Analysis of Uncertainty Credit Hours: 3","MANE 4500 - Modeling and Control of Dynamic Systems Credit Hours: 3"}'),
('Nuclear Engineering Curriculum',	'Third Year',	'Fall* OR Spring',	'{"HASS Core Elective Credit Hours: 4
	 (See footnote 3 below)","ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1","MANE 4400 - Nuclear Power Systems Engineering Credit Hours: 4","MANE 4470 - Radiological Engineering Credit Hours: 3","MANE 4480 - Physics of Nuclear Reactors Credit Hours: 4"}'),
('Nuclear Engineering Curriculum',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4 
	(See footnote 1 below)","HASS Core Elective  Credit Hours: 4
	 (See footnote 3 below)","MANE 4…. NE Technical Elective Credit hours: 3
	(See footnotes 1 and 11 below)","MANE 4380 - Nuclear Engineering Senior Design Project I Credit Hours: 1","MANE 4370 - Nuclear Engineering Laboratory Credit Hours: 4"}'),
('Nuclear Engineering Curriculum',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4
	 (See footnote 1 below)","MANE 4…. Nuclear Engineering Laboratory II Credit Hours: 3
	(See footnote 10 below)","MANE 4…. NE Technical Elective II Credit Hours: 3
	 (See footnotes 1 and 11 below)","MANE 4390 - Nuclear Engineering Senior Design Project II Credit Hours: 2"}'),
('Philosophy',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","Science Core Elective Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4"}'),
('Philosophy',	'First Year',	'Spring',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 2 below)","Philosophy Elective Credit Hours: 4
	(See footnote 3 below)","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4"}'),
('Philosophy',	'Second Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnote 2 below)","Free Elective Credit Hours: 4","PHIL 2140 - Introduction to Logic Credit Hours: 4"}'),
('Philosophy',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Philosophy',	'Third Year',	'The Arch Summer Semester*',	'{"Philosophy Elective Credit Hours: 4
	(See footnote 3 below)","HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4"}'),
('Philosophy',	'Third Year',	'Fall OR Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Philosophy',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4 ","Free Elective Credit Hours: 4 ","Free Elective Credit Hours: 4 ","PHIL 4990 - Capstone Experience in Philosophy Credit Hours: 3 to 6"}'),
('Philosophy',	'Fourth Year',	'Spring',	'{"Philosophy Elective Credit Hours: 4
	(See footnote 3 below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Physics',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 1 below)","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","PHYS 1150 - Honors Physics I Credit Hours: 4"}'),
('Physics',	'First Year',	'Spring',	'{"Free Elective Credit Hours: 4","BIOL 1010 - Introduction to Biology Credit Hours: 3","BIOL 1015 - Introduction to Biology Laboratory Credit Hours: 1","MATH 1020 - Calculus II Credit Hours: 4","PHYS 1250 - Honors Physics II Credit Hours: 4"}'),
('Physics',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 1 below)","CHEM 1100 - Chemistry I Credit Hours: 4","MATH 2400 - Introduction to Differential Equations Credit Hours: 4","PHYS 2210 - Quantum Physics I Credit Hours: 4"}'),
('Physics',	'Second Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 1 below)","MATH 2010 - Multivariable Calculus and Matrix Algebra Credit Hours: 4","PHYS 2220 - Quantum Physics II Credit Hours: 4","PHYS 4330 - Theoretical Mechanics Credit Hours: 4"}'),
('Sustainability Studies',	'Second Year',	'Spring',	'{"SUST Advanced Option Credit Hours: 4
	(See footnote 4 below)","Science Core Elective Credit Hours: 4
	(See footnote 2 below)","CAS Course Option Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4"}'),
('Physics',	'Third Year',	'The Arch Summer Semester*',	'{"HASS Core Elective Credit Hours: 4
	(See footnotes 1 and 9 below)","Mathematics Elective Credit Hours: 4
	(See footnotes 4 and 9 below)","PHYS 2962 Computing for Physicists Free Elective Credit Hours: 2
	(See footnote 6 below)","PHYS 2963 Mathematical Physics Free Elective Credit Hours: 2
	(See footnote 7 below)","PHYS 2350 - Experimental Physics Credit Hours: 4"}'),
('Physics',	'Third Year',	'Fall OR Spring*',	'{"Free Elective Credit Hours: 4","PHYS 4100 - Introductory Quantum Mechanics Credit Hours: 4","PHYS 4210 - Electromagnetic Theory Credit Hours: 4","PHYS 4420 - Thermodynamics and Statistical Mechanics Credit Hours: 4"}'),
('Physics',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnote 1 below)","Mathematics Elective Credit Hours: 4
	(See footnote 4 below)","Culminating Experience Credit Hours: 4
	(See footnote 5 below)"}'),
('Physics',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	(See footnote 1 below)"}'),
('Psychological Science',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","CSCI 1100 - Computer Science I Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","PSYC 1200 - Introduction to Psychological Science Credit Hours: 4"}'),
('Psychological Science',	'First Year',	'Spring',	'{"Science Core Elective Credit Hours: 4","PSYC 2/4000 Core Content Elective Credit Hours: 4
	(See footnote 1 below)","MATH 1020 - Calculus II Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","PSYC 2310 - Research Methods and Statistics I Credit Hours: 4"}'),
('Psychological Science',	'Second Year',	'Fall',	'{"Science Core Elective Credit Hours: 4","PSYC 2/4000 Core Content Elective Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","PSYC 4310 - Research Methods and Statistics II Credit Hours: 4"}'),
('Psychological Science',	'Second Year',	'Spring',	'{"PSYC 2/4000 Core Content Elective Credit Hours: 4
	(See footnote 1 below)","Psychology Elective Credit Hours: 4
	(See footnote 2 below)","Science Core Elective Credit Hours: 4","PSYC 4350 - Mathematical Methods in Psychological Science Credit Hours: 4"}'),
('Psychological Science',	'Third Year',	'The Arch Summer Semester*',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4
	 "}'),
('Psychological Science',	'Third Year',	'Fall OR Spring',	'{"PSYC 2/4000 Core Content Elective Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4"}'),
('Psychological Science',	'Fourth Year',	'Fall',	'{"Psychology Elective Credit Hours: 4
	(See footnote 2 below)","Free Elective Credit Hours: 4","Free Elective Credit Hours: 4 ","Free Elective Credit Hours: 4  "}'),
('Psychological Science',	'Fourth Year',	'Spring',	'{"Free Elective Credit Hours: 4","Free Elective Credit Hours: 4 ","Free Elective Credit Hours: 4  ","PSYC 4XXX Advanced Seminar in Psychology Credit Hours: 4
	Or","Undergraduate Research Project Credit Hours: 4
	Or","Honors Thesis Credit Hours: 4"}'),
('Science, Technology, and Society',	'First Year',	'Fall',	'{"Science Core Elective Credit Hours: 4
	(See footnote 6 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4","STSO 1110 - Science, Technology, and Society Credit Hours: 4"}'),
('Science, Technology, and Society',	'First Year',	'Spring',	'{"Science Core Elective Credit Hours: 4
	(See footnote 6 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Intermediate STS course Credit Hours: 4
	(See footnote 2 below)","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","MATH 1020 - Calculus II Credit Hours: 4"}'),
('Science, Technology, and Society',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Free Elective Credit Hours: 4
	(See footnote 7 below)","Science Core Elective Credit Hours: 4
	(See footnote 6 below)","STSO 2100 - Investigating Society Credit Hours: 4"}'),
('Science, Technology, and Society',	'Second Year',	'Spring',	'{"CAS Course Credit Hours: 4
	(See footnote 8 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Science Core Elective Credit Hours: 4
	(See footnote 6 below)","STSO 4300 - Sustainability and STS Sustainability Careers Credit Hours: 4"}'),
('Science, Technology, and Society',	'Third Year',	'The Arch Summer Semester*',	'{"Advanced STS Course Credit Hours: 4
	(See footnote 3 below)","Advanced STS Course Credit Hours: 4
	(See footnote 3 below)","Free Elective Credit Hours: 4
	(See footnote 7 below)"}'),
('Science, Technology, and Society',	'Third Year',	'Fall OR Spring',	'{"CAS Course Credit Hours: 4
	(See footnote 8 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","HASS Core Elective Credit Hours: 4
	(See footnote 5 below)","Free Elective Credit Hours: 4
	(See footnote 7 below)"}'),
('Science, Technology, and Society',	'Fourth Year',	'Fall',	'{"Free Elective Credit Hours: 4
	(See footnote 7 below)","CAS Course Credit Hours: 4
	(See footnote 8 below)","Free Elective Credit Hours: 4
	(See footnote 7 below)","STSO 4980 - Research Design Credit Hours: 4"}'),
('Science, Technology, and Society',	'Fourth Year',	'Spring',	'{"CAS Course Credit Hours: 4
	(See footnote 8 below)","Free Elective Credit Hours: 4
	  (See footnote 7 below)","Free Elective Credit Hours: 4
	(See footnote 7 below)","STSO 4990 - STS and Sustainability Senior Project Credit Hours: 4"}'),
('Sustainability Studies',	'First Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4
	(See footnote 2 below)","IHSS 1240 - Sustainability Debates Credit Hours: 4","(see footnote 3 below)","MATH 1500 - Calculus for Architecture, Management, and HASS Credit Hours: 4","MATH 1010 - Calculus I Credit Hours: 4"}'),
('Sustainability Studies',	'First Year',	'Spring',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4
	(See footnote 2 below)","STSO 2300 - Environment and Society Credit Hours: 4","MATH 1520 - Mathematical Methods in Management and Economics Credit Hours: 4","(see footnote 3 below)","or MATH 1020 - Calculus II Credit Hours: 4"}'),
('Sustainability Studies',	'Second Year',	'Fall',	'{"HASS Core Elective Credit Hours: 4","Science Core Elective Credit Hours: 4
	(See footnote 2 below)","Free Elective Credit Hours: 4","STSO 2100 - Investigating Society Credit Hours: 4"}'),
('Sustainability Studies',	'Third Year',	'The Arch Summer Semester*',	'{"SUST Advanced Option Credit Hours: 4
	(See footnote 4 below)","SUST Advanced Option Credit Hours: 4
	(See footnote 4 below)","Free Elective Credit Hours: 4"}'),
('Sustainability Studies',	'Third Year',	'Fall OR Spring',	'{"SUST Advanced Option Credit Hours: 4
	(See footnote 4 below)","CAS Course Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","HASS Core Elective Credit Hours: 4"}'),
('Sustainability Studies',	'Fourth Year',	'Fall',	'{"CAS Course Credit Hours: 4
	(See footnote 1 below)","Free Elective Credit Hours: 4","STSO 4300 - Sustainability and STS Sustainability Careers Credit Hours: 4","STSO 4980 - Research Design Credit Hours: 4"}'),
('Sustainability Studies',	'Fourth Year',	'Spring',	'{"CAS Course Credit Hours: 4
	(See footnote 1 below)","HASS Core Elective Credit Hours: 4","Free Elective Credit Hours: 4","STSO 4990 - STS and Sustainability Senior Project Credit Hours: 4"}');

-- 2021-11-29 20:40:55.646847+00
