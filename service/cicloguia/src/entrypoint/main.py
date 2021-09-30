from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return 200


@app.get("/items/{category}")
def read_item(category: str):
    return {"item_id": category}


@app.get("/images/{name}")
def read_image(name: str):
    return {"item_id": name}
