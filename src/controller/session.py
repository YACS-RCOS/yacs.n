from common import *
from db.session import Session as SessionModel
from db.user import User as UserModel
from datetime import datetime
import view.message as msg

def deleteSession(form):
    if not checkKeys(form, ['sessionID']):
        return msg.errMsg("Please check your request body.")

    sessions = SessionModel()

    givenSessionID = form['sessionID']

    sessionFounded = sessions.getSession(sessionID=givenSessionID)

    if sessionFounded == None:
        return msg.errMsg("Failed to find given session")

    if len(sessionFounded) == 0:
        return msg.errMsg("Can't found the session.")

    if sessionFounded[0]['end_time'] != None:
        return msg.errMsg("This session already canceled.")

    endTime = datetime.utcnow()

    endSessionResult = sessions.endSession(sessionID=givenSessionID,endTime=endTime)
    if endSessionResult == None:
        return msg.errMsg("Failed to end this session.")

    return msg.successMsg({"sessionID":givenSessionID,"endTime": str(endTime)})


def addSession(form):
    if not checkKeys(form,['email','password']):
        return msg.errMsg("Please check the inputs.")

    sessions = SessionModel()
    users = UserModel()

    (email,password)=(form['email'],form['password'])

    usersFounded = users.getUser(email=email,password=encrypt(password),enable=True)
    if usersFounded == None:
        return msg.errMsg("Failed to validate user information.")

    if len(usersFounded) == 0:
        return  msg.errMsg("Invalid email address or password.")

    uid = usersFounded[0]['user_id']
    newSessionID = sessions.createSessionID()
    startTime = datetime.utcnow()

    startSessionResult = sessions.startSession(newSessionID, uid, startTime)

    if startSessionResult == None:
        return msg.errMsg("Failed to start a new session.")

    return msg.successMsg({"sessionID" : newSessionID, "uid" : uid, "startTime": str(startTime)})

