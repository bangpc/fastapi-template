import jwt
import time

from functools import wraps
from pydantic import BaseModel
from typing import Optional, Callable, Any
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.configs import ConfigManager
from app.user.models import SIModel
from app.logs import LogHandler
from app.utils.status_code import StatusCode


# Decorator for authentication
class access_control:
    def __init__(
            self,
            superuser: bool = False,
            open: bool = False
        ):
        """_summary_

        Args:
            superuser (bool, optional): _description_. Defaults to False.
            open (bool, optional): _description_. Defaults to False.
        """        
        self.token = None
        self.request = None
        self.open = open
        self.superuser = superuser
        self.logger = LogHandler.get_logger("auth")
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.open:
                return func(*args, **kwargs)
            else:
                request = kwargs.get("request")
                if not request:
                    self.logger.error("Get None request")
                    raise HTTPException(
                        status_code=StatusCode.ERR_000001.value["http_code"],
                        detail=StatusCode.ERR_000001.value["detail"],
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                auth_str = request.headers.get("authorization")
                if auth_str is  None:
                    raise HTTPException(
                        status_code=StatusCode.ERR_000002.value["http_code"],
                        detail=StatusCode.ERR_000002.value["detail"],
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                auth_strs = auth_str.split(" ")
                if len(auth_strs) != 2:
                    self.logger.error("Wrong bearer token format")
                    raise HTTPException(
                        status_code=StatusCode.ERR_000003.value["http_code"],
                        detail=StatusCode.ERR_000003.value["detail"],
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                elif auth_strs[0] != "Bearer":
                    self.logger.error("Wrong bearer token format the format must be 'Bearer \{token\}'")
                    raise HTTPException(
                        status_code=StatusCode.ERR_000003.value["http_code"],
                        detail=StatusCode.ERR_000003.value["detail"],
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    token = auth_strs[1]
                    valid = self.verify(token)
                    if not valid["status"]:
                        raise HTTPException(
                            status_code=valid["http_code"],
                            detail=valid["detail"],
                            headers={"WWW-Authenticate": "Bearer"},
                        )
                    else:
                        return func(*args, **kwargs)
        return wrapper

    def verify(
            self, 
            token
        ):
        """_summary_

        Args:
            token (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            payload = jwt.decode(token, 
                                ConfigManager.config.core_configs.auth.secret_key, 
                                algorithms=[ConfigManager.config.core_configs.auth.algorithm])
            username: str = payload.get("sub")
            if username is None:
                self.logger.error("Username is None")
                return {
                    "status": False,
                    "http_code": StatusCode.ERR_000003.value["http_code"],
                    "detail": StatusCode.ERR_000003.value["detail"]
                }
            si = SIModel.find_one_si({"username": username})
            if (si["status"] or not si["status"]) and len(si["result"])==0:
                self.logger.error(f"Decoded username {username} but username does not exist")
                return {
                    "status": False,
                    "http_code": StatusCode.ERR_000003.value["http_code"],
                    "detail": StatusCode.ERR_000003.value["detail"]
                }
            if self.superuser and username != "aiss-admin":
                self.logger.error(f"Decoded username {username} but this endpoint required superuser")
                return {
                    "status": False,
                    "http_code": StatusCode.ERR_000004.value["http_code"],
                    "detail": StatusCode.ERR_000004.value["detail"]
                }
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                self.logger.error("Expired token")
                return {
                    "status": False,
                    "http_code": StatusCode.ERR_000005.value["http_code"],
                    "detail": StatusCode.ERR_000005.value["detail"]
                }
            return {
                "status": True,
                "username": username
            }
        except InvalidTokenError as e:
            self.logger(f"InvalidTokenError: {e}")
            return {
                "status": False,
                "http_code": StatusCode.ERR_000003.value["http_code"],
                "detail": StatusCode.ERR_000003.value["detail"]
            }