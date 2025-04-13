from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI(title="Docker Management System")

app.include_router(router, prefix="/docker")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=1243, reload=True)
