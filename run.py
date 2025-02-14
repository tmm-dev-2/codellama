from fastapi import FastAPI
from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7865, reload=True)
