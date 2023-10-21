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
    questions_text:str
    choices: List[ChoiceBase]

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#db_dependency=Annotated[Session, Depends(get_db)]
@app.get("/questions/{question_id}")
async def read_question(question_id: int,db: Session=Depends(get_db)):
    result = db.query(models.Questions).filter(models.Questions.id==question_id).first()
    if not result:
        raise HTTPException(status_code=404,details='Question not found')
    return result
@app.get("/choices/{question_id}")
async def read_choices(question_id: int,db:Session=Depends(get_db)):
        result=db.query(models.Choices).filter(models.Choices.question_id==question_id).all()
        if not result:
            raise HTTPException(status_code=404,details='Choices not found')
        return result

@app.post("/questions/")
async def create_questions(question: QuestionBase,db:Session=Depends(get_db)):
    db_question=models.Questions(questions_text=question.questions_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice=models.Choices(choice_text=choice.choice_text,is_correct=choice.is_correct,question_id=db_question.id)
        db.add(db_choice)
    db.commit()