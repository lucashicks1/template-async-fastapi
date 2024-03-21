from fastapi import FastAPI


app = FastAPI()

@app.get("/test")
def health_check():
    return "test"
