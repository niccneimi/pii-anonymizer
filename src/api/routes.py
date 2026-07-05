from fastapi import APIRouter, Response
from fastapi.concurrency import run_in_threadpool
import os
from typing import Optional

from .schemas import AnonymizeRequest, AnonymizeResponse
from src.detector.ensemble_detector import detect_pii, mask_text
from src.monitoring.logger import (
    log_model_usage, 
    log_processing_time, 
    get_model_name,
    get_request_id,
    log_error
)

router = APIRouter(prefix="/api")

@router.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize(request: AnonymizeRequest, response: Response):
    request_id = get_request_id()
    model_name = get_model_name(request.mode)
    
    try:
        log_model_usage(model_name, "anonymization", request_id, text_length=len(request.text))

        async with log_processing_time("pii_detection", request_id):
            entities = await run_in_threadpool(detect_pii, request.text, request.mode)

        async with log_processing_time("text_masking", request_id):
            result = await run_in_threadpool(mask_text, request.text, entities)

        response.headers["X-Model-Used"] = model_name
        response.headers["X-Entities-Found"] = str(len(entities))
        
        return AnonymizeResponse(anonymized_text=result)
        
    except Exception as e:
        log_error(e, request_id, operation="anonymization", mode=request.mode)
        raise


@router.get("/logs")
async def get_logs(lines: Optional[int] = 50, log_type: Optional[str] = "app"):
    try:
        log_file = f"logs/{log_type}.log"
        
        if not os.path.exists(log_file):
            return {"error": f"Log file {log_file} not found"}
        
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if lines > 0 else all_lines
            
        return {
            "log_type": log_type,
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "logs": [line.strip() for line in recent_lines]
        }
        
    except Exception as e:
        return {"error": f"Failed to read logs: {str(e)}"}


@router.get("/logs/stats")
async def get_log_stats():
    try:
        stats = {}
        
        for log_type in ["app", "errors"]:
            log_file = f"logs/{log_type}.log"
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    stats[log_type] = {
                        "file_exists": True,
                        "total_lines": len(lines),
                        "file_size_mb": os.path.getsize(log_file) / (1024 * 1024),
                        "last_modified": os.path.getmtime(log_file)
                    }
            else:
                stats[log_type] = {"file_exists": False}
        
        return stats
        
    except Exception as e:
        return {"error": f"Failed to get log stats: {str(e)}"}
