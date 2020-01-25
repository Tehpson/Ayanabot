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
FILE_LAST_SEEN = 'last_seen_id.txt'
FILE_RAID_STATUS = 'raid_status.txt'



print("connection with database establish") 




def retrieve_filedata(file_name):
    f_read = open(file_name, 'r')
    data = str(f_read.read().strip())
    f_read.close()
    return data

def store_filedata(data, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(data))
    f_write.close()
    return

def raid_status():
    return str(retrieve_filedata(FILE_RAID_STATUS))


def raid_check(mention):
    if 'Next raid' in raid_status():
        api.update_status('@' + mention.user.screen_name +'#Ayanabot no current raid active please come back later', mention.id)
    else:
        text = mention.full_text.lower()
        numberarray = [int(s) for s in text.split() if s.isdigit()]
        if len(numberarray) > 1:
            api.update_status('@' + mention.user.screen_name +'#Ayanabot Error please only enter one value', mention.id)
            print('#Ayanabot Error please only enter one value')
        elif len(numberarray) == 0:
            api.update_status ('@' + mention.user.screen_name +'#Ayanabot Error you need to enter how power you want to add to the raid', mention.id)
            print('#Ayanabot Error you need to enter how power you want to add to the raid')
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
                    api.update_status('@' + mention.user.screen_name +'#Ayanabot '+str(input_power)+' Power have been placed to deffend against tha attacker', mention.id)
                    print('#Ayanabot '+str(input_power)+' Power have been placed to deffend against tha attacker')
                    new_power = int(current_power) - input_power

                    sql = "UPDATE twitteruser SET power = '"+str(new_power)+"' WHERE twitter_ID = '"+twitter_ID+"'"
                    dbcursor.execute(sql)
                    dbconn.commit()
                    print ("-->new power is "+str(new_power))

                    sql = "INSERT INTO raid (twitter_id, attack_power) VALUES (%s,%s)"
                    val = (twitter_ID, str(input_power))
                    dbcursor.execute(sql,val)
                    dbconn.commit()


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
        api.update_status('#Ayanabot Hello @' + mention.user.screen_name, mention.id)
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
    api.update_status('@' + mention.user.screen_name + '#Ayanabot You have '+ power +' power', mention.id)
    print ("-->Responding...")




#-----main----
def main_code():
    
    last_seen_id = int(retrieve_filedata(FILE_LAST_SEEN))

    print('\n')
    print('checking for uppdate')

    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        print('---------')
        print(str(mention.id) + ' - ' + str(mention.user.id) + ' - ' + mention.user.screen_name + ': ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_filedata(last_seen_id, FILE_LAST_SEEN)
        if '#ayanabot' in mention.full_text.lower():
            print('-->#Ayanabot found')
            check_databese_for_user(mention)
            if 'hello ' in mention.full_text.lower() or 'hi' in mention.full_text.lower():
                hello_phase(mention)

            if '!power' in mention.full_text.lower():
                check_power(mention)
            if '!raid ' in mention.full_text.lower():
                raid_check(mention)

            if '!attack' in mention.full_text.lower():
                attack.attack_check(mention)

            if '!raidstatus' in mention.full_text.lower():
                api.update_status('@' + mention.user.screen_name +' '+ raid_status(), mention.id)
                print ("-->Responding...")

        print('---------')

while True:
    main_code()
    time.sleep(15)