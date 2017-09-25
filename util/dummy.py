# -*- coding:utf-8 -*-

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from albumdef import *
 
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/newwyy?charset=utf8', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# Create objects  
user = Album(name="大规模5", album_id=001, singer_name="末地", img='dsfsgsgdsf', date='24021-01', singer_id=02141)
session.add(user)
 
user = Album(name="大规模4", album_id=001, singer_name="末地", img='dsfsgsgdsf', date='24021-01', singer_id=02141)
session.add(user)
 
user = Album(name="大规模6", album_id=001, singer_name="末地", img='dsfsgsgdsf', date='24021-01', singer_id=02141)
session.add(user)
 
# commit the record the database
session.commit()
