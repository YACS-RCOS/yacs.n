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
import controller.user as user_controller
import controller.session as session_controller
import controller.userevent as event_controller
from io import StringIO
import json

from flask_cors import CORS

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn)

app = Flask(
    __name__,
    template_folder='./public/templates')
CORS(app)


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


@app.route('/api/department', methods=['GET'])
def get_departments():
    return jsonify(class_info.get_departments())


@app.route('/api/subsemester', methods=['GET'])
def get_subsemesters():
    return jsonify(class_info.get_subsemesters())


@app.route('/api/courses', methods=['POST'])
def uploadHandler():
    # check for user files
    if not len(request.files):
        return Response("Need a *.csv file", 400)
    # get file
    csv_file = StringIO(request.files['file'].read().decode())
    courses.populate_from_csv(csv_file)
    # redirect back to home
    return redirect(url_for('root'))


# - user system api
@app.route('/user', methods=['GET'])
def getUserInfo():
    return user_controller.getUserInfo(request.json)


@app.route('/user', methods=['POST'])
def addUser():
    return user_controller.addUser(request.json)


@app.route('/user', methods=['DELETE'])
def deleteUser():
    return user_controller.deleteUser(request.json)


@app.route('/user', methods=['PUT'])
def updateUserInfo():
    return user_controller.updateUser(request.json)


@app.route('/session', methods=['POST'])
def login():
    return session_controller.addSession(request.json)


@app.route('/session', methods=['DELETE'])
def logout():
    return session_controller.deleteSession(request.json)


@app.route('/event', methods=['POST'])
def addUserEvent():
    return event_controller.addEvent(json.loads(request.data))


if __name__ == '__main__':
    app.run()
