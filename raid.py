import tweepy
import mysql.connector
from configparser import ConfigParser
import ctypes
import connect
import random
import time

ctypes.windll.kernel32.SetConsoleTitleW("Raid announce")

parser = ConfigParser()
parser.read('dev.ini')
api = connect.twitter_conn()
dbconn = connect.conndb()
dbcursor = dbconn.cursor()

raid_in_action = False

def raid_setup():
    raid_in_action = True
    raid_power=random.randrange(1000,10000,1)
    api.update_status('#Ayanabot : The Pirates are attacking and they have an army with '+raid_power+' in power')

def raid_attack():
    raid_in_action = False


while True:
    if raid_in_action == False:
        raid_setup()
    else:
        raid_attack()
    time.sleep(1800)

