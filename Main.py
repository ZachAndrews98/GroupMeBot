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
import Log
import Event_List
import Reminders
import Analyze
import Main
import Functions
# creates new session (uses api key from groupme), needed for all objects
s = session.Session(KEYS.GROUPME_API_KEY)
# create the bot manager
manager = bots.Bots(s)
# creates the message utility
mess = messages.Messages(s,KEYS.GROUP_ID)
# stores the bot, assuming only 1 bot to keep track of, if more bots just add more
# variables and increment the index
# also assumes a bot has already been made through groupme developer website
try:
    BOT = manager.list()[0]
except:
    print("No bot present, creating bot")
    bot_name = str(input("What would you like to name the bot?\n"))
    BOT = manager.create(bot_name,KEYS.GROUP_ID)
# stores the ids of the most recently analyzed/read message
NEWEST_MESSAGE_READ_ID = None
NEWEST_MESSAGE_ANALYZED_ID = None
# constants for the time interval to check events
CHECK_TIME = datetime.datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
CHECK_TIME_END = datetime.datetime.now().replace(hour=8, minute=30, second=1, microsecond=0)
# stores each event that is coming up
event_list = Event_List.event_list()
# flag to determine if the events have been checked yet
checked_events = False
# stores reminders
reminder_list = Reminders.reminder_list()
# possible commands for the terminal and the bot
commands = ['help','time','weather','list events','create event',
                'delete event','list reminders','create reminder','delete reminder']

if __name__ == '__main__':
    Log.log_debug(str(datetime.datetime.now())+" >> System Started")
    Main.event_list.check_for_events()
    Main.reminder_list.check_for_reminders()
    Functions.check_date()
    Main.run()

def run():
    try:
        while True:
            # checks if there are any new messages
            if mess.list_after(Main.NEWEST_MESSAGE_ANALYZED_ID) is not None:
                current_message = mess.list()[0] # newest message
                text = current_message.text.lower()
                name = current_message.name
                at_bot = '@'+Main.BOT.name
                # checks if the bot is mentioned
                if at_bot.lower() in text:
                    Analyze.analyze_message(text,name) # analyzes the message
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
            Functions.post_message(message)
        # get help information
        elif command == 'create event':
            date = str(input('Enter the date of the event\n')).split('/')
            name = str(input('Enter the name of the event\n'))
            desc = str(input('Enter the description of the event\n'))
            if len(date[2]) != 4:
                date[2] = '20'+date[2]
            response = Functions.create_event(name,int(date[2]),int(date[1]),int(date[0]),desc)
            print(response)
        elif command == 'list events':
            response = Functions.list_events()
            print(response)
        elif command == 'delete event':
            name = str(input('Enter the name of the event\n'))
            Functions.delete_event(name)
            print("Event Deleted")
        elif command == 'create reminder':
            day = str(input('Enter the day for the reminder\n'))
            id = str(input('Enter the name of the reminder\n'))
            desc = str(input('Enter the description of the event\n'))
            response = Functions.create_reminder(day, id, desc)
            print(response)
        elif command == 'list reminders':
            response = Functions.list_reminders()
            print(response)
        elif command == 'delete reminder':
            name = str(input('Enter the name of the reminder\n'))
            Functions.delete_reminder(name)
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
