from typing import Union, List, Type, Optional
from pydantic import BaseModel, Field

class SIRegister(BaseModel):
    si_id: str
    username: str
    user_group: str
    email: str
    password: str