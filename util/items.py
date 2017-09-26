# -*- coding:utf-8 -*-
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/newwyy?charset=utf8', echo=True)
Base = declarative_base()
 
########################################################################
class Song(Base):
    """"""
    __tablename__ = "song"
 
    id = Column(BIGINT, primary_key=True)
    song_name = Column(String(512))
    song_id = Column(BIGINT,unique=True)
    album_id = Column(BIGINT)
    album_name = Column(String(512))
    singer_id = Column(BIGINT)
    singer_name = Column(String(512))
    date = Column(String(20))
    comment_num = Column(BIGINT)
    lyric = Column(TEXT)

 
class Comment(Base):
    """"""
    __tablename__ = "comment"
    id = Column(BIGINT, primary_key=True)
    nickname = Column(String(512))
    content = Column(TEXT)
    date = Column(String(20))
    song_name = Column(String(512))
    song_id = Column(BIGINT)
    likes = Column(BIGINT)
    user_id = Column(BIGINT)
    user_img = Column(String(512))
    comment_id = Column(BIGINT, unique=True)


    #----------------------------------------------------------------------
#    def __init__(self, name, album_id, singer_name, img, date, singer_id):
#        """"""
#        self.name = name
#        self.album_id = album_id
#        self.singer_name = singer_name
#        self.img = img
#	self.date = date
#	self.singer_id = singer_id
 
# create tables
Base.metadata.create_all(engine)
