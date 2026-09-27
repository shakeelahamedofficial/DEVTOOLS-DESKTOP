"""
DevTools Desktop — HTTP Request Logic
"""

import time
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json

from PySide6.QtCore import QThread, Signal

@dataclass
class HttpRequest:
    method: str
    url: str
    headers: Dict[str, str]
    body: str

@dataclass
class HttpResponse:
    success: bool
    status_code: int = 0
    status_reason: str = ""
    headers: Dict[str, str] = None
    body: str = ""
    error_message: str = ""
    time_ms: int = 0
    size_bytes: int = 0

class HttpWorker(QThread):
    """Background worker for HTTP requests to prevent UI blocking."""
    
    finished = Signal(HttpResponse)
    
    def __init__(self, request: HttpRequest, timeout: int = 10, parent=None):
        super().__init__(parent)
        self.request = request
        self.timeout = timeout
        
    def run(self):
        req = self.request
        
        if not req.url.startswith("http://") and not req.url.startswith("https://"):
            req.url = "http://" + req.url
            
        data = None
        if req.body and req.method not in ["GET", "HEAD", "OPTIONS"]:
            data = req.body.encode("utf-8")
            
        urllib_req = urllib.request.Request(
            url=req.url,
            data=data,
            method=req.method
        )
        
        for k, v in req.headers.items():
            if k and v:
                urllib_req.add_header(k, v)
                
        # Handle cases where no user-agent is provided, add default so some APIs don't block
        if not any(k.lower() == 'user-agent' for k in req.headers.keys()):
            urllib_req.add_header('User-Agent', 'DevToolsDesktop/1.0')

        t0 = time.perf_counter()
        
        try:
            # We use urllib to minimize dependencies
            with urllib.request.urlopen(urllib_req, timeout=self.timeout) as response:
                time_ms = int((time.perf_counter() - t0) * 1000)
                
                status_code = response.getcode()
                status_reason = response.reason
                
                resp_headers = dict(response.info().items())
                
                # Only read body if not HEAD
                body_bytes = b""
                if req.method != "HEAD":
                    body_bytes = response.read()
                    
                size_bytes = len(body_bytes)
                
                # Try decoding
                try:
                    body_text = body_bytes.decode('utf-8')
                    # Try formatting as JSON if content-type says so
                    if 'application/json' in resp_headers.get('Content-Type', '').lower():
                        try:
                            parsed = json.loads(body_text)
                            body_text = json.dumps(parsed, indent=2, ensure_ascii=False)
                        except:
                            pass
                except UnicodeDecodeError:
                    body_text = f"[{size_bytes} bytes of binary data]"
                    
                res = HttpResponse(
                    success=True,
                    status_code=status_code,
                    status_reason=status_reason,
                    headers=resp_headers,
                    body=body_text,
                    time_ms=time_ms,
                    size_bytes=size_bytes
                )
                self.finished.emit(res)
                
        except urllib.error.HTTPError as e:
            time_ms = int((time.perf_counter() - t0) * 1000)
            resp_headers = dict(e.headers.items())
            
            body_bytes = b""
            if req.method != "HEAD":
                body_bytes = e.read()
            size_bytes = len(body_bytes)
            
            try:
                body_text = body_bytes.decode('utf-8')
                if 'application/json' in resp_headers.get('Content-Type', '').lower():
                        try:
                            parsed = json.loads(body_text)
                            body_text = json.dumps(parsed, indent=2, ensure_ascii=False)
                        except:
                            pass
            except UnicodeDecodeError:
                body_text = f"[{size_bytes} bytes of binary data]"
                
            res = HttpResponse(
                success=True, # HTTP errors are successful requests, just bad statuses
                status_code=e.code,
                status_reason=e.reason,
                headers=resp_headers,
                body=body_text,
                time_ms=time_ms,
                size_bytes=size_bytes
            )
            self.finished.emit(res)
            
        except urllib.error.URLError as e:
            # Network level error
            time_ms = int((time.perf_counter() - t0) * 1000)
            res = HttpResponse(
                success=False,
                error_message=f"Network Error: {e.reason}",
                time_ms=time_ms
            )
            self.finished.emit(res)
            
        except Exception as e:
            time_ms = int((time.perf_counter() - t0) * 1000)
            res = HttpResponse(
                success=False,
                error_message=f"Error: {str(e)}",
                time_ms=time_ms
            )
            self.finished.emit(res)
