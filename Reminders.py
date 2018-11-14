# Created by Zachary Andrews
# Github: ZachAndrews98

file_name = '.reminders/reminders.rmndr'


# list of reminders
class reminder_list:
    reminders = list()

    def __init__(self):
        self.reminders.clear()

    # adds new reminder
    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        with open(file_name, 'a') as file:
            file.write(str(reminder) + '\n')
        file.close()
        self.remove_blank_lines()

    # deletes a specified reminder
    def delete_reminder(self, reminder_id):
        deleted = False
        with open(file_name, 'w+') as file:
            for reminder in list(self.reminders):
                if reminder.id != reminder_id:
                    file.write(str(reminder) + '\n')
                else:
                    self.reminders.remove(reminder)
                    deleted = True
        file.close()
        return deleted

    # returns the list of reminders
    def get_reminder_list(self):
        return self.reminders

    # returns a specific reminder
    def get_reminder(self, reminder_id):
        for reminder in self.reminders:
            if reminder.id == reminder_id:
                return reminder

    # returns a list of reminders for a specific day
    def get_reminders_by_day(self, day):
        reminder_list = list()
        for reminder in self.reminders:
            if reminder.day == day:
                reminder_list.append(reminder)
        return reminder_list

    # run at startup, checks if any reminders are stored, if there are adds them
    # to the list
    def check_for_reminders(self):
        # if storage file exists
        try:
            file = open(file_name, 'r')
            for line in file:
                line = line.replace("\n","")
                if "\n" in line:
                    print("\t\tTRUE")
                line = line.split(':')
                day = line[0].strip()
                id = line[1].split('- ')[0].strip()
                desc = line[1].split('- ')[1].strip()
                self.reminders.append(reminder(day, id, desc))
            file.close()
        # creates file if doesn't exist
        except BaseException:
            file = open(file_name, 'w+')
            file.close()
            return

    # removes blank lines in ./.reminders/reminders.rmndr
    def remove_blank_lines(self):
        with open(file_name) as filehandle:
            lines = filehandle.readlines()

        with open(file_name, 'w+') as file:
            lines = filter(lambda x: x.strip(), lines)
            file.writelines(lines)
        filehandle.close()
        file.close()


# reminder class, stores information about reminders
class reminder:
    days = {
        'mon': 0,
        'monday': 0,
        'tues': 1,
        'tuesday': 1,
        'weds': 2,
        'wednesday': 2,
        'thurs': 3,
        'thursday': 3,
        'fri': 4,
        'friday': 4,
        'sat': 5,
        'saturday': 5,
        'sun': 6,
        'sunday': 6}
    day = None
    id = None
    desc = None

    def __init__(self, day, id, desc):
        self.day = self.days[day.lower()]
        self.Day = day
        self.id = id
        self.desc = desc

    def __repr__(self):
        return self.Day + ': ' + self.id + '- ' + self.desc
