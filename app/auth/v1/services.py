from .schemas import SILoginResponse
from app.user.models import SIModel
from passlib.context import CryptContext
from app.utils.status_code import StatusCode
from app.logs.log_handler import LogHandler
from .utils import get_password_hash, create_access_token
from app.utils.decorators.auto_tracing import auto_tracing

class AuthService:
    def __init__(
            self,
            logger
        ):
        self.logger = logger

    @auto_tracing()
    def si_login(
            self,
            si_data
        ):
        try:
            si = SIModel.find_one_si({"username": si_data["username"]})
            if (si["status"] or not si["status"]) and len(si["result"])==0:
                self.logger.error(f"Username {si_data['username']} does not exist")
                status = StatusCode.ITEM_NOT_FOUND_ERROR.value
                status["content"]["detail"] = f"Username {si_data['username']} does not exist"
                return status
            elif not si["status"]:
                self.logger.error(f"Something wrong with database: {si['error']}")
                status = StatusCode.UNKNOWN_ERROR.value
                status["content"]["detail"] = f"Something wrong please contact AISS administrator"
                return status
            access_token  = create_access_token({"sub": si["result"]["username"]})
            
            self.logger.success("Login success")
            status = StatusCode.SUCCESS.value
            si_login_response = SILoginResponse(access_token=access_token)
            status["content"]["detail"] = si_login_response.dict()
            return status
        
        except Exception as e:
            self.logger.error(e)
            status = StatusCode.UNKNOWN_ERROR.value
            status["content"]["detail"] = str(e)
            return status

    # def validate_login_svc(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    #     general_logger.info(f"token: {token}")
    #     try:
    #         validate_token_result = check_token(token)
    #         if not validate_token_result["status"]:
    #             status = StatusCode.UNAUTHORIZED.value
    #             status["content"]["detail"] = validate_token_result["detail"]
    #             return status
    #         else:
    #             si = SIModel.find_one_si({"username": validate_token_result["username"]})
    #             if (si["status"] or not si["status"]) and len(si["result"])==0:
    #                 general_logger.error(f"Username {si_data['username']} does not exist")
    #                 status = StatusCode.UNAUTHORIZED.value
    #                 status["content"]["detail"] = f"Fail to validate credential for user {si_data['username']}"
    #                 return status
    #             elif not si["status"]:
    #                 general_logger.error(f"Something wrong with database: {si['error']}")
    #                 status = StatusCode.UNKNOWN_ERROR.value
    #                 status["content"]["detail"] = f"Something wrong please contact AISS  administrator"
    #                 return status
    #             else:
    #                 general_logger.success("Validate credential success")
    #                 status = StatusCode.SUCCESS.value
    #                 status["content"]["detail"] = "Validate credential success"
    #                 return status
    #     except Exception as e:
    #         general_logger.error(e)
    #         status = StatusCode.UNKNOWN_ERROR.value
    #         status["content"]["detail"] = str(e)
    #         return status