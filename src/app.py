#!/usr/bin/python3
from flask import Flask
from flask import send_from_directory
from flask import jsonify
from flask import Response
from flask import request
import db.connection as connection
import db.classinfo as ClassInfo

from CsvToInsert import CsvToInsert

from io import StringIO

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)


app = Flask(
    __name__,
    template_folder='./public/templates')


# - web routes break into routes/ ... later

@app.route('/', methods=['GET'])
def root():
    return send_from_directory('./public/templates/', 'schedule.html')


@app.route('/admin', methods=['GET'])
def admin():
    return send_from_directory('./public/templates/', 'admin.html')


@app.route('/css/<string:file>', methods=['GET'])
def css(file):
    return send_from_directory('./public/css/', file)


@app.route('/js/<string:file>', methods=['GET'])
def js(file):
    return send_from_directory('./public/js/', file)


# - data routes

@app.route('/api/class', methods=['GET'])
def get_classes():
    return jsonify(class_info.get_classes_full())

@app.route('/api/upload', methods=['POST'])
def uploadHandler():
    if len(request.files) > 0:
        files = []
        for _, file in request.files.items():
            if ('.' in file.filename and file.filename.rsplit('.')[1] == 'csv'):
                # Flask opens passed files from POST in binary mode by default
                content = file.read().decode()
                # https://stackoverflow.com/questions/3305926/python-csv-string-to-array
                tempFile = StringIO(content)
                files.append(tempFile)
            else:
                print("not csv file")
        print(files)
        csvToDBInsertJob = CsvToInsert(connection.db)
        csvToDBInsertJob.populateDBFromCSVDataSourceDirectoryPath(files)
    # for key, value in request.form.items():
    #     print(key, value)
    return Response("Received file(s)", 200)

if __name__ == '__main__':
    app.run()
