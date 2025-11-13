from fastapi import FastAPI

app = FastAPI()

app.get("/")
def main():
    print("Hello world!")
    return "Hello world!"