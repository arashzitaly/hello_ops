from fastapi import FastAPI

app = FastAPI(title="hello_ops")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello(name: str):
    return {"message": f"hello {name}"}
