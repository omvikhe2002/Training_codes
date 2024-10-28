from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "om": {
        "username": "om",
        "full_name": "Om Vikhe",
        "email": "om@example.com",
        "hashed_password": "1234",  
        "disabled": False,
    }
}
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["hashed_password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/profile")
async def read_profile(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": user["username"], "full_name": user["full_name"]}


if __name__=="__main__":
    import uvicorn
    uvicorn.run("Authentication:app", host="127.0.0.1", port=8001, reload=True)