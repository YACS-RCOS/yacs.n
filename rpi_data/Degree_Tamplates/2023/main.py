from subprocess import call

# call main parser, main scraper, main to_json function
call(["python", "html_parser.py"])
call(["python", "major_scrap.py"])
call(["python", "to_json_2022.py"])

# call edge cases functions
jsons = ["ienv","psysci","chembio","engcocu","gamesimu","mechengcu"]
for edgecase in jsons:
    call(["python", edgecase+".py"])
    
# main json
fout = open("jsons/majorData.json", "w", encoding='UTF-8')
fmain = open("jsons/majorDataTemp.json", "r", encoding='UTF-8')
lines = fmain.readlines()
for line in lines:
    print(line)
    fout.write(line)
    
# edge cases json added
for i in range(len(jsons)):
    fjson = open("jsons/"+jsons[i]+".json", "r", encoding='UTF-8')
    lines = fjson.readlines()
    for line in lines:
        fout.write(line)
        if(i == len(jsons)-1):
            break
        fout.write(",\n")
        
fout.write('\n]')