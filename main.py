from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI(title="Docker Management System")

app.include_router(router, prefix="/docker")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
