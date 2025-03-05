import requests
import time
import cv2
import json
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from .schemas import LoginRequest
from .services import AuthService
from app.utils.status_code import StatusCode
from app.logs import LogHandler
from .permissions import access_control
from app.utils.decorators.auto_tracing import auto_tracing

router = APIRouter(prefix="/auth", tags= ["Authentication"])

@cbv(router)
class AuthRouter:
    logger = LogHandler.get_logger("auth")
    auth_service = AuthService(logger)

    @router.post("/auth/login")
    @access_control(open=True)
    @auto_tracing()
    def si_login(
            self,
            request: Request,
            login_request: LoginRequest
        ):
        self.logger.info("====Login====")
        result = self.auth_service.si_login(login_request.model_dump_json())
        self.logger.info(f"Login result: {result}")
        return JSONResponse(
            status_code = result["http_code"],
            content = result["content"],
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @router.get("/auth/check-login")
    @access_control()
    @auto_tracing()
    def si_check_login(
            self,
            request: Request
        ):
        status = StatusCode.SUCCESS.value
        status["content"]["detail"] = "You are logged in"
        return JSONResponse(
            status_code = status["http_code"],
            content = status["content"],
            headers={"WWW-Authenticate": "Bearer"}
        )