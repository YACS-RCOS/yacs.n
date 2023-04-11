-- *CODE FOR TABLES, MAKE SURE THIS IS RAN FIRST TO CREATE THE TABLES AND AVOID ERRORS*

CREATE TABLE PATHWAYNAME(
    id SERIAL PRIMARY KEY,
    nameOfPath TEXT,
    compatibleMinors text[]
);

CREATE TABLE REQUIREMENTSFORPATH(
    id SERIAL PRIMARY KEY,
    chooses text[],
    classOne text[],
    classTwo text[],
    classThree text[]
);

CREATE TABLE COMBINE(
    require_id INTEGER,
    pathway_id INTEGER,
    majorName TEXT,
    PRIMARY KEY (require_id, pathway_id),
    CONSTRAINT fk_require FOREIGN KEY(require_id) REFERENCES REQUIREMENTSFORPATH(id),
    CONSTRAINT fk_path FOREIGN KEY(pathway_id) REFERENCES PATHWAYNAME(id)
);

-- CODE THAT STORES ALL THE PATHWAY NAMES AND THEIR RESPECTIVE MINORS

INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Creative Design and Innovation"', '{"Behavioral and Cognitive Neuroscience"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Electronic Art"', '{"Electronic Arts Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Graphic Design"', '{"Graphic Design Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Studio Arts"', '{"Studio Arts"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Artificial Intelligence"', '{"Cognitive Science of Artificial Intelligence Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Behavioral and Cognitive Neuroscience"', '{"Behavioral and Cognitive Neuroscience"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Linguistics"', '{"Linguistics Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Mind, Brain, and Intelligence"', '{"Cognitive Science Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Understanding Human Behavior"', '{"General Psychology Minor and Psychological Science Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Well-being: Body and Mind"', '{"Well-being"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Fact and Fiction"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Literature and Creative Writing"', '{"Literature and Creative Writing Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Strategic Communication"', '{"Strategic Communication Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Environmental Future"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Sustainability"', '{"Sustainability Studies Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics"', '{"Economics Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Banking and Finance"', '{"Economics of Banking and Finance Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Decision-Making"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Healthcare Market"', '{"Economics of Healthcare Markets"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Policy and Regulation"', '{"Economics of Policy and Regulations"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Quantitative Modeling"', '{"Economics of Quantitative Modeling"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Economics of Technology and Innovation"', '{"Economics of Technology and Innovation Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Information Technology and Web Sciences"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Interactive Media/Data Design"', '{"Graphic Design Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Living in a World of Data"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Chinese Language"', '{"Chinese Language Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Foreign Language"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Game Studies"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Media and Culture"', '{"Media and Culture Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Music and Culture"', '{"Music Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Music Composition and Production"', '{"Music Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Music Performance"', '{"Music Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Video, Performance, and Social Practice"', '{"Video, Performance, and Social Practice Electronic Arts Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Extent and Limits of Rationality"', '{}'
);

INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Logical Thinking"', '{"Philosophy of Logic, Computation, and Mind Minor"}'
);

INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Philosophy"', '{"Philosophy Minor"}'
);

INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Thinking with Science"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Art History, Theory, and Criticits"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Design, Innovation, and Society"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Ethics, Integrity, and Social Responsibility"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Gender, Race, Sexuality, Ethnicity, and Social Change"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"History"', '{"History Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Law and Policy"', '{"Law and Policy Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Public Health"', '{"Public Health Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Science, Technology, and Society"', '{"Science, Technology, and Society Minor"}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Transfer Student Arts and Humanitity"', '{}'
);
INSERT INTO PATHWAYNAME(nameOfPath, compatibleMinors) VALUES (
    '"Transfer Student Social Science"', '{}'
);


-- CODE THAT LISTS ALL THE CLASSES AND THEIR RESPECTIVE OPTIONS

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":','"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1960 - Remixing in Digital Culture",
                    "IHSS 1960 - Worlds on Display",
                    "IHSS 1960 - Game Sound and Musical Play",
                    "ARTS 1020 - Digital Imaging",
                    "ARTS 1030 - Digital Filmmaking",
                    "ARTS 1380 - Fundamentals of Music and Sound",
                    "IHSS 1170 - History of Animation",
                    "IHSS 1700 - Songwriting Workshop",
                    "IHSS 1040 - Documentary in the 21st Century Identity Production"'],
    ARRAY['"COMM 4960 - Color Theory",
                    "ARTS 4960- Performance Art",
                    "ARTS 2210 - Sculpture I",
                    "ARTS 2220 - Fundamentals of 2D Design",
                    "ARTS 2380 - Music and Sound I",
                    "ARTS 2700 - Sound Recording and Production I",
                    "ARTS 2960 - Topics in the Arts Credit Hours 2 to 4(Radical Graphics/Screenprinting)",
                    "ARTS 4210 - Sculpture II",
                    "ARTS 4960 - Topics in the Arts Credit Hours 2 to 4(History and Analysis of Western Music)",
                    "COGS 2120 - Introduction to Cognitive Science",
                    "COGS 4620 - Cognitive Engineering",
                    "COMM 2570 - Typography",
                    "COMM 2660 - Introduction to Graphic Design",
                    "COMM 4320 - Visual Poetics and Narrative",
                    "COMM 4460 - Visual Design Theory and Application",
                    "COMM 4960 - Topics in Communication (Brand Identity Design)",
                    "PSYC 2220 - Human Factors in Design"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":','"Choose remaining credits from the following":', NULL],
    ARRAY[' "IHSS 1960 - Behind the Television Screen",
                    "IHSS 1960 – Remixing in Digital Culture",
                    "ARTS 1020 - Digital Imaging",
                    "ARTS 1050 - Art History",
                    "IHSS 1030 - Behind the TV Screen",
                    "IHSS 1040 - Documentary in the 21st Century Identity Production"'],
    ARRAY['"ARTS 4960 Performance Art",
                    "ARTS 2040 - Intermediate Digital Imaging",
                    "ARTS 2060 - 2D Experimental Animation",
                    "ARTS 2070 - Graphic Storytelling",
                    "ARTS 2230 - 3D Digital Modeling",
                    "ARTS 2700 - Sound Recording and Production I",
                    "ARTS 4060 - 3D Visual Effects",
                    "ARTS 4070 - 3D Animation",
                    "ARTS 4090 - Art and Code and Interactivity",
                    "ARTS 4860 - Advanced Digital Imaging"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, with at least 4 credits at the 4000-level":', NULL, NULL],
    ARRAY['"IHSS 1560 - Media and Society",
                    "IHSS 1562 - Life in Color",
                    "COMM 2520 - Communication Theory and Practice",
                    "COMM 2570 - Typography",
                    "COMM 2660 - Introduction to Graphic Design",
                    "COMM 4320 - Visual Poetics and Narrative",
                    "COMM 4460 - Visual Design Theory and Application",
                    "COMM 4970 - 2D Motion Graphics",
                    "COMM 4730 - Brand Identity Design",
                    "COMM 4690 - Interface Design Hypermedia Theory and Application",
                    "COMM 4880 - Interactive Data Visualization",
                    "WRIT 1110 - Writing in Context"'],
    NULL,
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"ARTS 1050 - Art History",
                    "orARTS 2540 - The Multimedia Century"'],
    ARRAY['"ARTS 1XXX",
                    "ARTS 1200 - Basic Drawing",
                    "ARTS 2200 - Intermediate Drawing",
                    "ARTS 2210 - Sculpture I",
                    "ARTS 2220 - Fundamentals of 2D Design",
                    "ARTS 4200 - Advanced Drawing",
                    "ARTS 4210 - Sculpture II",
                    "ARTS 4220 - Painting",
                    "ARTS 4260 - Life Drawing and Anatomy for Artists"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"COGS 2120 - Introduction to Cognitive Science"'],
    ARRAY['"PHIL 4960 – Ethics of AI",
                    "COGS 4960 - Learning and Advanced Game AI",
                    "PHIL 4961 - Intermediate Formal Logic & AI",
                    "IHSS 1972 - AI and Society",
                    "IHSS 1140 - Minds and Machines",
                    "IHSS 1235 - Are Humans Rational?",
                    "COGS 4210 - Cognitive Modeling",
                    "COGS 4410 - Programming for Cognitive Science and Artificial Intelligence",
                    "COGS 4420 - Game AI",
                    "COGS 4640 - Intelligent Virtual Agents",
                    "COGS 4880 - Language-Endowed Intelligent Agents"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following, with at least 4 credits at the 4000-level":', NULL],
    ARRAY['"PSYC 1200 - Introduction to Psychological Science"'],
    ARRAY['"IHSS 1960 – Understanding Empathy,",
                    "COGS 4330 - Introduction to Cognitive Neuroscience",
                    "COGS 4360 - Behavioral Neuroscience",
                    "COGS 4600 - Cognition and the Brain",
                    "COGS 4610 - Stress and the Brain",
                    "COGS 4700 - Hormones, Brain, and Behavior",
                    "PSYC 4330 - Introduction to Cognitive Neuroscience",
                    "PSYC 4360 - Behavioral Neuroscience",
                    "PSYC 4500 - Drugs, Society, and Behavior",
                    "PSYC 4600 - Cognition and the Brain",
                    "PSYC 4610 - Stress and the Brain",
                    "PSYC 4700 - Hormones, Brain, and Behavior"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"COGS 2120 - Introduction to Cognitive Science"'],
    ARRAY['"IHSS 1140 - Minds and Machines",
                    "IHSS 1235 - Are Humans Rational?",
                    "IHSS 1972 AI & Society",
                    "COGS 4330 - Introduction to Cognitive Neuroscience",
                    "COGS 4600 - Cognition and the Brain",
                    "PSYC 4350 - Mathematical Methods in Psychological Science",
                    "PSYC 4370 - Cognitive Psychology",
                    "PSYC 4410 - Sensation and Perception",
                    "PHIL 4961 - Intermediate Formal Logic & AI"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following, with at least 4 credits at the 4000 level":', NULL],
    ARRAY['"PSYC 1200 - Introduction to Psychological Science"'],
    ARRAY['"IHSS 19XX – Understanding Empathy",
                    "PSYC 2XXX",
                    "PSYC 4XXX",
                    "PSYC 2310 - Research Methods and Statistics I",
                    "PSYC 2730 - Social Psychology",
                    "PSYC 2800 - Introduction to Sports Psychology",
                    "PSYC 4110 - Motivation and Performance",
                    "PSYC 4200 - Industrial and Organizational Psychology",
                    "PSYC 4310 - Research Methods and Statistics II",
                    "PSYC 4350 - Mathematical Methods in Psychological Science",
                    "PSYC 4370 - Cognitive Psychology",
                    "PSYC 4400 - Personality",
                    "PSYC 4450 - Learning",
                    "PSYC 4500 - Drugs, Society, and Behavior",
                    "PSYC 4720 - Abnormal Psychology",
                    "PSYC 4740 - Psychology and The Law",
                    "PSYC 4750 - Forensic Psychology",
                    "PSYC 4800 - Sport Psychology Seminar"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following, with at least 4 credits at the 4000 level":', NULL],
    ARRAY['"IHSS 19XX – Understanding Empathy",
                    "ARTS 1200 - Basic Drawing",
                    "IHSS 1110 - Nature/Society",
                    "IHSS 1140 - Minds and Machines",
                    "IHSS 1175 - Well-being Cultivating Curiosity",
                    "IHSS 1180 - The Art of Listening",
                    "IHSS 1700 - Songwriting Workshop",
                    "IHSS 1720 - Music and Nature"'],
    ARRAY['"ARTS 2310 - Rensselaer Concert Choir Credit Hours 1 (course can be repeated multiple times for credit)",
                    "ARTS 2960 - Topics in the Arts Credit Hours 2 to 4(Private Lessons, Credit Hours 1)",
                    "COGS 4610 - Stress and the Brain",
                    "COGS 4700 - Hormones, Brain, and Behavior",
                    "PHIL 4240 - Ethics",
                    "PSYC 1200 - Introduction to Psychological Science",
                    "PSYC 4430 - Psychology of Mindfulness",
                    "PSYC 4440 - Sensibilities",
                    "PSYC 4500 - Drugs, Society, and Behavior",
                    "PSYC 4610 - Stress and the Brain",
                    "PSYC 4700 - Hormones, Brain, and Behavior",
                    "PSYC 4730 - Positive Psychology",
                    "PSYC 4960 - Topics in Psychology Credit Hours 1 to 4(Empathy and Emotion)",
                    "WRIT 2320 - Creative Writing Creative Non-Fiction",
                    "WRIT 2330 - Creative Writing The Short Story"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose 4 credits from the following":', '"Choose remaining credits from the following​​​​, with at least 4 credits at the 4000-level":'],
    ARRAY['"COGS 2340 - Introduction to Linguistics"'],
    ARRAY['"LANG 1XXX",
                    "LANG 2XXX"'],
    ARRAY['"LANG 4XXX",
                    "IHSS 1492 - Language and Culture",
                    "COGS 4340 - The Linguistics of Computational Linguistics",
                    "COGS 4560 - Cross-linguistic Perspectives",
                    "COGS 4780 - Advanced Topics in Linguistics",
                    "COGS 4880 - Language-Endowed Intelligent Agents"']
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1976 – Fiction from Film to the Internet IHSS 1964 - Documentary in the 21st Century  ARTS 1030 - Digital Filmmaking",
                    "IHSS 1160 - Science and Scientific Misconduct",
                    "IHSS 1300 - Race and Film in U.S. Culture and History",
                    "IHSS 1560 - Media and Society",
                    "PHIL 1110 - Introduction to Philosophy",
                    "IHSS 1550 - Fiction From Film to the Internet",
                    "IHSS 1776 - The American Dream Credit Hours"'],
    ARRAY['"ARTS 4040 - Rethinking Documentary Video Production",
                    "ARTS 4560 - Hactivism",
                    "ARTS 4640 - Science Fictions",
                    "COMM 2440 - Documentary Film",
                    "COMM 4530 - Reality TV and Post-Factual Media",
                    "COMM 4580 - Advertising and Culture",
                    "LITR 4150 - Science and Fiction",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 4130 - Philosophy of Science",
                    "PSYC 2100 - Critical Thinking",
                    "STSO 4430 - Drugs in History",
                    "STSO 4590 - American Politics in Crisis",
                    "WRIT 2320 - Creative Writing Creative Non-Fiction",
                    "WRIT 2330 - Creative Writing The Short Story"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, at least 4 credits at the 4000 level":', NULL, NULL],
    ARRAY['"LITR XXXX",
                    "WRIT 1XXX",
                    "WRIT 2XXX",
                    "IHSS 1550 - Fiction From Film to the Internet",
                    "IHSS 1776 - The American Dream Credit Hours",
                    "COMM 4320 - Visual Poetics and Narrative",
                    "COMM 4780 - Interactive Narrative",
                    "LITR 2110 - Introduction to Literature",
                    "LITR 2150 - Modern and Contemporary Literature",
                    "LITR 4150 - Science and Fiction",
                    "LITR 4230 - Irish Literature",
                    "LITR 4770 - Women Writers",
                    "WRIT 1110 - Writing in Context",
                    "WRIT 2320 - Creative Writing Creative Non-Fiction",
                    "WRIT 2330 - Creative Writing The Short Story"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, at least 4 credits at the 4000 level":', NULL, NULL],
    ARRAY['"COMM 1XXX",
                    "COMM 2XXX",
                    "IHSS 19XX – Writing and Society",
                    "WRIT 4XXX",
                    "COMM 2520 - Communication Theory and Practice",
                    "COMM 2660 - Introduction to Graphic Design",
                    "COMM 4580 - Advertising and Culture",
                    "IHSS 1492 - Language and Culture",
                    "IHSS 1560 - Media and Society",
                    "WRIT 1110 - Writing in Context",
                    "WRIT 2110 - Strategic Writing",
                    "WRIT 2340 - Speech Communication"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1960 – Music and Protest",
                    "IHSS 1960 – Designing Climate Justice",
                    "IHSS 1110 - Nature/Society",
                    "IHSS 1200 - Principles of Economics",
                    "IHSS 1240 - Sustainability Debates",
                    "IHSS 1320 - A Century of Environmental Thought",
                    "IHSS 1350 - Law, Values, and Public Policy Perspectives on Science and Technology",
                    "IHSS 1720 - Music and Nature",
                    "IHSS 1040 - Documentary in the 21st Century Identity Production"'],
    ARRAY['"ARTS 4250 - Art, Community, and Technology",
                    "ARTS 4240 - Eco Chic Living Art",
                    "ECON 4230 - Environmental Economics",
                    "PHIL 4300 - Environmental Philosophy",
                    "PHIL 4500 - Bioethics",
                    "STSO 4250 - Bioethics",
                    "STSO 4720 - Consumer Culture",
                    "STSO 4280 - Sustainability Education",
                    "ARTS 4120 - Biopunk Arts Lab Practice",
                    "ARTS 4140 - Queer Ecologies"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following must complete at least 4 credits at the 4000-level":', NULL],
    ARRAY['"STSO 2300 - Environment and Society"'],
    ARRAY['"IHSS 1960 - Designing Climate Justice",
                    "STSO 1110 - Science, Technology, and Society",
                    "IHSS 1110 - Nature/Society",
                    "IHSS 1320 - A Century of Environmental Thought",
                    "IHSS 1240 - Sustainability Debates",
                    "STSO 4300 - Sustainability and STS Sustainability Careers",
                    "STSO 4340 - Environmental Philosophy",
                    "STSO 4510 - History of American Technology",
                    "STSO 4720 - Consumer Culture",
                    "STSO 4260 - Food, Farms, and Famine",
                    "STSO 4280 - Sustainability Education",
                    "STSO 4350 - Politics of Design",
                    "STSO 4500 - Globalization and Development",
                    "STSO 4330 - Environmental Justice"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose other one of the following":', '"Choose remaining credits from":'],
    ARRAY['"ECON 1200 - Introductory Economics",
                    "IHSS 1200 - Principles of Economics"'],
    ARRAY['"ECON 2XXX",
                    "ECON 2010 - Intermediate Microeconomic Theory",
                    "ECON 2020 - Intermediate Macroeconomic Theory"'],
    ARRAY['"ECON 4XXX"']
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose one of the following":', NULL],
    ARRAY['"ECON 4130 - Money and Banking",
                    "ECON 4330 - Economics of Financial Institutions and Markets"'],
    ARRAY['"ECON 1200 - Introductory Economics",
                    "IHSS 1200 - Principles of Economics"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1200 - Principles of Economics",
                    "ECON 1200 - Introductory Economics"'],
    ARRAY['"ECON 4220 - Applied Game Theory",
                    "ECON 4270 - Behavioral Economics",
                    "ECON 4340 - Behavioral Financial Economics",
                    "ECON 4320 - Economic Models of Decision-Making",
                    "ECON 4360 - Experimental Economics"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1200 - Principles of Economics",
                    "ECON 1200 - Introductory Economics"'],
    ARRAY[' "ECON 4170 - Health Economics and Policy",
                    "ECON 4270 - Behavioral Economics",
                    "ECON 4290 - Economics of Biotech and Medical Innovations"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1200 - Principles of Economics",
                    "ECON 1200 - Introductory Economics"'],
    ARRAY['"ECON 4150 - Economics of Government Regulation and Firm Strategy",
                    "ECON 4170 - Health Economics and Policy",
                    "ECON 4310 - Law and Economics",
                    "ECON 4230 - Environmental Economics"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1200 - Principles of Economics",
                    "ECON 1200 - Introductory Economics"'],
    ARRAY['"ECON 4280 - Econometric Methods for Big Data",
                    "ECON 4570 - Econometrics",
                    "ECON 4360 - Experimental Economics"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1200 - Principles of Economics",
                    "ECON 1200 - Introductory Economics"'],
    ARRAY['"ECON 4110 - Economics of Innovation and New Technologies",
                    "ECON 4290 - Economics of Biotech and Medical Innovations",
                    "ECON 4430 - Economics of Growth & Innovation"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose One of the following":', '"Choose remaining credits from the following":'],
    ARRAY['"ITWS 2210 - Introduction to Human Computer Interaction"'],
    ARRAY['"IHSS 1220 - IT and Society",
                    "ITWS 1220 - IT and Society"'],
    ARRAY['"ARTS 2540 - The Multimedia Century",
                    "COGS 2120 - Introduction to Cognitive Science",
                    "COMM 2520 - Communication Theory and Practice",
                    "COMM 2660 - Introduction to Graphic Design",
                    "IHSS 1200 - Principles of Economics",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2140 - Introduction to Logic",
                    "PSYC 1200 - Introduction to Psychological Science",
                    "STSO 1110 - Science, Technology, and Society",
                    "STSO 2210 - Design, Culture, and Society",
                    "WRIT 2110 - Strategic Writing",
                    "WRIT 2340 - Speech Communication",
                    "COMM 4420 - Foundations of HCI Usability"']
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, with at least 4 credits at the 4000 level":', NULL, NULL],
    ARRAY['"IHSS 1560 - Media and Society",
                    "WRIT 1110 - Writing in Context",
                    "COMM 2520 - Communication Theory and Practice",
                    "COMM 2660 - Introduction to Graphic Design",
                    "COMM 4420 - Foundations of HCI Usability",
                    "COMM 4470 - Information Design",
                    "COMM 4690 - Interface Design Hypermedia Theory and Application",
                    "COMM 4780 - Interactive Narrative",
                    "COMM 4880 - Interactive Data Visualization"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose remaining credits from the following":', NULL, NULL],
    ARRAY['"IHSS 1140 - Minds and Machines",
                    "IHSS 1150 - The Genome and You",
                    "IHSS 1160 - Science and Scientific Misconduct",
                    "IHSS 1200 - Principles of Economics",
                    "ITWS 1220 - IT and Society",
                    "IHSS 1220 - IT and Society",
                    "COMM 4470 - Information Design",
                    "COMM 4690 - Interface Design Hypermedia Theory and Application",
                    "COMM 4880 - Interactive Data Visualization",
                    "ECON 4220 - Applied Game Theory",
                    "ECON 4270 - Behavioral Economics",
                    "ECON 4570 - Econometrics",
                    "PHIL 2100 - Critical Thinking",
                    "PSYC 2100 - Critical Thinking",
                    "PSYC 2310 - Research Methods and Statistics I",
                    "PSYC 4350 - Mathematical Methods in Psychological Science"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following":', NULL, NULL],
    ARRAY['"LANG 1410 - Chinese I",
                    "LANG 2410 - Chinese II",
                    "LANG 4420 - Chinese III",
                    "LANG 4430 - Chinese IV",
                    "LANG 4470 - Chinese V"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, with at least 8 credit hours at, or above, the 2000-level and at least 3 credit hours at the 4000-level":', NULL, NULL],
    ARRAY['"LANG 1XXX",
                    "LANG 2XXX",
                    "LANG 4XXX"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following":', NULL, NULL],
    ARRAY['"GSAS 1600 - History and Culture of Games",
                    "GSAS 2510 - Introduction to Game Design",
                    "GSAS 2520 - Introduction to Game Storytelling",
                    "GSAS 2540 - Introduction to Game Programming",
                    "GSAS 4520 - Game Development I",
                    "GSAS 4540 - Game Development II",
                    "GSAS 4510 - Experimental Game Design"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following, with at least 8 credit hours at, or above, the 2000-level and at least 3 credit hours at the 4000-level":', NULL, NULL],
    ARRAY['"IHSS 19XX – Remixing in Digital Culture",
                    "IHSS 19XX – Technology and the Top Ten",
                    "COMM 29XX - The Film Experience",
                    "IHSS 1030 - Behind the TV Screen",
                    "IHSS 1560 - Media and Society",
                    "IHSS 1776 - The American Dream Credit Hours",
                    "COMM 2410 - Perspectives on Photography",
                    "COMM 2440 - Documentary Film",
                    "COMM 2520 - Communication Theory and Practice",
                    "COMM 2616 - Superheroes in the Classroom",
                    "COMM 2750 - Critical Television",
                    "COMM 4530 - Reality TV and Post-Factual Media",
                    "COMM 4540 - Visual Culture",
                    "COMM 4550 - Religion in the Media",
                    "COMM 4580 - Advertising and Culture",
                    "ARTS 4040 - Rethinking Documentary Video Production"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 19XX – Remixing in Digital Culture",
                    "IHSS 19XX - Technology and the Top 10",
                    "IHSS 1010 - Exploring Music @Rensselaer",
                    "ARTS 2510 - Histories of Jazz and Improvised Music",
                    "IHSS 1700 - Songwriting Workshop",
                    "ARTS 2550 - Popular Music and Society"'],
    ARRAY['"ARTS 4960 - Performance Art",
                    "ARTS 2520 - World Music",
                    "ARTS 2700 - Sound Recording and Production I",
                    "ARTS 4700 - Sound Recording and Production II",
                    "ARTS 2500 - Histories of Western Music",
                    "ARTS 2180 - Deep Listening",
                    "ARTS 4180 - Topics in Deep Listening"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 19XX – Remixing in Digital Culture",
                    "IHSS 19XX – Technology and the Top Ten",
                    "ARTS 1380 - Fundamentals of Music and Sound",
                    "IHSS 1010 - Exploring Music @Rensselaer",
                    "ARTS 2510 - Histories of Jazz and Improvised Music",
                    "IHSS 1700 - Songwriting Workshop",
                    "ARTS 2550 - Popular Music and Society",
                    "ARTS 2500 - Histories of Western Music"'],
    ARRAY['"ARTS 2020 - Music and Technology I",
                    "ARTS 2380 - Music and Sound I",
                    "ARTS 2600 - Ensemble Nonlinear Credit Hours",
                    "1ARTS 2700 - Sound Recording and Production I",
                    "ARTS 4160 - Music and Technology II",
                    "ARTS 4380 - Music and Sound II",
                    "ARTS 4700 - Sound Recording and Production II"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 19XX – Remixing in Digital Culture",
                    "ARTS 1380 - Fundamentals of Music and Sound",
                    "IHSS 1010 - Exploring Music @Rensselaer",
                    "ARTS 2510 - Histories of Jazz and Improvised Music",
                    "ARTS 2550 - Popular Music and Society",
                    "ARTS 2500 - Histories of Western Music"'],
    ARRAY['"ARTS 2180 - Deep Listening",
                    "ARTS 2300 - Rensselaer Orchestra Credit Hours 1 (course can be repeated multiple times for credit)",
                    "ARTS 2310 - Rensselaer Concert Choir Credit Hours 1 (course can be repeated multiple times for credit)",
                    "ARTS 2350 - Chamber Music Ensemble Credit Hours 1 (course can be repeated multiple times for additional credit)",
                    "ARTS 2600 - Ensemble Nonlinear Credit Hours",
                    "ARTS 2960 - Topics in the Arts Credit Hours 2 to 4(Fusion Ensemble or Contemporary Improv Ensemble )",
                    "ARTS 4180 - Topics in Deep Listening",
                    "ARTS 2750 - Private Music Lessons Credit Hours 1 (course can be repeated multiple times for credit)"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following, with at least 4 credits at the 4000 level":', NULL],
    ARRAY['"IHSS 19XX – Remixing in Digital Culture",
                    "IHSS 19XX – Technology and the Top Ten",
                    "ARTS 1030 - Digital Filmmaking",
                    "IHSS 1300 - Race and Film in U.S. Culture and History",
                    "IHSS 1030 - Behind the TV Screen",
                    "IHSS 1180 - The Art of Listening",
                    "IHSS 1040 - Documentary in the 21st Century Identity Production"'],
    ARRAY['"ARTS 2010 - Intermediate Video",
                    "ARTS 2540 - The Multimedia Century",
                    "ARTS 4040 - Rethinking Documentary Video Production",
                    "ARTS 4250 - Art, Community, and Technology",
                    "ARTS 4130 - New Media Theory",
                    "ARTS 4240 - Eco Chic Living Art",
                    "ARTS 4560 - Hactivism",
                    "ARTS 4630 - Writing and Directing for Video",
                    "ARTS 4640 - Science Fictions",
                    "ARTS 4120 - Biopunk Arts Lab Practice",
                    "ARTS 4140 - Queer Ecologies",
                    "ARTS 4050 - Advanced Video Media Studio"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Select 12 credits from the following":', NULL, NULL],
    ARRAY['"IHSS 1140 - Minds and Machines",
                    "IHSS 1180 - The Art of Listening",
                    "IHSS 1200 - Principles of Economics",
                    "IHSS 1235 - Are Humans Rational?",
                    "IHSS 1570 - War and Technolog Past, Present, and Future",
                    "IHSS 1510 - War and Society",
                    "COGS 2120 - Introduction to Cognitive Science",
                    "COMM 2520 - Communication Theory and Practice",
                    "ECON 4220 - Applied Game Theory",
                    "ECON 4270 - Behavioral Economics",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2140 - Introduction to Logic",
                    "PSYC 2100 - Critical Thinking",
                    "PSYC 4370 - Cognitive Psychology",
                    "STSO 4530 - History of Science and Technology",
                    "WRIT 2340 - Speech Communication",
                    "WRIT 4550 - Proposing and Persuading",
                    "PHIL 4961 – Intermediate Formal Logic & AI"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from a choice of the following​​​​, with at least 4 credits at the 4000-level":', NULL, NULL],
    ARRAY['"IHSS 1140 - Minds and Machines",
                    "IHSS 1235 - Are Humans Rational?",
                    "PSYC 2100 - Critical Thinking",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2140 - Introduction to Logic",
                    "PHIL 4140 - Intermediate Logic",
                    "PHIL 4420 - Computability and Logic",
                    "PHIL 4960 – Inductive Logic",
                    "PHIL 4961 – Intermediate Formal Logic & AI"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following with at least 4 credits at the 4000-level":', NULL],
    ARRAY['"PHIL1000",
                    "IHSS 19XX Philosophy, Technology, and the Human Future",
                    "IHSS 1150 - The Genome and You",
                    "IHSS 1160 - Science and Scientific Misconduct",
                    "IHSS 1165 - Great Ideas in Philosophy",
                    "PHIL 1110 - Introduction to Philosophy",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2140 - Introduction to Logic",
                    "PSYC 2100 - Critical Thinking"'],
    ARRAY['"PHIL 2XXX",
                    "PHIL 4XXX",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2140 - Introduction to Logic",
                    "PHIL 2400 - Philosophy of Biology",
                    "PHIL 4130 - Philosophy of Science",
                    "PHIL 4240 - Ethics",
                    "PHIL 4300 - Environmental Philosophy",
                    "PHIL 4480 - Metaphysics and Consciousness",
                    "PSYC 2100 - Critical Thinking"'],
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following":', NULL, NULL],
    ARRAY['"IHSS 1160 - Science and Scientific Misconduct",
                    "IHSS 1175 - Well-being Cultivating Curiosity",
                    "IHSS 1570 - War and Technology Past, Present, and Future",
                    "STSO 1110 - Science, Technology, and Society",
                    "ARTS 4240 - Eco Chic Living Art",
                    "ARTS 4960 - Topics in the Arts Credit Hours 2 to 4(Bio-Punk) Arts Lab Practices)",
                    "COMM 2520 - Communication Theory and Practice",
                    "LITR 4150 - Science and Fiction",
                    "PHIL 2100 - Critical Thinking",
                    "PHIL 2400 - Philosophy of Biology",
                    "PHIL 4130 - Philosophy of Science",
                    "PSYC 2100 - Critical Thinking",
                    "STSO 4510 - History of American Technology",
                    "STSO 4530 - History of Science and Technology",
                    "STSO 4400 - Medicine, Culture, and Society",
                    "WRIT 2110 - Strategic Writing",
                    "WRIT 4410 - Research Writing",
                    "WRIT 4550 - Proposing and Persuading"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"ARTS 1050 - Art History",
                    "ARTS 2510 - Histories of Jazz and Improvised Music",
                    "IHSS 1170 - History of Animation",
                    "IHSS 1300 - Race and Film in U.S. Culture and History",
                    "IHSS 1700 - Songwriting Workshop"'],
    ARRAY['"ARTS 2540 - The Multimedia Century",
                    "ARTS 4130 - New Media Theory",
                    "ARTS 2500 - Histories of Western Music"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"IHSS 1610 - Design and Innovation Studio I",
                    "STSO 2610 - Design and Innovation Studio II"'],
    ARRAY['"ENGR 4610 - Design and Innovation Studio C",
                    "STSO 4605 - Design and Innovation Studio B",
                    "STSO 4610 - Design and Innovation  Studio C"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following":', NULL, NULL],
    ARRAY['"IHSS 1140 - Minds and Machines",
                    "IHSS 1150 - The Genome and You",
                    "IHSS 1160 - Science and Scientific Misconduct",
                    "IHSS 1350 - Law, Values, and Public Policy Perspectives on Science and Technology",
                    "STSO 1110 - Science, Technology, and Society",
                    "IHSS 1960 – Designing Climate Justice",
                    "ARTS 4250 - Art, Community, and Technology",
                    "ARTS 4240 - Eco Chic Living Art",
                    "ARTS 4560 - Hactivism",
                    "PHIL 4240 - Ethics",
                    "PHIL 4300 - Environmental Philosophy",
                    "PHIL 4500 - Bioethics",
                    "STSO 4210 - Engineering Ethics",
                    "STSO 4250 - Bioethics",
                    "STSO 4340 - Environmental Philosophy",
                    "STSO 4400 - Medicine, Culture, and Society"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits from the following":', '"Can select only one of the following to be applied to pathway":', NULL],
    ARRAY['"COMM 2440 - Documentary Film",
                    "COMM 4550 - Religion in the Media",
                    "LITR 4770 - Women Writers",
                    "STSO 2510 - Cultural Anthropology",
                    "STSO 2520 - Sociology",
                    "STSO 4560 - Gender, Science, and Technology",
                    "ARTS 4140 - Queer Ecologies",
                    "ARTS 2550 - Popular Music and Society"'],
    ARRAY['"IHSS 1968 – Songs of Identity",
                    "IHSS 19XX – Revolutions in Perspective",
                    "IHSS 19XX - Worlds on Display",
                    "IHSS 1150 - The Genome and You",
                    "IHSS 1300 - Race and Film in U.S. Culture and History",
                    "IHSS 1492 - Language and Culture",
                    "IHSS 1560 - Media and Society",
                    "IHSS 1666 - Religion in a Global World"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose remaining credits from the following":', NULL],
    ARRAY['"STSO 2500 - American History"'],
    ARRAY['"STSO 4000 – STS Elective IHSS 1960 - Revolutions in Perspective",
                    "STSO 1110 - Science, Technology, and Society",
                    "IHSS 1776 - The American Dream Credit Hours",
                    "IHSS 1570 - War and Technology Past, Present, and Future",
                    "IHSS 1320 - A Century of Environmental Thought",
                    "STSO 4420 - History of Medicine",
                    "STSO 4430 - Drugs in History",
                    "STSO 4440 - History of Mental Health",
                    "STSO 4510 - History of American Technology",
                    "STSO 4530 - History of Science and Technology",
                    "STSO 4720 - Consumer Culture"'],
    NULL
);

INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose one of the following":', '"Choose remaining credits from the following":'],
    ARRAY['"STSS 2700 - Law and Society"'],
    ARRAY['"IHSS 19XX – Revolutions in Comparative Perspective",
                    "IHSS 19XX – Sociology of Inequality",
                    "IHSS 1350 - Law, Values, and Public Policy: Perspectives on Science and Technology",
                    "IHSS 1500 - Human Rights in History",
                    "IHSS 1510 - War and Society",
                    "STSH 1110 - Science, Technology, and Society",
                    "STSS 1110 - Science, Technology, and Society"'],
    ARRAY['"STSH 4210 - Engineering Ethics",
                    "STSH 4310 - Energy Politics",
                    "STSH 4430 - Drugs in History",
                    "STSH 4520 - Social Demography: Society by the Numbers", 
                    "STSH 4700 - Environmental Law",
                    "STSH 4800 - Public Service and Social Justice",
                    "STSS 4310 - Energy Politics", 
                    "STSS 4320 - Resilience Planning", 
                    "STSS 4430 - Drugs in History", 
                    "STSS 4520 - Social Demography: Society by the Numbers", 
                    "STSS 4540 - China and the United States", 
                    "STSS 4560 - Gender, Science, and Technology", 
                    "STSS 4570 - Contemporary Political Thought", 
                    "STSS 4590 - American Politics in Crisis", 
                    "STSS 4800 - Public Service and Social Justice"']
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Required":', '"Choose one of the following":', '"Choose remaining credits from the following":'],
    ARRAY['"STSO 2520 - Sociology"'],
    ARRAY['"IHSS 1150 - The Genome and You",
                    "PSYC 1200 - Introduction to Psychological Science",
                    "STSO 1110 - Science, Technology, and Society"'],
    ARRAY['"COGS 4610 - Stress and the Brain",
                    "COGS 4700 - Hormones, Brain, and Behavior",
                    "PSYC 4500 - Drugs, Society, and Behavior",
                    "PSYC 4610 - Stress and the Brain",
                    "PSYC 4700 - Hormones, Brain, and Behavior",
                    "STSO 4420 - History of Medicine",
                    "STSO 4440 - History of Mental Health",
                    "STSO 4250 - Bioethics",
                    "STSO 4430 - Drugs in History",
                    "STSO 4260 - Food, Farms, and Famine",
                    "STSO 4400 - Medicine, Culture, and Society",
                    "STSO 4560 - Gender, Science, and Technology"']
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose one of the following a minimum of 4 credits must be completed at the 4000-level":', NULL, NULL],
    ARRAY['"STSO 4XXX",
                    "STSO 1110 - Science, Technology, and Society",
                    "ITWS 1220 - IT and Society",
                    "IHSS 1220 - IT and Society",
                    "STSO 2500 - American History",
                    "STSO 2300 - Environment and Society",
                    "STSO 2510 - Cultural Anthropology",
                    "STSO 2520 - Sociology"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits of the following course prefixes, with at least 8 credit hours at, or above, the 2000 level and at least 3 credit hours at the 4000 level":', NULL, NULL],
    ARRAY['"ARTS XXXX",
                    "COMM XXXX",
                    "GSAS XXXX",
                    "IHSS XXXX",
                    "LANG XXXX",
                    "LITR XXXX",
                    "PHIL XXXX",
                    "STSH XXXX",
                    "WRIT XXXX"'],
    NULL,
    NULL
);
INSERT INTO REQUIREMENTSFORPATH(chooses, classone, classtwo, classthree) VALUES (
    ARRAY['"Choose 12 credits of the following course prefixes, with at least 8 credit hours at, or above, the 2000 level and at least 3 credit hours at the 4000 level":', NULL, NULL],
    ARRAY['"COGS XXXX",
                    "ECON XXXX",
                    "GSAS XXXX",
                    "IHSS XXXX",
                    "PSYC XXXX",
                    "STSS XXXX"'],
    NULL,
    NULL
);


--  CODE TO MERGE THE TABLES INTO ONE

INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    1, 1, '"Arts / Designs"'
);

INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    2, 2, '"Arts / Designs"'
);

INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    3, 3, '"Arts / Designs"'
);

INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    4, 4, '"Arts / Designs"'
);

INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    5, 5, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    6, 6, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    7, 7, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    8, 8, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    9, 9, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    10, 10, '"Cognitive Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    11, 11, '"Communication/ Writing"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    12, 12, '"Communication/ Writing"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    13, 13, '"Communication/ Writing"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    14, 14, '"Ecology"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    15, 15, '"Ecology"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    16, 16, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    17, 17, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    18, 18, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    19, 19, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    20, 20, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    21, 21, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    22, 22, '"Economics"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    23, 23, '"Information Technology"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    24, 24, '"Information Technology"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    25, 25, '"Information Technology"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    26, 26, '"Language"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    27, 27, '"Language"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    28, 28, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    29, 29, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    30, 30, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    31, 31, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    32, 32, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    33, 33, '"Media / Music"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    34, 34, '"Philosophy"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    35, 35, '"Philosophy"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    36, 36, '"Philosophy"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    37, 37, '"Philosophy"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    38, 38, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    39, 39, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    40, 40, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    41, 41, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    42, 42, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    43, 43, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    44, 44, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    45, 45, '"Social Science"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    46, 46, '"Transfer Student"'
);
INSERT INTO COMBINE(require_id, pathway_id, majorName) VALUES (
    47, 47, '"Transfer Student"'
);

-- PRINTING ALL THE TABLES INDIVIDUALLY

SELECT * FROM PATHWAYNAME;
SELECT * FROM REQUIREMENTSFORPATH;
SELECT * FROM COMBINE;

-- JOINING THE TABLES

SELECT COMBINE.majorname, PATHWAYNAME.nameofpath, (requirementsforpath.chooses[1]), REQUIREMENTSFORPATH.classone, (requirementsforpath.chooses[2]), REQUIREMENTSFORPATH.classtwo, (requirementsforpath.chooses[3]), REQUIREMENTSFORPATH.classthree, PATHWAYNAME.compatibleminors
FROM COMBINE
JOIN PATHWAYNAME ON PATHWAYNAME.id = COMBINE.require_id
JOIN requirementsforpath ON REQUIREMENTSFORPATH.id = COMBINE.pathway_id
