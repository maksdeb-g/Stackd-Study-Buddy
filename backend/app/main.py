from fastapi import FastAPI

app = FastAPI(
    title="Stackd - Study Buddy API",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Stackd API"}