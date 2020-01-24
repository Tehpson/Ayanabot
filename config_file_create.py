from configparser import ConfigParser

config = ConfigParser()

config['db'] = {
    'HOST': '192.168.1.246',
    'USERNAME': 'PaythonUsr',
    'PWD': '=Lx.k5bd`g*Km6\v',
    'NAME': 'ayanatehp'
}

config['twittersetting'] = {
    'CONSUMER_KEY': '15Z898d5ILHb0Xx7tDZmGK1si',
    'CONSUMER_SECRET': '4HSvDaSBZu8FyczNYIZuQfXI5CSgSdKm0OAsOUIkg54Fih2THg',
    'ACCESS_KEY': '1089407885141032960-ay2tuxXGW71BoEh7J02t6J3rBTIYue',
    'ACCESS_SECRET': 'Gr6KrvB8BxM52aglkIIIk9rUYRNAi87FNpYlg6Rh1B20e'
    }

config['Gamesetting'] = {
    'score_a_hello': '2',
    'powerupdate_a_time': '1'
}

with open ('./dev.ini', 'w') as f:
    config.write(f)

print ("update done")