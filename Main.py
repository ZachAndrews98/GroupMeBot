"""
    GroupMe Bot
    # Created by Zachary Andrews
    # Github: ZachAndrews98

    Creates a bot that can be run from the terminal for the GroupMe app. Uses
    Groupy to interface with GroupMe's API, can post and read messages from the
    terminal. Will analyze any message using the '@' symbol and the name of the
    bot in the group. The bot can currently tell the time, weather, and create
    and keep track of events as well as reminders. Currently cannot create a bot
    through this, so in order to use you must create a bot via GroupMe's
    Developer site.
"""
# nonlocal imports
from groupy import session
from groupy.api import bots
from groupy.api import messages
from groupy.api.attachments import Mentions
from groupy.api import groups
import datetime

# local imports
import KEYS
import Weather
import Log
import Event_List
import Reminders
import Analyze
import Main
# creates new session (uses api key from groupme), needed for all objects
s = session.Session(KEYS.GROUPME_API_KEY)
# create the bot manager
manager = bots.Bots(s)
# creates the message utility
mess = messages.Messages(s,KEYS.GROUP_ID)
# creates the weather utility
weather = Weather.weather('Meadville, PA, US')
# stores the bot, assuming only 1 bot to keep track of, if more bots just add more
# variables and increment the index
# also assumes a bot has already been made through groupme developer website
BOT = manager.list()[0]
# stores the ids of the most recently analyzed/read message
NEWEST_MESSAGE_READ_ID = None
NEWEST_MESSAGE_ANALYZED_ID = None
# constants for the time interval to check events
CHECK_TIME = datetime.datetime.now().replace(hour=8, minute=33, second=0, microsecond=0)
CHECK_TIME_END = datetime.datetime.now().replace(hour=8, minute=33, second=1, microsecond=0)
# stores each event that is coming up
event_list = Event_List.event_list()
# flag to determine if the events have been checked yet
checked_events = False
# stores reminders
reminder_list = Reminders.reminder_list()
# possible commands for the terminal and the bot
commands = ['read','post','cancel','shutdown','help']
bot_commands = ['help','time','weather','list events','create event','delete event']

if __name__ == '__main__':
    Log.log_debug(str(datetime.datetime.now())+" >> System Started")
    Main.check_date()
    Main.run()
    # g = groups.Groups(Main.s)
    # manager = g.get(KEYS.GROUP_ID)
    # t = manager.members
    # Main.post_message('@Zachary Andrews')
    # Mentions(loci = [0,15], user_ids=[40352095])
    #Main.post_message(manager)
    #Main.post_message(str(manager))

