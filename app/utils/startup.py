from app.logs import setup_logger, LogHandler
from app.db import initialize_mongodb
import time
import os
import redis
from app.configs import ConfigManager, load_configs
# from app.utils.instrumentation import Tracer
from app.storage.s3_client import S3Client

setup_logger(log_folder="app/logs/logs_data")
setup_logger(log_folder="app/logs/logs_data", logger_name="smh")
setup_logger(log_folder="app/logs/logs_data",  logger_name="si_management")
setup_logger(log_folder="app/logs/logs_data",  logger_name="status_management")
setup_logger(log_folder="app/logs/logs_data",  logger_name="plant_heatmap")
setup_logger(log_folder="app/logs/logs_data",  logger_name="auth")
setup_logger(log_folder="app/logs/logs_data",  logger_name="camera_management")
setup_logger(log_folder="app/logs/logs_data",  logger_name="license_management")
setup_logger(log_folder="app/logs/logs_data",  logger_name="face_management")
setup_logger(log_folder="app/logs/logs_data",  logger_name="heatmap")
setup_logger(log_folder="app/logs/logs_data",  logger_name="image_captioning")
general_logger = LogHandler.get_logger("general")
general_logger.success("Initialize log success!")


general_logger.info("Starting load configs")
load_configs("app/configs")

general_logger.info("Starting initialize mongodb")
db_config = ConfigManager.config.core_configs.database
initialize_mongodb(db_config.host,
                    db_config.port,
                    db_config.username,
                    db_config.password,
                    db_config.auth)

# tracer = Tracer()
# Tracer.setup_tracer()
# print(Tracer.tracer)

# Read aes_key and hmac_key
aes_key_file = ConfigManager.config.core_configs.crypt_keys.aes
hmac_key_file = ConfigManager.config.core_configs.crypt_keys.hmac
with open(aes_key_file, "rb") as file:
    aes_key = file.read()
    file.close()
with open(hmac_key_file, "rb") as file:
    hmac_key = file.read()
    file.close()

#=== S3 storage MinIO

# general_logger.info(f"Config: {ConfigManager.config}")
# try:
s3_conf = ConfigManager.config.core_configs.storage
s3_client = S3Client(
                aws_access_key_id=s3_conf.access_key_id,
                aws_secret_access_key=s3_conf.secret_access_key,
                endpoint_url=s3_conf.s3_endpoint
            )
S3_BUCKET = s3_conf.s3_bucket
for bucket in S3_BUCKET:
    if not s3_client.is_bucket_exist(bucket_name=bucket):
        s3_client.create_bucket(bucket_name=bucket)
general_logger.info("=== Done S3 client init\n")

# # except Exception as se:
#     general_logger.error(f"{se}") 

trace_endpoint = ConfigManager.config.servers.trace.endpoint
trace_service_name = ConfigManager.config.servers.trace.service_name


#=== Redis client
redis_conf = ConfigManager.config.servers.redis
# redis_conn = redis.Redis(host=redis_conf.REDIS_HOST, port=redis_conf.REDIS_PORT, db=redis_conf.CELERY_BROKER_DB, password=redis_conf.REDIS_PASS)
# redis_img = redis.Redis(host=redis_conf.REDIS_HOST, port=redis_conf.REDIS_PORT, db=3, password=redis_conf.REDIS_PASS)
# redis_parking = redis.Redis(host=redis_conf.REDIS_HOST, port=redis_conf.REDIS_PORT, db=4, password=redis_conf.REDIS_PASS)

from .redis import Redis
def load_redis():
    Redis(redis_conf.REDIS_HOST, redis_conf.REDIS_PORT, redis_conf.CELERY_BROKER_DB, redis_conf.REDIS_PASS)

load_redis()