
TIME_DESC = "Responds with the current time, I'm aware of the redundancy"
WEATHER_DESC = "Gives the current weather in Meadville, PA"
LIST_REMINDER_DESC = "Lists current day's reminders followed by all reminders scheduled"
LIST_EVENT_DESC = "Lists current day's events followed by all events scheduled"
CREATE_REMINDER_DESC = "Creates a weekly reminder for an inputted day"
CREATE_EVENT_DESC = "Creates an event that will occur on the inputted day"
DELETE_REMINDER_DESC = "Deletes the reminder with the inputted name"
DELETE_EVENT_DESC = "Deletes the event with the inputted name"
HELP_DESC = "Displays all commands that are available"
INFO_DESC = "Gives further information on the inputted command"

TIME_FORMAT = "time"
WEATHER_FORMAT = "weather"
LIST_REMINDER_FORMAT = "list reminders"
LIST_EVENT_FORMAT = "list events"
CREATE_REMINDER_FORMAT = "'create reminder: <day of week for reminder>, <name of reminder>, <reminder description>'"
CREATE_EVENT_FORMAT = "'create event: <date of event>, <name of event>, <event description>'"
DELETE_REMINDER_FORMAT = "'delete reminder: <name of reminder>'"
DELETE_EVENT_FORMAT = "'delete event: <name of event>'"
HELP_FORMAT = "help"
INFO_FORMAT = "info <full command name>"

TIME_INFO = [TIME_DESC, TIME_FORMAT]
WEATHER_INFO = [WEATHER_DESC, WEATHER_FORMAT]
LIST_REMINDER_INFO = [LIST_REMINDER_DESC, LIST_REMINDER_FORMAT]
LIST_EVENT_INFO = [LIST_EVENT_DESC, LIST_EVENT_FORMAT]
CREATE_REMINDER_INFO = [CREATE_REMINDER_DESC, CREATE_REMINDER_FORMAT]
CREATE_EVENT_INFO = [CREATE_EVENT_DESC, CREATE_EVENT_FORMAT]
DELETE_REMINDER_INFO = [DELETE_REMINDER_DESC, DELETE_REMINDER_FORMAT]
DELETE_EVENT_INFO = [DELETE_EVENT_DESC, DELETE_EVENT_FORMAT]
HELP_INFO = [HELP_DESC, HELP_FORMAT]
INFO_INFO = [INFO_DESC, INFO_FORMAT]

def get_info(text):
    if 'time' in text:
        response = 'Info: ' + TIME_INFO[0] + '\nFormat: ' + TIME_INFO[1]
    elif 'weather' in text:
        response = 'Info: ' + WEATHER_INFO[0] + '\nFormat: ' + WEATHER_INFO[1]
    elif 'list' in text:
        if 'events' in text:
            response = 'Info: ' + LIST_EVENT_INFO[0] + '\nFormat: ' + LIST_EVENT_INFO[1]
        elif 'reminders' in text:
            response = 'Info: ' + LIST_REMINDER_INFO[0] + '\nFormat: ' + LIST_REMINDER_INFO[1]
        else:
            response = 'That is not a possible command'
    elif 'create' in text:
        if 'event' in text:
            response = 'Info: ' + CREATE_EVENT_INFO[0] + '\nFormat: ' + CREATE_EVENT_INFO[1]
        elif 'reminder' in text:
            response = 'Info: ' + CREATE_REMINDER_INFO[0] + '\nFormat: ' + CREATE_REMINDER_INFO[1]
        else:
            response = 'That is not a possible command'
    elif 'delete' in text:
        if 'event' in text:
            response = 'Info: ' + DELETE_EVENT_INFO[0] + '\nFormat: ' + DELETE_EVENT_INFO[1]
        elif 'reminder' in text:
            response = 'Info: ' + DELETE_REMINDER_INFO[0] + '\nFormat: ' + DELETE_REMINDER_INFO[1]
        else:
            response = 'That is not a possible command'
    elif 'help' in text:
        response = 'Info: ' + HELP_INFO[0] + '\nFormat: ' + HELP_INFO[1]
    elif 'info' in text:
        response = 'Info: ' + INFO_INFO[0] + '\nFormat: ' + INFO_INFO[1]
    else:
        response = 'That is not a possible command'
    return response

