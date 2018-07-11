# Created by Zachary Andrews
# Github: ZachAndrews98

import datetime

import Main
import Log
import Functions

def analyze_message(message):
    response = ''
    text = message.text.lower()
    at_bot = '@'+Main.BOT.name
    # checks if the bot is mentioned
    if at_bot.lower() in text:
        Log.log_info(str(datetime.datetime.now())+" >> "+message.name+": "+message.text)
        if Functions.check_easter_egg(text):
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
            elif 'list' in text:
                if 'events' in text:
                    response = 'List Events: Lists all events that are scheduled'
                elif 'reminders' in text:
                    response = 'List Reminders: Lists all reminders that are scheduled'
                else:
                    response = 'That is not a possible command'
            elif 'create' in text:
                if 'event' in text:
                    response = 'Create Event: Creates an event, should be formatted as such- ' +\
                    'create event: <date>(m/d/y), <event name>, <event description>'
                elif 'reminders' in text:
                    response = 'Create Reminder: Creates a reminder, should be formatted as such- ' +\
                    'create reminder: <day>, <reminder name>, <reminder description>'
                else:
                    response = 'That is not a possible command'
            elif 'delete' in text:
                if 'event' in text:
                    response = 'Delete Event: Delete an event, the name of the event should be right'+\
                                'after the command'
                elif 'reminder' in text:
                    response = 'Delete Reminder: Delete a reminder, the name of the reminder should be '+\
                                'right after the command'
                else:
                    response = 'That is not a possible command'
            elif 'help' in text:
                response = 'Help: Displays possible commands'
            else:
                response = 'That is not a possible command'
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
            response = 'The weather is currently: '+Main.weather.get_current_weather()
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
                info = text.split(':')[1].split(',')
                day = info[0].strip()
                id = info[1].strip()
                desc = info[2].strip()
                response = Functions.create_reminder(day, id, desc)
            elif 'delete' in text:
                text = text.split(':')
                Functions.delete_reminder(text[1].strip())
            else:
                response = "I'm sorry, I don't believe that is one of the options"
        elif 'help' in text:
            response = 'Heres a list of my commands:\n'+str(Main.bot_commands)+\
                        '\nUse "Info" <command> for more info on the command'
        else:
            response = "I'm sorry @"+message.name+", I don't understand"
        # posts the response in the group
        Functions.post_message(response)
        Log.log_info((str(datetime.datetime.now())+" >> "+Main.BOT.name+": "+response))
