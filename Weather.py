# Created by Zachary Andrews
# Github: ZachAndrews98

import KEYS

try:
    import pyowm
except BaseException:
    print("Required packages not installed, please run pip3 install -r requirements.txt")
    quit()


def get_current_weather():
    weath = ""
    try:
        owm = pyowm.OWM(KEYS.get_weather_key())
        observation = owm.weather_at_place('Meadville, PA, US')
        w = observation.get_weather()
        weath += '\n' + w.get_status() + '\nTemperature: ' + str(int(w.get_temperature('fahrenheit')
                                                                     ['temp'])) + '°F\nHumidity: ' + str(w.get_humidity()) + '%'
        return weath
    except BaseException:
        return "No key entered in configuration file, weather cannot be given"
