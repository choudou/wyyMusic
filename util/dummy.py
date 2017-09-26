# -*- coding:utf-8 -*-

import datetime
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items import *
 
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/newwyy?charset=utf8', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
try:
# Create objects  
    user = Song(song_name="大规模5", song_id=001, album_id=001, album_name = 'sgsf', singer_name="末地", comment_num=9324, date='24021-01', singer_id=02141, lyric='dgsfdsfsfsf')
    session.add(user)
    session.commit()
except exc.IntegrityError as ex:
    print ex
    session.rollback()
try:
    user = Song(song_name="大规模5", song_id=001, album_id=001, album_name = 'sgsf', singer_name="末地", comment_num=2414, date='24021-01', singer_id=02141, lyric='dgsfdsfsfsf')
    session.add(user)
    session.commit()
except Exception as ex:
    print ex.__class__
    session.rollback()

try: 
    user = Song(song_name="大规模5", song_id=002, album_id=001, album_name = 'sgsf', singer_name="末地", comment_num=2414, date='24021-01', singer_id=02141, lyric='dgsfdsfsfsf')
    session.add(user)
    session.commit()
except Exception as ex:
    print ex.__class__
    session.rollback()
# commit the record the database
