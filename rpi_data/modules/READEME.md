# Package requirements
pandas
bs4
requests
lxml
regex
pyyaml
selenium

# Course Parser
Hopefully this will be the last one.
There is one relevant file, new_parse.py
This file will do everything and produce a csv of the relevant semester.

# How to run

# Common issues

------------------------------------------------------------------------------------------------------------------------------------------
Sel | CRN | Maj | Cod | Sec | Cmp | Crd | Nme | Dys | Tme | Cap | Act | Rem | WLC | WLA | WLR | XLC | XLA | XLR | Prof | Date | Loc | Attr
------------------------------------------------------------------------------------------------------------------------------------------
SR  |99341|CSCI |1100 |01   | T   | 4.00| CSI | MR  |12-150| 24 | 3   | 21  | 0   | 0   | 0   | 0   | 0   | 0   |Stur  |01-04 |TBA  |Intro
------------------------------------------------------------------------------------------------------------------------------------------
While some details have been truncated to fit, this is an example of what we expect a course to be from sis. And for the most part, many courses on sis follow this format.
But, SIS is not perfect, and there are often many mistakes in courses.
The first main one (though this is moreso a design decision than a mistake) is that many parts of courses may be empty, for example
------------------------------------------------------------------------------------------------------------------------------------------
    |     |     |     |     |     |     |     | T  |10-1150|   |     |    |     |     |     |     |     |     |TBA  |01-04 |TBA  |Intro
------------------------------------------------------------------------------------------------------------------------------------------
This is the lab block for the above cs1 course. As you may notice, most of the details are missing, and so it is impossible to build out a course just from this information. 
However, since this appears directly below the cs1 lecture block in sis, we will parse this course immedieatly after parsing the lecture block.
So, we keep a copy of the previous course that we parsed, and use that to fill in information about lab and test blocks.

Another common issue is the use of colspan, for example, Biomed 6940 in spring 2024, which looks like this in SIS
------------------------------------------------------------------------------------------------------------------------------------------
SR  |90453|BMED |6940 |01   | T   | 1-9 | REB | TBA  |     | 0 | 0   | 0  | 0   | 0   | 0   | 0   | 0   | 0   |TBA  |01-04 |TBA  |
------------------------------------------------------------------------------------------------------------------------------------------
However, is parsed as 
------------------------------------------------------------------------------------------------------------------------------------------
SR  |90453|BMED |6940 |01   | T   | 1-9 | REB | TBA       | 0 | 0   | 0  | 0   | 0   | 0   | 0   | 0   | 0   |TBA  |01-04 |TBA  |
-----------------------------------------------------------------------------------------------------------------------------------------
because of the use of colspan in the days column. This means that our indecies are off when we start formatting and processing stuff, which crashes the web scraper. We get around this by inserting a TBA for the value of the colspan that we see.

These are the two most common offenders, but other issues can pop up, so generally, a row should always have exactly 21 things in it before we begin processing. Many issues that pop up with the webscraper are related to the rows not having a length of 21.