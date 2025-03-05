import jwt
import time
import functools

from pydantic import BaseModel
from typing import Optional, Callable, Any
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.configs import ConfigManager
from app.utils.decorators.auto_tracing import auto_tracing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auto_tracing()
def verify_password(
        plain_password, 
        hashed_password
    ):
    """Function that verify plain password

    Args:
        plain_password (string): plain password taken from user
        hashed_password (string): hased password by the system

    Returns:
        bool: Return True or False
    """    
    return pwd_context.verify(plain_password, hashed_password)

@auto_tracing()
def get_password_hash(
        password
    ):
    return pwd_context.hash(password)

@auto_tracing()
def create_access_token(
        data: dict
    ):
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        _type_: _description_
    """    
    expires_delta  = timedelta(seconds=ConfigManager.config.core_configs.auth.expire_seconds)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
                      to_encode,
                      ConfigManager.config.core_configs.auth.secret_key,
                      algorithm=ConfigManager.config.core_configs.auth.algorithm
                  )
    return encoded_jwt

@auto_tracing()
def check_token(token):
    try:
        payload = jwt.decode(token, 
                             ConfigManager.config.core_configs.auth.secret_key, 
                             algorithms=[ConfigManager.config.core_configs.auth.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return {
                "status": False,
                "detail": "Could not validate credential"
            }
        return {
            "status": True,
            "username": username
        }
    except InvalidTokenError:
        return {
            "status": False,
            "detail": "Could not validate credential"
        }