from fastapi import FastAPI,Depends, HTTPException
from typing import Annotated
from model import ChoiceBase, QuestionBase
from database import engine,localSession
from sqlalchemy.orm import Session
import db_models


app=FastAPI()

db_models.base.metadata.create_all(bind=engine)

def get_db():
    db=localSession()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
@app.get("/")
async def root():
    return {"message":"hi"}

@app.post("/questions/")
async def create_questions(question: QuestionBase,db=db_dependency):
    db_question=models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice=models.Choices(choice_text=choice.choice_text,is_correct=choice.is_correct)
        db.add(db_choice)
    db.commit()