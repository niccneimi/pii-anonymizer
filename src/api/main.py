from fastapi import FastAPI
from .routes import router
from .middleware import LoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="PII Anonymizer API")
instrumentator = Instrumentator(
    should_instrument_requests_inprogress=True,
    inprogress_name="http_requests_in_progress",
    inprogress_labels=True
)

instrumentator.instrument(app).expose(app)

app.add_middleware(LoggingMiddleware)
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pii-anonymizer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
