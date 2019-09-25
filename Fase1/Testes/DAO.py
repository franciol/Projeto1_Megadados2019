import pymysql
import json

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        for result in cursor:
            print(result)


def connectMYSQL():
    with open('acesso.json') as json_data:
        d = json.load(json_data)


        connection = pymysql.connect(
        host=d['connection']['host'],
        user=d['connection']['user'],
        password=d['connection']['password'],
        database=d['connection']['database'])
    
        return connection


