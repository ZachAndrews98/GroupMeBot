# Created by Zachary Andrews
# Github: ZachAndrews98

class reminder_list:
    reminders = list()

    def __init__(self):
        self.reminders.clear()
        self.check_for_reminders()

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        with open('reminders/reminders.rmndr','a') as file:
            file.write(str(reminder)+'\n')
        file.close()

    def delete_reminder(self, reminder_id):
        deleted = False
        with open('reminders/reminders.rmndr','w+') as file:
            for reminder in list(self.reminders):
                if reminder.id != reminder_id:
                    file.write(str(reminder)+'\n')
                else:
                    self.reminders.remove(reminder)
                    deleted = True
        file.close()
        return deleted

    def get_reminders(self):
        return self.reminders

    def get_reminder(self, reminder_id):
        for reminder in self.reminders:
            if reminder.id == reminder_id:
                return reminder

    def get_reminders_by_day(self, day):
        reminder_list = list()
        for reminder in self.reminders:
            if reminder.day == day:
                reminder_list.append(reminder)
        return reminder_list

    def check_for_reminders(self):
        # if storage file exists
        try:
            file = open('reminders/reminders.rmndr','r')
            for line in file:
                line = line.split(':')
                day = line[0].strip()
                id = line[1].split('- ')[0].strip()
                desc = line[1].split('- ')[1].strip()
                self.reminders.append(reminder(day, id, desc))
            file.close()
        # creates file if doesn't exist
        except:
            file = open('reminders/reminders.rmndr','w+')
            file.close()
            return

class reminder:
    days = {'mon': 0, 'monday': 0, 'tues': 1, 'tuesday': 1, 'weds': 2, 'wednesday': 2, 'thurs': 3,
            'thursday': 3, 'fri': 4, 'friday': 4, 'sat': 5, 'saturday': 5, 'sun': 6, 'sunday': 6}
    day = None
    id = None
    desc = None

    def __init__(self, day, id, desc):
        self.day = self.days[day.lower()]
        self.Day = day
        self.id = id
        self.desc = desc

    def __repr__(self):
        return self.Day+': '+self.id+'- '+self.desc
