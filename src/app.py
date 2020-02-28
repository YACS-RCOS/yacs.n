#!/usr/bin/python3
from flask import Flask
from flask import send_from_directory
from flask import jsonify
import db.connection as connection
import db.classinfo as ClassInfo

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


if __name__ == '__main__':
    app.run()
