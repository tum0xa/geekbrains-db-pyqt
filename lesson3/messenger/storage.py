from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper

from settings import *


class Storage:
    class Clients:
        def __init__(self, username):
            self.id = None
            self.username = username

    class History:
        def __init__(self, client, last_login):
            self.id = None
            self.client = client
            self.last_login = last_login

    class ContactList:
        def __init__(self, owner_id, client_id):
            self.id = None
            self.owner_id = owner_id
            self.client_id = client_id

    def __init__(self, db_name, pool_recycle=7200):
        self.db_engine = create_engine(db_name, echo=False, pool_recycle=pool_recycle)

        self.metadata = MetaData()

        clients_table = Table('Clients', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('username', String, unique=True),
                              Column('information', String)
                              )

        history_table = Table('History', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('client', ForeignKey('Clients.id'), unique=True),
                              Column('last_login', DateTime),
                              Column('ip_address', String)
                              )
        contact_list_table = Table('ContactList', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('owner_id', Integer, primary_key=True),
                                   Column('client_id', Integer, primary_key=True))

        self.metadata.create_all(self.db_engine)

        mapper(self.Clients, clients_table)
        mapper(self.History, history_table)
        mapper(self.ContactList, contact_list_table)


if __name__ == '__main__':
    test_db = Storage(DEFAULT_DB)
    clients = Storage.Clients('TestClient')

