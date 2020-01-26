import tweepy
import mysql.connector
from configparser import ConfigParser
import ctypes
import connect
import random
import time

ctypes.windll.kernel32.SetConsoleTitleW("Raid")

parser = ConfigParser()
parser.read('dev.ini')
api = connect.twitter_conn()
dbconn = connect.conndb()
dbcursor = dbconn.cursor()

raid_in_action = False
FILE_NAME_RAID = 'raid_power_file.txt'
FILE_NAME_STATUS = 'raid_status.txt'
diffrent_text = 1

def retrieve_file_data(file_name):
    f_read = open(file_name, 'r')
    raid_power = str(f_read.read().strip())
    f_read.close()
    return raid_power

def store_file_data(data, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(data))
    f_write.close()
    return






def raid_setup():
    print('--------------')
    #clears the database with all the entryes before raid 
    sql = "DELETE FROM raid"
    dbcursor.execute(sql)
    dbconn.commit()
    raid_power=random.randrange(1000,10000,1)
    store_file_data(raid_power, FILE_NAME_RAID)
    api.update_status('#Ayanabot our spy have informed us that the enamy are attacking and they have an army with '+str(raid_power)+' in power. they are about 30 min away')
    print ('#Ayanabot our spy have informed us that the enamy are attacking and they have an army with '+str(raid_power)+' in power')



    print('--------------')




def raid_attack():

    piret_attack_power=retrieve_file_data(FILE_NAME_RAID)
    player_attack_power = 0

    print('--------------')
    print ('raid_attack')
    sql= "SELECT attack_power FROM raid"
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    for power_value in result:
        player_attack_power = player_attack_power + int(power_value[0])
    piret_draw = random.randrange(0,int(piret_attack_power),1)
    player_draw = random.randrange(0,int(player_attack_power)+1,1)
    print('piret_draw = '+str(piret_draw))
    print('player_draw = '+str(player_draw))

    if piret_draw < player_draw:
        print ('players win')
        api.update_status('#Ayanabot Moste of the attackers was killed and they who didn\'t die did flee and everyone who was defending has shown that they deserve more power ')
        sql= "SELECT twitter_id FROM raid"
        dbcursor.execute(sql)
        result = dbcursor.fetchall()
        for id in result:
            twitter_ID = id[0]
            sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+str(twitter_ID)+"'"
            dbcursor.execute(sql)
            result = dbcursor.fetchone()
            for current_power in result:
                sql= "SELECT attack_power FROM raid WHERE twitter_ID = '"+str(twitter_ID)+"'"
                dbcursor.execute(sql)
                result = dbcursor.fetchone()
                for input_power in result:
                    win_with = player_draw - piret_draw

                    newpower = str(current_power + input_power + win_with) 
            sql = "UPDATE twitteruser SET power = '"+newpower+"' WHERE twitter_ID = '"+str(twitter_ID)+"'"
            dbcursor.execute(sql)
            dbconn.commit()

    elif piret_draw > player_draw:
        print ('Pirets win')
        if diffrent_text == 0:
            api.update_status('#Ayanabot Sadly the attackers were successful and killed everyone and did steal most of the power we had')
            diffrent_text = diffrent_text + 1
        elif diffrent_text == 1:
            api.update_status('#Ayanabot Mission fail let\'s get them next time')
            diffrent_text = 2
        elif diffrent_text == 2:
            api.update_status('#Ayanabot THEY TOOK ARE POWER AND KILLED US ALL' )
            diffrent_text = 0
    
    elif piret_draw == player_draw:
        print('draw')
        api.update_status('#Ayanabot You did not only kill all the attackers but also yourself, Because of this embarrassing defense everyone who was defending loses some power ')


    print('Raid is over')
    print('--------------')
        


while True:
    if raid_in_action == False:
        raid_setup()
        raid_in_action = True
        time_until_raid = 31
        while time_until_raid > 1:
            time_until_raid = time_until_raid -1
            raid_status = 'Raid ongoing they are about '+str(time_until_raid)+ ' minuts away'
            store_file_data(raid_status, FILE_NAME_STATUS)
            print ('Raid ongoing they are about '+str(time_until_raid)+ ' minuts away')
            time.sleep(60)
            

    else:
        raid_attack()
        raid_in_action = False
        time_until_raid = 31
        while time_until_raid > 1:
            time_until_raid = time_until_raid -1
            raid_status = 'Next raid is in '+str(time_until_raid)+ 'minuts'
            store_file_data(raid_status, FILE_NAME_STATUS)
            print ('Next raid is in '+str(time_until_raid)+ ' minuts')
            if time_until_raid == 10:
                print('#Ayanabot only 10 min left to join the defence')
            time.sleep(60)
            



