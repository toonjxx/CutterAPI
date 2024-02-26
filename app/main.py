from fastapi import FastAPI
import uvicorn
from routers import device_control

app = FastAPI()

app.include_router(device_control.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
   
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)