def run():
    try:
        while True:
            # checks if there are any new messages
            if mess.list_after(Main.NEWEST_MESSAGE_ANALYZED_ID) is not None:
                current_message = mess.list()[0] # newest message
                Analyze.analyze_message(current_message) # analyzes the message
                Main.NEWEST_MESSAGE_ANALYZED_ID = current_message.id # sets the new analyzed id
            if not Main.checked_events and datetime.datetime.now() > CHECK_TIME and \
                            datetime.datetime.now() < CHECK_TIME_END:
                check_date() # checks if any events have passed
    # enters terminal command mode
    except KeyboardInterrupt:
        Log.log_debug(str(datetime.datetime.now())+" >> KeyboardInterrupt")
        command = str(input("Would you like to do?\n")).lower()
        # reads the chats that have not been read yet
        if command == 'read':
            Log.log_debug(str(datetime.datetime.now())+" >> Messages Read")
            if mess.list_after(Main.NEWEST_MESSAGE_READ_ID) is not None:
                for m in mess.list_after(Main.NEWEST_MESSAGE_READ_ID):
                    print(m.name+': '+m.text)
                Main.NEWEST_MESSAGE_READ_ID = mess.list()[0].id
        # post into the group as the bot
        elif command == 'post':
            message = str(input('What would you like to say? (type "cancel" to cancel message)\n'))
            if message.lower() == 'cancel':
                run()
            Log.log_debug(str(datetime.datetime.now())+" >> Manual Posting: "+message)
            post_message(message)
        # get help information
        elif command == 'create event':
            name = str(input('Enter the name of the event\n'))
            date = str(input('Enter the date of the event\n')).split('/')
            desc = str(input('Enter the description of the event\n'))
            response = Main.create_event(name,int(date[2]),int(date[1]),int(date[0]),desc)
            print(response)
        elif command == 'list events':
            response = Main.list_events()
            print(response)
        elif command == 'delete event':
            name = str(input('Enter the name of the event\n'))
            Main.delete_event(name)
            print("Event Deleted")
        elif command == 'create reminder':
            day = str(input('Enter the day for the reminder\n'))
            id = str(input('Enter the name of the reminder\n'))
            desc = str(input('Enter the description of the event\n'))
            response = Main.create_reminder(day, id, desc)
            print(response)
        elif command == 'list reminders':
            response = Main.list_reminders()
            print(response)
        elif command == 'delete reminder':
            name = str(input('Enter the name of the reminder\n'))
            Main.delete_reminder(name)
        elif command == 'help':
            Log.log_debug(str(datetime.datetime.now())+" >> Help")
            print("Possible Commands:")
            for command in commands:
                print("\t"+command)
        # shutdown the system
        elif command == 'shutdown':
            Log.log_debug(str(datetime.datetime.now())+" >> System Shutdown")
            exit()
        # cancel command mode
        elif command == 'cancel':
            pass
        Log.log_debug(str(datetime.datetime.now())+" >> Continuing operation")
        run()

def check_date():
    # if the time matches the threshold, check what the events for the day are, posts them
    Main.event_list.delete_event_before_date(datetime.date.today() - datetime.timedelta(1))
    events = Main.event_list.get_events_by_date(datetime.date.today())
    response = "Today's events: "
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event)
    else:
        response += 'None'
    reminders = Main.reminder_list.get_reminders_by_day(datetime.datetime.today().weekday())
    response += "\nToday's reminders: "
    if len(reminders) != 0:
        for reminder in reminders:
            response += '-- '+ str(reminder) + '\n'
    else:
        response += 'None'
    post_message(response)
    Main.checked_events = True
    #checks if any events have expired
    if Main.checked_events and datetime.datetime.now() > CHECK_TIME_END:
        Main.checked_events = False

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

def create_event(name, year, month, day, desc):
    # creates a new event and adds it to the list
    Main.event_list.add_event(Event_List.event(name,datetime.date(year, day, month),desc))
    response = 'Okay, I made an event: '+str(Main.event_list.get_event(name))
    return response

def create_reminder(day, id, desc):
    Main.reminder_list.add_reminder(Reminders.reminder(day, id, desc))
    response = 'Okay I have created a reminder: '+str(Main.reminder_list.get_reminder(id))
    return response

def list_reminders():
    response = 'Reminders: \n'
    reminders = Main.reminder_list.get_reminders()
    if len(reminders) != 0:
        for reminder in reminders:
            response += '-- '+ str(reminder)+'\n'
    else:
        response += 'None'
    return response

def delete_event(name):
    if Main.event_list.delete_event(name.strip()):
        response = 'Okay I have removed the event'
    else:
        response = 'That reminder does not exist'

def delete_reminder(name):
    if Main.reminder_list.delete_reminder(name.strip()):
        response = 'Okay I have removed the reminder'
    else:
        response = 'That reminder does not exist'

# posts message into group
def post_message(message):
    manager.post(str(BOT.bot_id),str(message))

# childish easter eggs cause I am a child
def check_easter_egg(text):
    if datetime.datetime.now().time == datetime.time(16,4):
        post_message("Error 4:04, command not found")
        return True
    if "69" in text:
        post_message("HA, nice")
        return True
