from fastapi import FastAPI
from api.routes.chat_routes import router

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Omnichannel Accelerator Running"}

app.include_router(router)
