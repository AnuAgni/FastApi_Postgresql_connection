from fastapi import FastAPI,Depends, HTTPException
from typing import Annotated,List
from pydantic import BaseModel
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import models


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text:str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text:str
    choices: List[ChoiceBase]

def get_db():
    db=localSession()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@app.post("/questions/")
async def create_questions(question: QuestionBase,db=db_dependency):
    db_question=models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice=models.Choices(choice_text=choices.choice_text,is_correct=choices.is_correct,question_id=db_question.id)
        db.add(db_choice)
    db.commit()