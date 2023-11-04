import logging
from fastapi import Request
from datetime import datetime

# Create a logger instance for request logging
request_logger = logging.getLogger("request_logger")

async def request_logging_middleware(request: Request, call_next):
    """
    Middleware to log request details.
    """
    log_entry = {
        "timestamp": datetime.now(),
        "method": request.method,
        "url": request.url.path,
    }
    request_logger.info(log_entry)
    response = await call_next(request)
    return response
