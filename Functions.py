# Created by Zachary Andrews
# Github: ZachAndrews98
import Main
import datetime
# checks to see if there are any events or reminders for the day and deletes old events
def check_date():
    # if the time matches the threshold, check what the events for the day are, posts them
    Main.event_list.delete_event_before_date(datetime.date.today() - datetime.timedelta(1))
    events = Main.event_list.get_events_by_date(datetime.date.today())
    response = "Today's events:\n"
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event)
    else:
        response += 'None'
    reminders = Main.reminder_list.get_reminders_by_day(datetime.datetime.today().weekday())
    response += "\nToday's reminders:\n"
    if len(reminders) != 0:
        for reminder in reminders:
            response += '-- '+ str(reminder) + '\n'
    else:
        response += 'None'
    post_message(response)
    Main.checked_events = True
    #checks if any events have expired
    if Main.checked_events and datetime.datetime.now() > Main.CHECK_TIME_END:
        Main.checked_events = False

# creates output for current and future events
def list_events():
    response = 'Events Today:\n'
    events = Main.event_list.get_events_by_date(datetime.date.today())
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event) + '\n'
    else:
        response += 'None'
    response += '\nEvents: \n'
    events = Main.event_list.get_event_list()
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event)
    else:
        response += 'None'
    return response

# creates a new event and adds it to the list
def create_event(name, year, month, day, desc):
    Main.event_list.add_event(Event_List.event(name,datetime.date(year, day, month),desc))
    response = 'Okay, I made an event: '+str(Main.event_list.get_event(name))
    return response

# creates a new reminder and adds it to the list
def create_reminder(day, id, desc):
    Main.reminder_list.add_reminder(Reminders.reminder(day, id, desc))
    response = 'Okay I have created a reminder: '+str(Main.reminder_list.get_reminder(id))
    return response

# creates the output for current and future reminders
def list_reminders():
    response = 'Reminders: \n'
    reminders = Main.reminder_list.get_reminders()
    if len(reminders) != 0:
        for reminder in reminders:
            response += '-- '+ str(reminder)+'\n'
    else:
        response += 'None'
    return response

# deletes event
def delete_event(name):
    if Main.event_list.delete_event(name.strip()):
        response = 'Okay I have removed the event'
    else:
        response = 'That reminder does not exist'

# deletes reminder
def delete_reminder(name):
    if Main.reminder_list.delete_reminder(name.strip()):
        response = 'Okay I have removed the reminder'
    else:
        response = 'That reminder does not exist'

# posts message into group
def post_message(message):
    Main.manager.post(str(Main.BOT.bot_id),str(message))

# childish easter eggs cause I am a child
def check_easter_egg(text):
    time = datetime.datetime.now().time
    if time == datetime.time(4,4) or time == datetime.time(16,4):
        post_message("Error 4:04, command not found")
        return True
    if time == datetime.time(4,20) or time == datetime.time(16,20):
        post_message("Blaze it")
        return True
    if "69" in text:
        post_message("HA, nice")
        return True