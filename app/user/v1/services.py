from .models import SIModel
from passlib.context import CryptContext
from app.utils.status_code import StatusCode
from app.logs.log_handler import LogHandler
from app.auth.utils import get_password_hash
from app.utils.decorators.auto_tracing import auto_tracing

class UserService:
    def __init__(
            self,
            logger
        ):
        """_summary_

        Args:
            logger (_type_): _description_
        """        
        self.logger = logger

    @auto_tracing()
    def si_register(
            self,
            data: dict = None
        ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        
        try:
            hashed_password = get_password_hash(data["password"])
            si = SIModel.find_one_si({"username": data["username"]})
            if si["status"] and len(si["result"])!=0:
                self.logger.error(f"Username {data['username']} already exist")
                status = StatusCode.ITEM_EXIST_ERROR.value
                status["content"]["detail"] = f"Username {data['username']} already exist"
                return status
            SIModel.insert_one_si({
                "si_id": data["si_id"],
                "username": data["username"],
                "user_group": data["user_group"],
                "email": data["email"],
                "hashed_password": hashed_password
            })
            self.logger.success("Register success")
            status = StatusCode.SUCCESS.value
            status["content"]["detail"] = "Register success"
            return status

        except Exception as e:
            self.logger.error(e)
            status = StatusCode.UNKNOWN_ERROR.value
            status["content"]["detail"] = str(e)
            return status

    @auto_tracing()
    def si_delete(
            self,
            username: str = None
        ):
        """_summary_

        Args:
            username (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        
        try:
            si = SIModel.find_one_si({"username": username})
            if not si["status"]:
                self.logger.error(f"Username {username} does not existed")
                status = StatusCode.ITEM_NOT_FOUND_ERROR.value
                status["content"]["detail"] = f"Username {username} does not existed"
                return status
            result =  SIModel.delete_one_si({"username": username})
            if not result["status"]:
                self.logger.error(result['error'])
                status = StatusCode.UNKNOWN_ERROR.value
                status["content"]["detail"] = result["error"]
                return status
            self.logger.success(f"Delete user {username} success")
            status = StatusCode.SUCCESS.value
            status["content"]["detail"] = f"Delete user {username} success"
            return  status
        except Exception as e:
            self.logger.error(e)
            status = StatusCode.UNKNOWN_ERROR.value
            status["content"]["detail"] = str(e)
            return status