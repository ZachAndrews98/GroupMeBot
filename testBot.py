"""
    GroupMe Bot Version: 0.2.1
    # Created by Zachary Andrews
    # Github: ZachAndrews98

    Creats a bot that can be run from the terminal for the GroupMe app. Uses
    Groupy to interface with GroupMe's API, can post and read messages from the
    terminal. Will analyze any message using the '@' symbol and the name of the
    bot in the group. The bot can currently tell the time, weather, and create
    and keep track of events as well as reminders.
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
import testBot
# creates new session (uses api key from groupme), needed for all objects
s = session.Session(KEYS.GROUPME_API_KEY)
# create the bot
test = bots.Bots(s)
# creates the message utility
mess = messages.Messages(s,KEYS.GROUP_ID)
# creates the weather utility
weather = Weather.weather('Meadville, PA, US')
# stores the bot, assuming only 1 bot to keep track of, if more bots just add more
# variables and increment the index
BOT = test.list()[0]
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
    #Log.log_debug(str(datetime.datetime.now())+" >> System Started")
    #testBot.run()
    g = groups.Groups(testBot.s)
    test = g.get(KEYS.GROUP_ID)
    t = test.members
    testBot.post_message('@Zachary Andrews')
    Mentions(loci = [0,15], user_ids=[40352095])
    #testBot.post_message(test)
    #testBot.post_message(str(test))

def run():
    try:
        while True:
            # checks if there are any new messages
            if mess.list_after(testBot.NEWEST_MESSAGE_ANALYZED_ID) is not None:
                current_message = mess.list()[0] # newest message
                analyze_message(current_message) # analyzes the message
                testBot.NEWEST_MESSAGE_ANALYZED_ID = current_message.id # sets the new analyzed id
            check_date() # checks if any events have passed
    # enters terminal command mode
    except KeyboardInterrupt:
        Log.log_debug(str(datetime.datetime.now())+" >> KeyboardInterrupt")
        command = str(input("Would you like to do?\n")).lower()
        # reads the chats that have not been read yet
        if command == 'read':
            Log.log_debug(str(datetime.datetime.now())+" >> Messages Read")
            if mess.list_after(testBot.NEWEST_MESSAGE_READ_ID) is not None:
                for m in mess.list_after(testBot.NEWEST_MESSAGE_READ_ID):
                    print(m.name+': '+m.text)
                testBot.NEWEST_MESSAGE_READ_ID = mess.list()[0].id
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
            response = testBot.create_event(name,int(date[2]),int(date[0]),int(date[1]),desc)
            testBot.post_message(response)
        elif command == 'list events':
            response = testBot.list_events()
            testBot.post_message(response)
        # elif command == 'delete event':
        #     name = str(input('Enter the name of the event\n'))
        #     testBot.delete_event(name)
        elif command == 'create reminder':
            day = str(input('Enter the day for the reminder\n'))
            id = str(input('Enter the name of the reminder\n'))
            desc = str(input('Enter the description of the event\n'))
            response = testBot.create_reminder(day, id, desc)
            testBot.post_message(response)
        elif command == 'list reminders':
            response = testBot.list_reminders()
            testBot.post_message(response)
        # elif command == 'delete reminder':
        #     name = str(input('Enter the name of the reminder\n'))
        #     testBot.delete_reminder(name)
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

# analyzes messages directed at the bot
def analyze_message(message):
    response = ''
    text = message.text.lower()
    at_bot = '@'+BOT.name
    # checks if the bot is mentioned
    if at_bot.lower() in text:
        Log.log_info(str(datetime.datetime.now())+" >> "+message.name+": "+message.text)
        if check_easter_egg(text):
            return
        if len(text) == len(at_bot):
            response = 'Hi, @'+str(message.name)+' what would you like?'
        # if the message mentions info
        elif 'info' in text:
            if 'time' in text:
                response = 'Time: Displays the current time, VERY redundant, but its included just cause'
            elif 'weather' in text:
                response = 'Weather: Displays the current weather in Meadville, PA, also kinda redundant,' +\
                            'but still included'
            elif 'list events' in text:
                response = 'List Events: Lists all events that are coming up'
            elif 'create event' in text:
                response = 'Create Event: Creates an event, should be formatted as such- ' +\
                'create event: <date>(m/d/y), <event name>, <event description>'
            elif 'delete event' in text:
                response = 'Delete Event: Delete an event, the name of the event should be right'+\
                            'after the command'
            elif 'help' in text:
                response = 'Help: Displays possible commands'
            else:
                response = 'That is not a possible command'
        # if the message mentions time
        elif 'time' in text:
            response = 'The time is currently: '+str(datetime.datetime.now().time())
        # if the message mentions weather
        elif 'weather' in text:
            response = 'The weather is currently: '+weather.get_current_weather()
        # if the message mentions events
        elif 'event' in text:
            # checks if list command
            if 'list' in text:
                response = testBot.list_events()
            # checks if the event command is properly formatted
            elif ':' not in text:
                response = "Make sure you include a ':' after the name of the command and try again"
            # checks if create command
            elif 'create' in text:
                info = text.split(':')[1].split(',')
                date = info[0].split('/')
                date[2] = '20'+date[2]
                # breaks up message into segments for parsing
                name = str(info[1]).strip()
                year = int(date[2])
                month = int(date[0])
                day = int(date[1])
                desc = info[2].strip()
                response = testBot.create_event(name,year,month,day,desc)
            # checks if delete command
            elif 'delete' in text:
                text = text.split(':')
                testBot.event_list.delete_event(text[1].strip())
                response = 'Okay I have removed the event'
            else:
                response = "I'm sorry, I don't believe that is one of the options"
        elif 'reminder' in text:
            response = ''
            if 'list' in text:
                response = testBot.list_reminders()
            elif ':' not in text:
                response = "Make sure you include a ':' after the name of the command and try again"
            elif 'create' in text:
                info = text.split(':')[1].split(',')
                day = info[0].strip()
                id = info[1].strip()
                desc = info[2].strip()
                response = testBot.create_reminder(day, id, desc)
            elif 'delete' in text:
                text = text.split(':')
                if testBot.reminder_list.delete_reminder(text[1].strip()):
                    response = 'Okay I have removed the reminder'
                else:
                    response = 'That reminder does not exist'
            else:
                response = "I'm sorry, I don't believe that is one of the options"
        elif 'help' in text:
            response = 'Heres a list of my commands:\n'+str(testBot.bot_commands)+\
                        '\nUse "Info" <command> for more info on the command'
        else:
            response = "I'm sorry @"+message.name+", I don't understand"
        # posts the response in the group
        post_message(response)
        Log.log_info((str(datetime.datetime.now())+" >> "+BOT.name+": "+response))

def check_date():
    # if the time matches the threshold, check what the events for the day are, posts them
    if not testBot.checked_events and datetime.datetime.now() > CHECK_TIME and \
                    datetime.datetime.now() < CHECK_TIME_END:
        events = testBot.event_list.get_event_list()
        for event in events:
            if event.date < datetime.date.today():
                Log.log_debug((str(datetime.datetime.now())+" >> deleted: "+str(event)))
                testBot.event_list.delete_event(event.name)

        events = testBot.event_list.get_events_by_date(datetime.date.today())
        response = "Today's events: "
        if len(events) != 0:
            for event in events:
                response += '-- '+ str(event)
        else:
            response += 'None'
        reminders = testBot.reminder_list.get_reminders_by_day(datetime.datetime.today().weekday())
        response += "\nToday's reminders: "
        if len(reminders) != 0:
            for reminder in reminders:
                response += '-- '+ str(reminder) + '\n'
        else:
            response += 'None'
        post_message(response)
        testBot.checked_events = True
    #checks if any events have expired
    if testBot.checked_events and datetime.datetime.now() > CHECK_TIME_END:
        testBot.checked_events = False

def list_events():
    response = 'Events Today:\n'
    events = testBot.event_list.get_events_by_date(datetime.date.today())
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event) + '\n'
    else:
        response += 'None'
    response += '\nEvents: \n'
    events = testBot.event_list.get_event_list()
    if len(events) != 0:
        for event in events:
            response += '-- '+ str(event)
    else:
        response += 'None'
    return response

def create_event(name, year, month, day, desc):
    # creates a new event and adds it to the list
    testBot.event_list.add_event(Event_List.event(name,datetime.date(year, month, day),desc))
    response = 'Okay, I made an event: '+str(testBot.event_list.get_event(name))
    return response

def list_reminders():
    response = 'Reminders: \n'
    reminders = testBot.reminder_list.get_reminders()
    if len(reminders) != 0:
        for reminder in reminders:
            response += '-- '+ str(reminder)+'\n'
    else:
        response += 'None'
    return response

def create_reminder(day, id, desc):
    testBot.reminder_list.add_reminder(Reminders.reminder(day, id, desc))
    response = 'Okay I have created a reminder: '+str(testBot.reminder_list.get_reminder(id))
    return response

# posts message into group
def post_message(message):
    test.post(str(BOT.bot_id),str(message))

# childish easter eggs cause I am a child
def check_easter_egg(text):
    if datetime.datetime.now().time == datetime.time(16,4):
        post_message("Error 4:04, command not found")
        return True
