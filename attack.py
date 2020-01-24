import tweepy
import mysql.connector
from configparser import ConfigParser
import ctypes
import connect
import random

ctypes.windll.kernel32.SetConsoleTitleW("Attack")

parser = ConfigParser()
parser.read('dev.ini')
api = connect.twitter_conn()
dbconn = connect.conndb()
dbcursor = dbconn.cursor()

def attack_setup(mention, namearray):
    if namearray[0] == "@tehpson":
        opponent = namearray[1]
    else:
        opponent = namearray[0]
    
    opponent_ID = str(api.get_user(opponent).id)
    attacker_ID = str(mention.user.id)

    sql= "SELECT * FROM twitteruser WHERE twitter_ID = '"+opponent_ID+"'"
    dbcursor.execute(sql)
    dbcursor.fetchall()
    if dbcursor.rowcount < 1:
        print("-->opponent dosent exist")
        api.update_status('@' + mention.user.screen_name + '#Ayanabot : ' +opponent+' have never enter the game', mention.id)
    else:
        print("-->opponent is in database")

        #look up power of opponent
        sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+opponent_ID+"'"
        dbcursor.execute(sql)
        result = dbcursor.fetchone()
        for current_powerpower in result:
            opponent_power = str(current_powerpower)
            print("opponent power:" +opponent_power)
        
        #look up power of attacker
        sql= "SELECT power FROM twitteruser WHERE twitter_ID = '"+attacker_ID+"'"
        dbcursor.execute(sql)
        result = dbcursor.fetchone()
        for current_powerpower in result:
            attacker_power = str(current_powerpower)
            print("attacker power:" +attacker_power)

        attack_action(opponent_ID,attacker_ID,opponent_power,attacker_power,opponent,mention)


def attack_action(opponent_ID,attacker_ID,opponent_power,attacker_power,opponent_name,mention):
    opponent_darw = random.randrange(0,int(opponent_power),1)
    attacker_darw = random.randrange(0,int(attacker_power),1)
    print(opponent_darw)
    print(attacker_darw)
    if opponent_darw - attacker_darw > 0:
        #opponent win
        win_with = opponent_darw - attacker_darw
        opponent_new_power = int(attacker_power)/2 + int(opponent_darw)
        attacker_new_power = int(attacker_power)/2
        api.update_status('#Ayanabot :@' + mention.user.screen_name + ' You lost with '+ str(win_with)+' trops and you power is now at '+str(attacker_new_power), mention.id)
        api.update_status('#Ayanabot :'+ opponent_name +' You won with '+ str(win_with)+' trops and you power is now at '+str(opponent_new_power), mention.id)


    elif attacker_darw - opponent_darw > 0:
        #attacker win
        win_with = attacker_darw - opponent_darw
        attacker_new_power = int(opponent_darw)/2 + int(attacker_power)
        opponent_new_power = int(opponent_darw)/2
        api.update_status('#Ayanabot :@' + mention.user.screen_name + ' You won with '+ str(win_with)+' trops and you power is now at ' +str(attacker_new_power), mention.id)
        api.update_status('#Ayanabot :'+ opponent_name +' You lost with '+ str(win_with)+' trops and you power is now at '+str(opponent_new_power), mention.id)
    elif opponent_darw - attacker_darw  == 0:
        #draw
        opponent_new_power = int(opponent_darw)/4*3
        attacker_new_power = int(attacker_power)/4*3
        api.update_status('#Ayanabot :@' + mention.user.screen_name +' It is a draw and you power is now at '+str(attacker_new_power), mention.id)
        api.update_status('#Ayanabot :'+opponent_name +' It is a draw and you power is now at '+str(opponent_new_power), mention.id)

    update_power(opponent_ID,attacker_ID,opponent_new_power,attacker_new_power)


def update_power(opponent_ID,attacker_ID,opponent_new_power,attacker_new_power):
    #update oppnents power
    sql = "UPDATE twitteruser SET power = '"+str(opponent_new_power)+"' WHERE twitter_ID = '"+str(opponent_ID)+"'"
    dbcursor.execute(sql)
    dbconn.commit()

    #update attacker power
    sql = "UPDATE twitteruser SET power = '"+str(attacker_new_power)+"' WHERE twitter_ID = '"+str(attacker_ID)+"'"
    dbcursor.execute(sql)
    dbconn.commit()
