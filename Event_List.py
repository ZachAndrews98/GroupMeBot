# Created by Zachary Andrews
# Github: ZachAndrews98

import datetime
import os

# list of events
class event_list:
    event_list = list()
    def __init__(self):
        #self.event_list.clear()
        #self.check_for_events()
        print(event_list)

    # adds event to list
    def add_event(self, event):
        self.event_list.append(event)
        with open('events/event_list.evt','a') as file:
            file.write(str(event)+'\n')
        file.close()
        self.remove_blank_lines()

    # returns the entire list of events
    def get_event_list(self):
        return self.event_list

    # gets single event by name
    def get_event(self, event_name):
        for event in self.event_list:
            if event.name == event_name:
                return event

    # gets all events on a certain date
    def get_events_by_date(self, date):
        events = list()
        for event in self.event_list:
            if event.date == date:
                events.append(event)
        return events

    # deletes event by name
    def delete_event(self,event_name):
        with open('events/event_list.evt','w+') as file:
            for event in list(self.event_list):
                if event.name != event_name:
                    file.write(str(event)+'\n')
                if event.name == event_name:
                    self.event_list.remove(event)
        file.close()
        self.remove_blank_lines()

    # deletes all events on and before a given date
    def delete_event_before_date(self,date):
        with open('events/event_list.evt','w+') as file:
            for event in list(self.event_list):
                print(event.date <= date)
                if event.date > date:
                    file.write(str(event)+'\n')
                if event.date <= date:
                    self.event_list.remove(event)
        file.close()
        self.remove_blank_lines()

    # run at startup, checks if any events are stored, if there are adds them to the list
    def check_for_events(self):
        # if storage file exists
        try:
            file = open('events/event_list.evt','r')
            for line in file:
                print(line)
                line = line.split(', ')
                date = line[0].split('/')
                self.event_list.append(event(line[1],datetime.date(int(date[2]),
                                            int(date[0]),int(date[1])),line[2]))
            file.close()
        # creates file if doesn't exist
            print(self.event_list)
            print(len(self.event_list))
        except:
            file = open('events/event_list.evt','w+')
            file.close()
            return

    def remove_blank_lines(self):
        with open('events/event_list.evt') as filehandle:
            lines = filehandle.readlines()

        with open('events/event_list.evt', 'w+') as file:
            lines = filter(lambda x: x.strip(), lines)
            file.writelines(lines)
        filehandle.close()
        file.close()

# event class, stores information about an event
class event:
    name = None
    date = None
    desc = None
    def __init__(self, event_name, event_date, event_desc):
        self.name = event_name
        self.date = event_date
        self.desc = event_desc

    def __repr__(self):
        return str(self.date.month)+'/'+str(self.date.day)+ \
            '/'+str(self.date.year)+', '+self.name+', '+self.desc
