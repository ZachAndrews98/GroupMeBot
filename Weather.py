# Created by Zachary Andrews
# Github: ZachAndrews98

import KEYS
import Weather

import pyowm

class weather:
    location = None
    def __init__(self, location):
        self.location = location

    def get_current_weather(self):
        weath = ""
        owm = pyowm.OWM(KEYS.WEATHER_KEY)
        observation = owm.weather_at_place(self.location)
        w = observation.get_weather()
        weath += '\n'+w.get_status() + '\nTemperature: ' + str(int(w.get_temperature('fahrenheit')['temp'])) + \
            '°\nHumidity: ' + str(w.get_humidity()) + '%'
        return weath
