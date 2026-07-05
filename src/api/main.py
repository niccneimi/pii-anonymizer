from fastapi import FastAPI
from .routes import router
from .middleware import LoggingMiddleware

app = FastAPI(title="PII Anonymizer API")

app.add_middleware(LoggingMiddleware)
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pii-anonymizer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
