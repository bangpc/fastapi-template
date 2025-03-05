import json
import base64

from urllib.parse import urlparse
from urllib.parse import quote
from fastapi import Request
from app.utils.decorators.auto_tracing import auto_tracing

@auto_tracing()
def get_client_info(
        request: Request
    ):
    """_summary_

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """    
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host
    user_agent = request.headers.get('user-agent')
    return {"client_ip": client_ip, "user_agent": user_agent}

@auto_tracing()
def encode_dict_to_base64(data):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """  
    json_data = json.dumps(data)
    json_bytes = json_data.encode('utf-8')
    base64_bytes = base64.b64encode(json_bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

@auto_tracing()
def decode_base64_to_dict(base64_string):
    """_summary_

    Args:
        base64_string (_type_): _description_

    Returns:
        _type_: _description_
    """    
    base64_bytes = base64.b64decode(base64_string)
    json_data = base64_bytes.decode('utf-8')
    data = json.loads(json_data)
    return data
