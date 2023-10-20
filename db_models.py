from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from database import base

class Questions(base):
    __tablename__='questions'
    id=Column(Integer,primary_key=True,index=True)
    questions_text=Column(String,index=True)

class Choices(base):
    __tablename__='choices'
    id=Column(Integer,primary_key=True,index=True)
    choice_text=Column(String,index=True)
    is_correct=Column(Boolean,default=False)
    question_id=Column(Integer,ForeignKey("questions.id"))