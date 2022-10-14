So in the file we may use three python files -> to_json_2022.py / html_parser.py / major_scrap.py
1: <html_parser.py>
The html_parser.py is used for read the "URL2022FallRaw.txt", which combined all the websites we need.
And then we use the html_parser.py to get the links for each of the websites. and store it in "majorURLlist2022FA.txt"
Also you can change the readfile name, in this way you can generate another txt file with all the valid links.

html_parser.py -> read -> "URL2022FallRaw.txt" -> write -> "majorURLlist2022FA.txt"

2: <major_scrap.py>
The major_scrap.py is used for read the "majorURLlist2022FA.txt" and then turn this file to a txt file that include all the 
info on the websites of every links. And the files that be generated are "majorData2022.txt" and "DBCCommandsN.txt".
outfile = "majorData2022.txt"
outfile2 = "DBCCommandsN.txt"

major_scrap.py -> read -> "majorURLlist2022FA.txt" -> write -> "majorData2022.txt" and "DBCCommandsN.txt"

3: <to_json_2022.py>
After we get the "majorData2022.txt", so we can just put the file in the to_json_2022.py and then we may get a json file that include all the 
data in the "majorData2022.txt".

to_json_2022.py -> read -> "majorData2022.txt" -> write -> majorData2022test.json