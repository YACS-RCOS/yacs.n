from subprocess import call

call(["python", "html_parser.py"])
call(["python", "major_scrap.py"])
call(["python", "to_json_2022.py"])
 
call(["python", "ienv.py"])
call(["python", "psysci.py"])
call(["python", "chembio.py"])
call(["python", "engcocu.py"])

fout = open("jsons/majorData.json", "w", encoding='UTF-8')
fmain = open("jsons/majorDataTest.json", "r", encoding='UTF-8')
lines = fmain.readlines()
for line in lines:
    print(line)
    fout.write(line)

jsons = ["ienv","psysci","chembio","engcocu"]
for json in jsons:
    fjson = open("jsons/"+json+".json", "r", encoding='UTF-8')
    lines = fjson.readlines()
    for line in lines:
        fout.write(line)
        fout.write(",\n")
        
fout.write('\n]')