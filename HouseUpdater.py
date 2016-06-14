#!/usr/bin/python3
""" Updates the REFIT House Information """

import urllib.request, urllib.error, urllib.parse
import json
import mysql.connector
from mysql.connector import errorcode
import time

connectionConfig = {
    'user': 'xxxx',
    'password': 'xxxx',
    'host': 'xxxx',
    'database': 'xxxx'
    }

## Database Connection & Cursors
##
try:
    house_connection = mysql.connector.connect(**connectionConfig)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor_edit = house_connection.cursor(buffered=True)
cursor_query = house_connection.cursor(buffered=True)

## SQL Queries
##
house_check_sql = (
    "SELECT houseID FROM houseInfo "
    "WHERE houseID = %(houseID)s"
    )

house_insert_sql = (
    "INSERT INTO houseInfo "
    "(houseID, houseName, houseServer, lastUpdate) "
    "VALUES (%(houseID)s, %(houseName)s,"
    " %(houseServer)s, %(lastUpdate)s)"
    )

house_update_sql = (
    "UPDATE houseInfo "
    "SET houseName=%(houseName)s, houseServer=%(houseServer)s,"
    " lastUpdate=%(lastUpdate)s WHERE houseID=%(houseID)s"
    )

script_insert_sql = (
    "INSERT INTO scriptInfo "
    "(houseID) "
    "VALUES (%(houseID)s)"
    )

## Functions
##

def server_call():
    """ Queries the MiOS server to get currently connected houses """
    url = "https://sta1.mios.com/locator_json.php?username=xxxx" # Replace xxxx with Vera username.
    house_content = urllib.request.urlopen(url).read().decode("utf-8")
    house_data = json.loads(house_content)
    return house_data

def house_insert():
    """ Inserts newly found houses """
    ## Calls & Parses
    house_data = server_call()
    for i in house_data['units']:
        ## Checks if record already exists
        cursor_query.execute(house_check_sql, {'houseID': i['serialNumber']})
        size = cursor_query.fetchall()
        if not size:
            ## Creates new record if house has been added
            cursor_edit.execute(house_insert_sql,
                                {'houseID':i['serialNumber'],
                                 'houseName':i['name'],
                                 'houseServer':i['active_server'],
                                 'lastUpdate':time.strftime('%Y-%m-%d %H:%M:%S')
                                }
                               )
            cursor_edit.execute(script_insert_sql,
                                {'houseID':i['serialNumber']})
            house_connection.commit()

def house_update():
    """ Updates existing houses """
    ## Calls & Parses
    house_data = server_call()
    for u in house_data['units']:
        ## Updates existing records
        cursor_edit.execute(house_update_sql,
                            {'houseID':u['serialNumber'],
                             'houseName':u['name'],
                             'houseServer':u['active_server'],
                             'lastUpdate':time.strftime('%Y-%m-%d %H:%M:%S')})
        house_connection.commit()

if __name__ == '__main__':
    house_insert()
    house_update()
    house_connection.close()