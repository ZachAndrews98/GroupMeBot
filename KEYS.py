# Created by Zachary Andrews
# Github: ZachAndrews98

import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

def new_config():
    """Create a blank config file if one does not exist. """
    config.add_section('Keys')
    config.set('Keys', '; Important keys for access to APIs')
    config.set('Keys', 'GroupMe', "")
    config.set('Keys', 'Weather', "")
    config.add_section('Keywords')
    config.add_section('Bot')
    config.set('Bot', '; Key information for Bot creation')
    config.set('Bot', 'Bot Name', "")
    config.set('Bot', 'Group Name', "")

    with open('./config.ini', 'w') as config_file:
        config.write(config_file)

def get_bot_name():
    config.read('config.ini')
    return config.get('Bot','Bot Name')
def get_group_name():
    config.read('config.ini')
    return config.get('Bot','Group Name')
def get_groupme_key():
    config.read('config.ini')
    return config.get('Keys','GroupMe')
def get_weather_key():
    config.read('config.ini')
    return config.get('Keys','Weather')