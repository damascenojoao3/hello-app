from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
 return {"message": "Hello World"}
 return {"second message": "That's another message"}
