from enum import Enum

class StatusCode(Enum):
    UNKNOWN_ERROR = {
        "http_code": 500,
        "detail": {
            "code": "000000",
            "message":"Some thing wrong in backend server please contact administrator"
        }
    }
    SUCCESS = {
        "http_code": 200,
        "detail":{
            "code": "SUCCESS",
            "message": "Success"
        }
    }
    ERR_000000 = {
        "http_code": 401,
        "detail": {
            "code": "000000",
            "message": "Unauthorized"
        }
    }
    ERR_000001 = {
        "http_code": 401,
        "detail": {
            "code": "000001",
            "message": "Could not find credentials"
        }
    }
    ERR_000002 = {
        "http_code": 401,
        "detail": {
            "code": "000002",
            "message": "Please provide authen token"
        }
    }
    ERR_000003 = {
        "http_code": 401,
        "detail": {
            "code": "000003",
            "message": "Invalid authentication credentials"
        }
    }
    ERR_000004 = {
        "http_code": 401,
        "detail": {
            "code": "000004",
            "message": "Unauthorized, this endpoint required superuser!"
        }
    }
    ERR_000005 = {
        "http_code": 401,
        "detail": {
            "code": "000005",
            "message": "Token expired"
        }
    }