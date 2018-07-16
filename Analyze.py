# Created by Zachary Andrews
# Github: ZachAndrews98

import datetime

import Main
import Weather
import Log
import Functions
import Info
import Chat

def analyze_message(text,name):
    response = ''
    at_bot = '@'+Main.BOT.name
    text = text[len(at_bot)+1:]
    Log.log_info(str(datetime.datetime.now())+" >> "+name+": "+text)
    if Functions.check_easter_egg(text):
        return
    if text == at_bot:
        response = 'Hi, @'+str(name)+' what would you like?'
    # if the message mentions info
    elif 'info' in text:
        response = Info.get_info(text)
    # if the message mentions time
    elif 'time' in text:
        time = datetime.datetime.now().time()
        hour = time.hour
        minute = time.minute
        if hour > 12:
            hour = hour % 12
            end = 'PM'
        else:
            end = 'AM'
        response = 'The time is currently: '+str(hour)+':'+str(minute)+' '+end
    # if the message mentions weather
    elif 'weather' in text:
        response = 'The weather is currently: '+Weather.get_current_weather()
    # if the message mentions events
    elif 'event' in text:
        # checks if list command
        if 'list' in text:
            response = Functions.list_events()
        # checks if the event command is properly formatted
        elif ':' not in text:
            response = "Make sure you include a ':' after the name of the command and try again"
        # checks if create command
        elif 'create' in text:
            try:
                info = text.split(':')[1].split(',')
                date = info[0].split('/')
                if len(date[2]) != 4:
                    date[2] = '20'+date[2]
                # breaks up message into segments for parsing
                name = str(info[1]).strip()
                year = int(date[2])
                month = int(date[1])
                day = int(date[0])
                desc = info[2].strip()
                response = Functions.create_event(name,year,month,day,desc)
            except Exception:
                response = "An error occurred, check the format of the command"
                Log.log_error(Exception)

        # checks if delete command
        elif 'delete' in text:
            text = text.split(':')
            Functions.event_list.delete_event(text[1].strip())
            response = 'Okay I have removed the event'
        else:
            response = "I'm sorry, I don't believe that is one of the options"
    elif 'reminder' in text:
        response = ''
        if 'list' in text:
            response = Functions.list_reminders()
        elif ':' not in text:
            response = "Make sure you include a ':' after the name of the command and try again"
        elif 'create' in text:
            try:
                info = text.split(':')[1].split(',')
                day = info[0].strip()
                id = info[1].strip()
                desc = info[2].strip()
                response = Functions.create_reminder(day, id, desc)
            except Exception:
                response = "An error occurred, check the format of the command"
                Log.log_error(Exception)
        elif 'delete' in text:
            text = text.split(':')
            Functions.delete_reminder(text[1].strip())
        else:
            response = "I'm sorry, I don't believe that is one of the options"
    elif 'help' in text:
        response = 'Heres a list of my commands:\n'+str(Main.commands)+\
                    '\nUse "Info" <command> for more info on a command'
    else:
        response = Chat.chat(text)
    # posts the response in the group
    Functions.post_message(response)
    Log.log_info((str(datetime.datetime.now())+" >> "+Main.BOT.name+": "+str(response)))
