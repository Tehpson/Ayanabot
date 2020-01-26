import random
import tweepy
import connect
from configparser import ConfigParser
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Slot")

parser = ConfigParser()
parser.read('dev.ini')
api = connect.twitter_conn()
dbconn = connect.conndb()
dbcursor = dbconn.cursor()

values = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR"]

def spinnwhell():
    i = random.randrange(0,5,1)
    output = values[i]
    return output





def check(mention):
    text = mention.full_text.lower()
    numberarray = [int(s) for s in text.split() if s.isdigit()]
    if len(numberarray) > 1:
        api.update_status('@' + mention.user.screen_name +'#Ayanabot Error please only enter one value', mention.id)
        print('#Ayanabot Error please only enter one value')
    elif len(numberarray) == 0:
        api.update_status ('@' + mention.user.screen_name +'#Ayanabot Error you need to enter how much power you want to play with', mention.id)
        print('#Ayanabot Error you need to enter how much power you want to paly with')
    elif len(numberarray) == 1:
        input_power = numberarray[0]
        twitter_ID = str(mention.user.id)
        sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+twitter_ID+"'"
        dbcursor.execute(sql)
        result = dbcursor.fetchone()
        for current_power in result:
            if current_power < input_power:
                api.update_status('@' + mention.user.screen_name +'#Ayanabot  ERROR not enough Power', mention.id)
                print('#Ayanabot  ERROR not enough Power')
            else:
                result_output(input_power, mention)



def play():

    firstWheel = spinnwhell()
    secondWheel = spinnwhell()
    thirdWheel = spinnwhell()

    row=[firstWheel,secondWheel,thirdWheel]

    CHERRY = 0
    ORANGE = 0
    PLUM = 0
    BELL = 0
    BAR = 0
    LEMON = 0

    for item in row:
        if item == "CHERRY":
            CHERRY += 1
        if item == "ORANGE":
            ORANGE += 1
        if item == "PLUM":
            PLUM += 1
        if item == "BELL":
            BELL += 1         
        if item == "LEMON":
            LEMON += 1
        if item == "BAR":
            BAR += 1

    if  CHERRY == 1:
        win = 1
    elif  CHERRY == 2:
        win = 2
    elif  CHERRY == 3:
        win = 7
    elif  (ORANGE == 3) or (ORANGE == 2 and BAR == 1):
        win = 5
    elif  (PLUM == 3) or (PLUM == 2 and BAR == 1):
        win = 5
    elif  (BELL == 3) or (BELL == 2 and BAR == 1):
        win = 5
    elif  (LEMON == 3) or (LEMON == 2 and BAR == 1):
        win = 6
    elif  BAR == 3:
        win = 10
    else:
        win = 0
    
    return win

def result_output(power, mention):
    win = play()
    if win == 0:
        diffret_text = random.randrange(0,2,1)
        if diffret_text == 0:
            api.update_status('@' + mention.user.screen_name + '#Ayanabot you lost', mention.id)
        if diffret_text == 1:
            api.update_status('@' + mention.user.screen_name + '#Ayanabot better luck next time', mention.id)
        if diffret_text == 2:
            api.update_status('@' + mention.user.screen_name + '#Ayanabot you didn\'t win', mention.id)
        print ('@' + mention.user.screen_name+ 'lost')

    else:
        win_prize = power*win
        api.update_status('@' + mention.user.screen_name + '#Ayanabot you won '+str(win_prize)+'!', mention.id)
        print ('@' + mention.user.screen_name + '#Ayanabot you won '+str(win_prize)+'!')
        
        twitter_ID = str(mention.user.id)
        sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+str(twitter_ID)+"'"
        dbcursor.execute(sql)
        result = dbcursor.fetchone()
        for current_power in result:
            newpower = int(current_power) + win_prize
            sql = "UPDATE twitteruser SET power = '"+str(newpower)+"' WHERE twitter_ID = '"+str(twitter_ID)+"'"
            dbcursor.execute(sql)
            dbconn.commit()



    