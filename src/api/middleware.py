import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.monitoring.logger import (
    log_request_start, 
    log_request_end, 
    log_error,
    set_request_context,
    clear_request_context,
)

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        set_request_context(request_id)
        
        try:
            log_request_start(request, request_id)
            start_time = time.time()

            response = await call_next(request)

            processing_time = time.time() - start_time
            model_used = response.headers.get("X-Model-Used")
            log_request_end(request, response, request_id, processing_time, model_used)
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time if 'start_time' in locals() else 0
            log_error(e, request_id, processing_time=processing_time)
            raise     
        finally:
            clear_request_context()