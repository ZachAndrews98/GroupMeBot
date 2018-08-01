# GroupMe Bot

## About

Created by Zachary Andrews
Github: ZachAndrews98

Creates and runs a bot from the terminal for the GroupMe app. Uses [Groupy](https://github.com/rhgrant10/Groupy)
to interface with GroupMe's API. Can post and read messages from the terminal.
Will analyze any message using the '@' symbol and the name of the bot in the
group. The bot can currently tell the time, weather, and create and keep track
of events as well as reminders for the group. These are kept in files under
`events/` or `reminders/` respectively. There is also a basic chatbot
implementation that uses the [ChatterBot](https://github.com/gunthercox/ChatterBot)
library for basic back and forth conversation.

## Startup

First clone the repository to your local machine. In a terminal execute
`pip3 install -r requirements.txt` to download all required packages. Once all
packages have downloaded run `python3 Main.py` to begin running the program. On
startup a config file will be generated and you will be prompted to enter a
[GroupMe API key](https://dev.groupme.com/). This key is INCREDIBLY important
and should not be shared with ANYONE, the program will also not function without
this. If you would like current weather capabilities you will also have to get
a key for [OpenWeatherMap(OWM)](https://home.openweathermap.org/) and put that
in the configuration file as well. Finally you will have to give a name for your
bot and the group for your bot to monitor. This group you must at least initially
be a member of since the group will be accessed using your GroupMe API key.

## Capabilities

The bot can post responses to commands given in the group chat if the message is
directed to the bot. The bot will not look at any chats that do not directly
mention it. It can also tell the time and weather in a given area by directing
'time' or 'weather' in a message at the bot. For events and reminders the
command scheme is a little more complicated. In the creation and deletion
processes a ':' is used to denote the end of the command and the beginning of
the parameters. The parameters differ depending on if an event or reminder is
being created, but should be separated by a ','. To view events and reminders
that have been created simply direct the message `list <events/reminders>` at
the bot. Everyday at 8:30 AM, the bot posts a message detailing all reminders
and events for that day. Also at this time events are checked to see if they
have already occurred. If they have, they are deleted from the  master list of
events.

### Create Event Parameters

The structure of the parameters should be: `<date>(m/d/y), <event name>, <event description>`.
Each of these is fairly self explanatory. Date is the date of the event, event
name is the name of the event and should be unique to each event, and event
description is the description of the event. This can include where and when the
event is occurring and what will be happening at said event.

### Create Reminder Parameters

The structure of the parameters should be: `<day>, <reminder name>, <description>`.
This system is set up for weekly reminders and as such is associated with a day
of the week instead of a date. As such the day should be given as either a
standard abbreviation or the fully written out day of the week. The name of the
reminder should be given next, followed by a description of what is happening.
Multiple reminders can be made for a single day of the week, but each reminder
should have a unique name as to avoid any confusion in the deletion process.

## Future plans

I plan to move the interaction between the bot and users to a direct messaging
system that only designated users will have access to. I also plan to try and
make the bot capable of responding to basic questions as well as throw in a few
fun little Easter eggs for possible responses.

## Current Bugs

Too many to go into detail. This system is incredibly buggy and I am slowly
figuring out bugs that I find in my testing, but chances are I will get tired of
bug hunting and fixing and will stop all together for a bit and focus on
features that I think would be cool to have, this is for my personal use after
all.

## Credit

This project uses both [Groupy](https://github.com/rhgrant10/Groupy) and
[ChatterBot](https://github.com/gunthercox/ChatterBot) for core functions.
I take no credit for any and all work done on those projects. [pyowm](https://github.com/csparpa/pyowm)
is used for current weather functionality.

## License

This project is lincensed under the [MIT Lincense](https://opensource.org/licenses/MIT)