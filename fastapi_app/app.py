import uvicorn
from fastapi import FastAPI


app = FastAPI()

msg = "Hola mundo!"

@app.get('/hola')
async def get_users():
    return msg


uvicorn.run(app, host='0.0.0.0', port=8000)
                                               
