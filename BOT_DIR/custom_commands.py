import logging
import os
import mysql.connector
import logging
from twitchio.ext import routines
import time
from datacleaner import *

# Define vars
auteurs = {}
commands = {}
queues = {}
roulettes = {}
active_queues = {}
params = {
    'user':'yourdbuser',
    'password':'yourpassword',
    'host':'127.0.0.1',
    'port':3306,
    'database':'TWITCH_BOT'
}

def init_commands():
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT commands.command, CHANNEL_LIST.channel, commands.text FROM commands INNER JOIN CHANNEL_LIST ON CHANNEL_LIST.id = commands.channel"
        )
        commands_raw = cur.fetchall()

        for command in commands_raw:
            commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def find_command(message):
    command = message.content.split()[0]
    channel = message.author.channel.name

    command_text = commands.get((command, channel))

    return command_text


def add_command(command, channel, text):
    commands[(command, channel)] = text

    # Now adds it to db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mysql.connector.connect(**params)


        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
                f"INSERT INTO commands (command, channel, text) VALUES ('{command}', (SELECT id from CHANNEL_LIST where channel = '{channel}'), '{text}')"
            )

        conn.commit()

        #for command in commands_raw:
        logging.info(command[1])
        commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def edit_command(command, channel, text):
    commands[(command, channel)] = text

    # Now updates db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"UPDATE commands SET text = '{text}' WHERE command = '{command}' AND channel = (SELECT id from CHANNEL_LIST where channel = '{channel}')"
        )
        conn.commit()

        #for command in commands_raw:
        logging.info(command[1])
        commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def remove_command(command, channel):
    commands.pop((command, channel))

    # Now updates db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM commands WHERE command='{command}' AND channel= (SELECT id from CHANNEL_LIST where channel = '{channel}')"
        )

        conn.commit()

        #for command in commands_raw:
        logging.info(command[1])
        commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')

### ROUTINES ###
def routine_factory(channel, seconds, minutes, hours, routine_text):
    @routines.routine(seconds=seconds, minutes=minutes, hours=hours, wait_first=False)
    async def temp_routine():
        await channel.send(routine_text)

    return temp_routine


def add_routine(
        channel, name, seconds, minutes,
        hours, routine_text):

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Adding new routine to db')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO routines (channel, name, seconds, minutes, hours, routine_text) VALUES ((SELECT id from CHANNEL_LIST where channel = '{channel}'), '{name}', '{seconds}', '{minutes}', '{hours}', '{routine_text}')"
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def init_routines(bot):
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    routines_db = {}
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Initializing routines')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"SELECT CHANNEL_LIST.channel, routines.name, routines.seconds, routines.minutes, routines.hours, routines.routine_text FROM routines INNER JOIN CHANNEL_LIST ON CHANNEL_LIST.id = routines.channel"
        )
        routines_raw = cur.fetchall()


        for routine in routines_raw:
            chan = bot.get_channel(routine[0])
            routines_db[routine[0] + '_' + routine[1]] = routine_factory(
                channel=chan,
                seconds=int(routine[2]),
                minutes=int(routine[3]),
                hours=int(routine[4]),
                routine_text=routine[5]
            )
            routines_db[routine[0] + '_' + routine[1]].start()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
        return routines_db


def remove_routine(channel, name):
    # Now delete from db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Removing routine from db')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM routines WHERE channel = (SELECT id from CHANNEL_LIST where channel = '{channel}') AND name = '{name}'"
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')



def init_users(channels):

    # Now reading from db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Init users to db')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        for i in channels:
            chan = str("'" + i + "'")
            cur.execute(
                f"INSERT IGNORE INTO CHANNEL_LIST (channel) VALUES (" + chan + ")",
            )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')

### ROULETTES

def init_roulettes(channels):
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing roulettes')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute multiple statements
        
        for twitch_chan in channels:
            # Reinit 'auteur' var
            roulette=[]
            cur.execute(
                f"SELECT roulette FROM CHANNEL_LIST where CHANNEL_LIST.channel = '{twitch_chan}'"
            )
            roulette_raw = cur.fetchall()
            roulette_clean = cleansql(roulette_raw)
            for roulette_tmp in roulette_clean:
                roulette.append(roulette_tmp)
            
            roulettes[f'{twitch_chan}'] = roulette


        
        # close the communication with the MariaDB
        cur.close()
    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')



def roulettes_active_check(channel): #check if a roulettes channel is active or not
    
    if "started" in roulettes[f'{channel}']:
        token = True
    else:
        token = False
        return token


def start_roulette(channel):
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing queues')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()


  
        cur.execute(
                f"UPDATE CHANNEL_LIST SET roulette = 'started' where channel = '{channel}'"
        )

            
        roulettes[f'{channel}'] = 'started'

        
        # close the communication with the MariaDB
        conn.commit()
        cur.close()
    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
  

def stop_roulette(channel):    
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing queues')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute multiple statements
        


  
        cur.execute(
                f"UPDATE CHANNEL_LIST SET roulette = 'stopped' where channel = '{channel}'"
        )

            
        roulettes[f'{channel}'] = 'stopped'

        
        # close the communication with the MariaDB
        conn.commit()
        cur.close()
    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


#### STREAM QUEUES         
            
