from enum import Enum

class StatusCode(Enum):
    UNKNOWN_ERROR = {
        "http_code": 500,
        "content": {
            "code": "ERR_UNKNOWN",
            "description":"Some thing wrong in backend server please contact administrator"
        }
    }
    SUCCESS = {
        "http_code": 200,
        "content":{
            "code": "SUCCESS",
            "description": "Success"
        }
    }
    
    INSERT_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00001",
            "description": "Error when insert or update cam"
        }
    }
    DB_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00002",
            "description": "Insert record into database error"
        }
    }
    # OBJECT_EXIST_ERROR = {
    #     "http_code": 400,
    #     "content": {
    #         "code": "ERR_00002",
    #         "description": "Object existed"
    #     }
    # }
    FIND_ITEM_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00003",
            "description": "Find item in database error"
        }
    }
    ITEM_NOT_FOUND_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00004",
            "description": "Does not found any item in database"
        }
    }
    INSTANCE_NOT_FOUND_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00005",
            "description": "Instance not found"
        }
    }
    NOT_SUCCESS_ALL = {
        "http_code": 200,
        "content": {
            "code": "AISS_00006",
            "description": "Not Success All"
        }
    }
    NOT_SUCCESS = {
        "http_code": 400,
        "content": {
            "code": "AISS_00007",
            "description": "Not Success"
        }
    }
    RECEIVED = {
        "http_code": 200,
        "content":{
            "code": "AISS_00008",
            "description": "Received"
        }
    }
    ITEM_EXIST_ERROR = {
        "http_code": 400,
        "content": {
            "code": "AISS_00009",
            "description": "Item existed in database"
        }
    }

    UNAUTHORIZED =  {
        "http_code": 401,
        "content": {
            "code": "AISS_00010",
            "description": "Unauthorized"
        }
    }

class StatusCodeV3(Enum):
    UNKNOWN_ERROR = {
        "http_code": 500,
        "content": {
            "code": "00001",
            "description":"Some thing wrong in backend server please contact administrator"
        }
    }
    SUCCESS = {
        "http_code": 200,
        "content":{
            "code": "00002",
            "description": "Success"
        }
    }
    
    INSERT_ERROR = {
        "http_code": 400,
        "content": {
            "code": "00003",
            "description": "Error when insert or update cam"
        }
    }
    DB_ERROR = {
        "http_code": 400,
        "content": {
            "code": "00004",
            "description": "Insert record into database error"
        }
    }

    FIND_ITEM_ERROR = {
        "http_code": 400,
        "content": {
            "code": "00005",
            "description": "Find item in database error"
        }
    }
    ITEM_NOT_FOUND_ERROR = {
        "http_code": 400,
        "content": {
            "code": "00006",
            "description": "Does not found any item in database"
        }
    }
    INSTANCE_NOT_FOUND_ERROR = {
        "http_code": 400,
        "content": {
            "code": "00007",
            "description": "Instance not found"
        }
    }
    NOT_SUCCESS_ALL = {
        "http_code": 200,
        "content": {
            "code": "00008",
            "description": "Not Success All"
        }
    }
    NOT_SUCCESS = {
        "http_code": 400,
        "content": {
            "code": "00009",
            "description": "Not Success"
        }
    }
    RECEIVED = {
        "http_code": 200,
        "content":{
            "code": "00010",
            "description": "Received"
        }
    }




class FaceRegisterCode(Enum):
    NOT_VALID = 10001
    TOO_LARGE = 10002
    NO_FACE = 10003
    MANY_FACE = 10004
    FAIL_PULL_IMAGE = 10005 
    DARK = 10006
    LIGHT = 10007
    BLURRY = 10008
    GRAYSCALE = 10009
    ANGLE = 10010
    SIMILARITY = 10011
    VALID = 10099