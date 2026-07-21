import time
import uuid
import re
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

EXCLUDED_PATHS = [
    r"^/metrics$",
    r"^/health$",
    r"^/ready$",
    r"^/live$",
    r"^/favicon\.ico$",
]

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_patterns = [re.compile(pattern) for pattern in EXCLUDED_PATHS]
    
    def _should_log(self, path: str) -> bool:
        return not any(pattern.match(path) for pattern in self.excluded_patterns)
    
    async def dispatch(self, request: Request, call_next):
        should_log = self._should_log(request.url.path)
        
        request_id = str(uuid.uuid4()) if should_log else None
        
        if should_log:
            set_request_context(request_id)
        
        try:
            if should_log:
                log_request_start(request, request_id)
                start_time = time.time()
            else:
                start_time = time.time()
            
            response = await call_next(request)
            
            if should_log:
                processing_time = time.time() - start_time
                model_used = response.headers.get("X-Model-Used")
                log_request_end(request, response, request_id, processing_time, model_used)
                response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time if 'start_time' in locals() else 0
            if should_log:
                log_error(e, request_id, processing_time=processing_time)
            raise
        finally:
            if should_log:
                clear_request_context()