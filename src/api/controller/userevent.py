from db.userevent import UserEvent as UserEvents
import view.message as msg
from common import *


def add_event(form):
    user_events = UserEvents()

    if not assert_keys_in_form_exist(form, ['uid', 'eventID', 'data', 'createdAt']):
        return msg.error_msg("Invalid request body.")


    uid = form['uid']
    event_id = form['eventID']
    event_data = form['data']
    timestamp = form['createdAt']

    res = user_events.add_event(uid=uid,event_id=event_id,data=str(event_data),timestamp=timestamp)

    if res is None:
        return msg.error_msg("Failed to add event.")

    return msg.success_msg({"msg": "Event added successfully."})
