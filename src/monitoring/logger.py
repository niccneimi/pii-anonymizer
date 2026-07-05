import loguru
import time
import uuid
from typing import Optional
from fastapi import Request, Response
from contextlib import asynccontextmanager

logger = loguru.logger

logger.remove()
logger.add(
    "logs/app.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {message}",
    enqueue=True
)
logger.add(
    "logs/errors.log",
    rotation="50 MB", 
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {extra[error_type]} | {message}",
    enqueue=True
)
logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {message}"
)

_request_context = {}

def get_request_id() -> str:
    return _request_context.get("request_id", str(uuid.uuid4()))

def set_request_context(request_id: str, **kwargs):
    _request_context.update({"request_id": request_id, **kwargs})

def clear_request_context():
    _request_context.clear()

def log_request_start(request: Request, request_id: str) -> None:
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("user-agent", "unknown")
    
    logger.info(
        f"Request started | {method} {url} | IP: {client_ip} | UA: {user_agent[:100]}",
        request_id=request_id
    )

def log_request_end(request: Request, response: Response, request_id: str, processing_time: float, model_used: Optional[str] = None) -> None:
    method = request.method
    url = str(request.url)
    status_code = response.status_code
    
    model_info = f" | Model: {model_used}" if model_used else ""
    
    logger.info(
        f"Request completed | {method} {url} | Status: {status_code} | Time: {processing_time:.3f}s{model_info}",
        request_id=request_id
    )

def log_error(error: Exception, request_id: str, **kwargs) -> None:
    error_type = type(error).__name__
    error_message = str(error)
    
    logger.error(
        f"Error occurred: {error_message}",
        request_id=request_id,
        error_type=error_type,
        **kwargs
    )

def log_model_usage(model_name: str, operation: str, request_id: str, **kwargs) -> None:
    logger.info(
        f"Model usage | {model_name} | Operation: {operation}",
        request_id=request_id,
        **kwargs
    )

@asynccontextmanager
async def log_processing_time(operation: str, request_id: str):
    start_time = time.time()
    try:
        yield
    finally:
        processing_time = time.time() - start_time
        logger.info(
            f"Processing time | {operation}: {processing_time:.3f}s",
            request_id=request_id
        )

def get_model_name(mode: str) -> str:
    mode_mapping = {
        "ensemble": "GLiNER + Regex Ensemble",
        "use_regex_only": "Regex Only",
        "use_gliner_only": "GLiNER Only"
    }
    return mode_mapping.get(mode, f"Unknown mode: {mode}")
