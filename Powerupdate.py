import tweepy
import time
import mysql.connector
from configparser import ConfigParser
import ctypes
import connect



ctypes.windll.kernel32.SetConsoleTitleW("Power Update")

parser = ConfigParser()
parser.read('dev.ini')

dbconn = connect.conndb()
dbcursor = dbconn.cursor()


print("connection with database establish") 


def add_power():
    updatecount = 0
    sql= "SELECT twitter_ID FROM twitteruser"
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    for id in result:
        twitter_ID = id[0]
        sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+str(twitter_ID)+"'"
        dbcursor.execute(sql)
        result = dbcursor.fetchone()
        for current_power in result:
            newpower = str(current_power + parser.getint('Gamesetting','powerupdate_a_time')) 
        sql = "UPDATE twitteruser SET power = '"+newpower+"' WHERE twitter_ID = '"+str(twitter_ID)+"'"
        dbcursor.execute(sql)
        dbconn.commit()
        updatecount = updatecount + 1
    print("powerupdate complete")
    print("updated power of "+str(updatecount)+" Accounts")
    print("-------")

while True:
    add_power()
    time.sleep(60)
