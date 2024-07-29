from subprocess import Popen
from fastapi import FastAPI
import uvicorn
import ssl

app = FastAPI()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("./certs/cert.crt", keyfile="./certs/key.pem")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 3001, ssl_keyfile="./certs/key.pem", ssl_certfile="./certs/cert.crt")
