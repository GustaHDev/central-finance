from fastapi import FastAPI

app = FastAPI(title="Central finance", version="0.1.0")

@app.get("/")
def root():
    return { "status": "Ok", "message": "Welcome to Central finance API" }