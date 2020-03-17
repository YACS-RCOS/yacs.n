#!/usr/bin/python3
from flask import Flask
from flask import send_from_directory
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
import db.connection as connection
import db.classinfo as ClassInfo
import db.courses as Courses
from io import StringIO

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn)

app = Flask(
    __name__,
    template_folder='./public/templates')


# - web routes break into routes/ ... later

# @app.route('/', methods=['GET'])
# def root():
#     return send_from_directory('./public/templates/', 'schedule.html')


# @app.route('/admin', methods=['GET'])
# def admin():
#     return send_from_directory('./public/templates/', 'admin.html')


# @app.route('/css/<string:file>', methods=['GET'])
# def css(file):
#     return send_from_directory('./public/css/', file)


@app.route('/js/<string:file>', methods=['GET'])
def js(file):
    return send_from_directory('./public/js/', file)


# - data routes

@app.route('/api/class', methods=['GET'])
def get_classes():
    return jsonify(class_info.get_classes_full())


@app.route('/api/department', methods=['GET'])
def get_departments():
    return jsonify(class_info.get_departments())


@app.route('/api/subsemester', methods=['GET'])
def get_subsemesters():
    return jsonify(class_info.get_subsemesters())

@app.route('/api/semester', methods=['GET'])
def get_semesters():
    return jsonify(class_info.get_semesters())

@app.route('/api/bulkCourseUpload', methods=['POST'])
def uploadHandler():
    # check for user files
    if not len(request.files):
        return Response("Need a *.csv file", 400)
    # get file
    csv_file = StringIO(request.files['file'].read().decode())
    isSuccess, error = courses.populate_from_csv(csv_file)
    if (isSuccess):
        return Response(status=200)
    else:
        print(error)
        return Response(error.__str__(), status=500)



if __name__ == '__main__':
    app.run()
