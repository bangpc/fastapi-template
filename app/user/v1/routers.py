import requests
import time
import cv2
import json
from typing import List
from fastapi_utils.cbv import cbv

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .schemas import SIRegister
from .services import UserService
from app.utils.status_code import StatusCode
from app.logs import LogHandler
from app.auth.permissions import access_control
from app.utils.decorators.auto_tracing import auto_tracing

router = APIRouter(prefix="/users", tags= ["Users Management"])

@cbv(router)
class UserRouter:
    logger = LogHandler.get_logger("si_management")
    user_service = UserService(logger)

    @router.post("/si/register")
    @access_control(open=True)
    @auto_tracing()
    def si_register(
            self,
            request: Request, 
            data: SIRegister
        ):
        """_summary_

        Args:
            request (Request): _description_
            data (SIRegister): _description_

        Returns:
            _type_: _description_
        """        
        self.logger.info("====SI Register====")
        result = self.user_service.si_register(data.dict())
        return JSONResponse(
            status_code = result["http_code"],
            content = result["content"]
        )

    @router.post("/si/delete/{username}")
    @access_control(superuser=True)
    @auto_tracing()
    def si_delete(
            username: str
        ):
        """_summary_

        Args:
            username (str): _description_

        Returns:
            _type_: _description_
        """        
        logger.info("=================SI Delete================")
        result = si_delete_svc(username)
        print(result)
        return JSONResponse(
            status_code = result["http_code"],
            content = result["content"]
        )