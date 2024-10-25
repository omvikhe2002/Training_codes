from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Users
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

Users.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    
class UserCreateSchema(BaseModel):
    id:int
    name: str
    email: str
    password: str

@app.get("/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(Users).all()

@app.post("/users", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    u = Users(name=user.name, email=user.email, password=user.password)
    db.add(u)
    db.commit()
    db.refresh(u)  
    return u

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_update: UserCreateSchema, db: Session = Depends(get_db)):
    
    user = db.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = user_update.password
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)