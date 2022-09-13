import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

msg = "Hola mundo!"

@app.get('/hola')
async def get_users():
    return msg


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