def join_queue(channel, user):

    # Now connecting it to db
    conn = None
    try:
        #read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info(f'Joining {user} to queue')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO stream_queue (channel, user) VALUES ((SELECT id from CHANNEL_LIST where channel = '{channel}'), '{user}')"
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()
        queues[f'{channel}'].append(user)
        
        result = True        
        

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
        result = False
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
            print(result)
            return result


def leave_queue(channel, user):

    # Now connecting to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info(f'Leaving {user} from queue')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"DELETE FROM stream_queue WHERE channel = (SELECT id from CHANNEL_LIST where channel = '{channel}') AND user = '{user}'"
        )

        conn.commit()
        
        queues[f'{channel}'].remove(user)
        result = True
        
    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
        result = False
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
            return result

def clear_queue(channel):

    # Now connecting to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info(f'Clearing {channel} queue')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"DELETE FROM stream_queue WHERE channel = (SELECT id from CHANNEL_LIST where channel = '{channel}')"
        )

        conn.commit()

        queues[f'{channel}'] = []


        # close the communication with the MariaDB
        cur.close()
        result = True

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
        result = False
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
            return result


            
def queue_on_off(channel, boolean): 

    # Now connecting to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Queue on/off')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"UPDATE CHANNEL_LIST SET queue = '{boolean}' WHERE channel = '{channel}'"
        )

        conn.commit()
        active_queues[f'{channel}'] = boolean


        # close the communication with the MariaDB
        cur.close()
        result = True
    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
        result = False
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
            return result

def queue_active_check(channel): #check if a queue channel is active or not

    if active_queues[f'{channel}'] == 1:
        token = True
    else:
        token = False
        return token

def queue_next(channel):  #Calls the next user in queue
    
    queues_tmp = queues[f'{channel}']
    if queues_tmp[0] == '':
        return False
    user = queues_tmp[0]
    queues_tmp.append(user)
    del queues_tmp[0]
    queues[f'{channel}'] = queues_tmp
    return user


def queue_end(channel,user):  #Put user at the end
    
    queues_tmp = queues[f'{channel}']

    if user in queues_tmp:
        queues_tmp.remove(user)
        queues_tmp.append(user)
    else:
        return False

    queues[f'{channel}'] = queues_tmp
    return True
    

            
def init_queue(channels):

    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing queues')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute multiple statements
        
        for twitch_chan in channels:
            # Reinit 'auteur' var
            queue=[]
            cur.execute(
                f"SELECT stream_queue.user FROM stream_queue INNER JOIN CHANNEL_LIST ON CHANNEL_LIST.id = stream_queue.channel where CHANNEL_LIST.channel = '{twitch_chan}' ORDER BY stream_queue.id ASC"
            )
            queues_raw = cur.fetchall()
            queues_clean = cleansql(queues_raw)
            for queue_tmp in queues_clean:
                queue.append(queue_tmp)
            
            queues[f'{twitch_chan}'] = queue



        cur.execute(
            f"SELECT channel, queue FROM CHANNEL_LIST"
        )
        queues_raw = cur.fetchall()
        for queue_tmp in queues_raw:
            active_queues[(queue_tmp[0])] = queue_tmp[1]
        
        # close the communication with the MariaDB
        cur.close()
    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def list_queue(channel): #displays players in the queue
    queue_tmp = queues[f'{channel}'] #if queue is empty
    if len(queue_tmp) == 0:
        return False
        
    waitfile = str('') #initializing string var
    for i in queue_tmp:
        if i == queue_tmp[0]:
            waitfile += '[next] ' #define who is the next player on the queue
        
        waitfile += str(f"{i}, ") #listing all players
    waitfile = str(waitfile)[:-2] # remove coma
    return waitfile


###FUNCTIONS BELOW THIS LINE ARE NOT EXPLOITED YET, I WILL FIX THE CITATION COMMAND ON COGS DIR
def add_author(channel, author):

    # Now connecting it to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Adding new author to db')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO quoteauthors (channel, allowedauthor) VALUES ((SELECT id from CHANNEL_LIST where channel = '{channel}'), '{author}')"
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()
        auteurs[f'{channel}'].append(author)
        
        

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def del_author(channel, author):

    # Now connecting to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Removing author to db')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute(
            f"DELETE FROM quoteauthors WHERE channel = (SELECT id from CHANNEL_LIST where channel = '{channel}') AND allowedauthor = '{author}'"
        )

        conn.commit()
        
        auteurs[f'{channel}'].remove(author)
        

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def list_author (channel):
    authorized_authors = auteurs.get(channel)
    return authorized_authors


def find_author (channel, author):
    authorized_authors = auteurs.get(channel)
    srch_auteur = cleanstring(author)
    token = srch_auteur in authorized_authors
    print(token)
    return token
    



def init_authors(channels):

    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute multiple statements
        
        for twitch_chan in channels:
            # Reinit 'auteur' var
            auteur=[]
            cur.execute(
                f"SELECT quoteauthors.allowedauthor FROM quoteauthors INNER JOIN CHANNEL_LIST ON CHANNEL_LIST.id = quoteauthors.channel where CHANNEL_LIST.channel = '{twitch_chan}'"
            )
            auteurs_raw = cur.fetchall()
            auteurs_clean = cleansql(auteurs_raw)
            for auteur_tmp in auteurs_clean:
                auteur.append(auteur_tmp)
            
            auteurs[f'{twitch_chan}'] = auteur

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')

