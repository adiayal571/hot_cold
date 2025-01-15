from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


LAST = ""

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/setLast/{last}")
def set_last(last):
    global LAST
    LAST = last


@app.get("/getLast")
def get_last():

    return {"last": LAST}