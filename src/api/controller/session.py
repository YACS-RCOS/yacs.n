from common import *
from db.session import Session as SessionModel
from db.user import User as UserModel
from datetime import datetime
import view.message as msg


async def delete_session(form):
    if not assert_keys_in_form_exist(form, ['sessionID']):
        return msg.error_msg("Please check your request body.")

    sessions = SessionModel()

    given_session_id = form['sessionID']

    session_founded = await sessions.get_session(session_id=given_session_id)

    if session_founded is None:
        return msg.error_msg("Failed to find given session")

    if len(session_founded) == 0:
        return msg.error_msg("Can't found the session.")

    if session_founded[0]['end_time'] is not None:
        return msg.error_msg("This session already canceled.")

    end_time = datetime.utcnow()

    res = await sessions.end_session(session_id=given_session_id, end_time=end_time)
    if res is None:
        return msg.error_msg("Failed to end this session.")

    return msg.success_msg({"sessionID": given_session_id, "endTime": str(end_time)})


async def add_session(form):
    if not assert_keys_in_form_exist(form, ['email', 'password']):
        return msg.error_msg("Please check the inputs.")

    sessions = SessionModel()
    users = UserModel()

    (email, password) = (form['email'], form['password'])

    users_founded = await users.get_user(email=email, password=encrypt(password), enable=True)
    if users_founded == None:
        return msg.error_msg("Failed to validate user information.")

    if len(users_founded) == 0:
        return msg.error_msg("Invalid email address or password.")

    uid = users_founded[0]['user_id']
    new_session_id = sessions.create_session_id()
    start_time = datetime.utcnow()

    res = await sessions.start_session(new_session_id, uid, start_time)

    if res == None:
        return msg.error_msg("Failed to start a new session.")

    return msg.success_msg({
        "sessionID": new_session_id, 
        "uid": uid, 
        "startTime": str(start_time),
        "userName" : users_founded[0]['name']
        })
