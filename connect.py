import mysql.connector
from configparser import ConfigParser
import ctypes
import tweepy

ctypes.windll.kernel32.SetConsoleTitleW("Connection")

parser = ConfigParser()
parser.read('dev.ini')

def conndb():
    dbconn = mysql.connector.connect(
    host=parser.get('db','host'),
    user=parser.get('db','username'),
    passwd=parser.get('db','pwd'),
    database=parser.get('db','name'),
    )
    return dbconn

def twitter_conn():
    auth = tweepy.OAuthHandler(parser.get('twittersetting','CONSUMER_KEY'), parser.get('twittersetting','CONSUMER_SECRET'))
    auth.set_access_token(parser.get('twittersetting','ACCESS_KEY'),parser.get('twittersetting','ACCESS_SECRET'))
    return tweepy.API(auth)