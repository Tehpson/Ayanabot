import tweepy
import time
import mysql.connector
from configparser import ConfigParser
import ctypes
import connect
import attack

ctypes.windll.kernel32.SetConsoleTitleW("Main")

parser = ConfigParser()
parser.read('dev.ini')
api = connect.twitter_conn()
dbconn = connect.conndb()
dbcursor = dbconn.cursor()
FILE_NAME = 'last_seen_id.txt'



print("connection with database establish") 




def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return





def check_databese_for_user(mention):
    twitter_ID = str(mention.user.id)
    sql= "SELECT * FROM twitteruser WHERE twitter_ID = '"+twitter_ID+"'"
    dbcursor.execute(sql)
    dbcursor.fetchall()
    if dbcursor.rowcount < 1:
        print("-->new user, adding user to database")
        add_to_database(mention)
    else:
        print("-->user already exist")

def add_to_database(mention):
    sql = "INSERT INTO twitteruser (twitter_ID,twitter_name) VALUES (%s,%s)"
    val = (str(mention.user.id), "@"+mention.user.screen_name)
    dbcursor.execute(sql,val)
    dbconn.commit()




def add_power(twitter_ID,power_type):
    sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+twitter_ID+"'"
    dbcursor.execute(sql)
    result = dbcursor.fetchone()
    for current_power in result:
        newpower = str(current_power + parser.getint('Gamesetting',power_type))
        
    sql = "UPDATE twitteruser SET power = '"+newpower+"' WHERE twitter_ID = '"+twitter_ID+"'"
    dbcursor.execute(sql)
    dbconn.commit()
    print ("-->new power is "+newpower)







def hello_phase(mention):
    print('-->Found hello phrase', flush=True)
    if mention.user.screen_name == 'tehpson':
        print("-->Not Responding... (reason: Not responing to myself)")
    else: 
        api.update_status('#Ayanabot : Hello @' + mention.user.screen_name, mention.id)
        print ("-->Responding...")
    add_power(str(mention.user.id),'power_a_hello')



def check_power(mention):
    print('-->Found !point', flush=True)
    twitter_ID = str(mention.user.id)
    sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+twitter_ID+"'"
    dbcursor.execute(sql)
    result = dbcursor.fetchone()
    for current_powerpower in result:
        power = str(current_powerpower)
    api.update_status('@' + mention.user.screen_name + '#Ayanabot : You have '+ power +' power', mention.id)
    print ("-->Responding...")





#-----main----
def main_code():
    
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    print('\n')
    print('checking for uppdate')

    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        print('---------')
        print(str(mention.id) + ' - ' + str(mention.user.id) + ' - ' + mention.user.screen_name + ': ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#ayanabot' in mention.full_text.lower():
            print('-->#Ayanabot found')
            check_databese_for_user(mention)
            if 'hello' in mention.full_text.lower() or 'hi' in mention.full_text.lower():
                hello_phase(mention)
            if '!power' in mention.full_text.lower():
                check_power(mention)
            if '!attack' in mention.full_text.lower():
                namearray = []
                count = 0
                for name in mention.full_text.lower().split(): 
                    if name.startswith('@'):
                        namearray.append(name)
                        count = count + 1
                if count == 2:
                    attack.attack_setup(mention,namearray)
                elif count == 1:
                    api.update_status('@' + mention.user.screen_name + '#Ayanabot : You need to enter a victum', mention.id)
                elif count >2:
                    api.update_status('@' + mention.user.screen_name + '#Ayanabot : you can only attack one at the time', mention.id)

        print('---------')

while True:
    main_code()
    time.sleep(15)