import MySQLdb as mdb
import json
import settings

class Database:
    def connect(self):
        db = settings.DATABASE_NAME
        user = settings.DATABASE_USER
        password = settings.DATABASE_PASSWORD
        host = settings.DATABASE_HOST
        port = settings.DATABASE_PORT
        return mdb.connect(host=host, port=port, user=user, passwd=password, db=db)

    def close_connect(self, session):
        return session.close()

    '''
    INSERT, UPDATE, DELETE, CREATE, and SET statement
    '''
    def execute_non_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            session.commit()
            self.close_connect(session)
            return 1
        except Exception as e:
            return 0

    '''SELECT'''
    def execute_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            self.close_connect(session)
            return rows
        except Exception as e:
            print e
            return 0
