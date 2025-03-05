from app.logs import setup_logger, LogHandler
from app.db import initialize_mongodb
import time
import os
import redis
from app.configs import ConfigManager, load_configs
# from app.utils.instrumentation import Tracer
from app.storage.s3_client import S3Client

setup_logger(log_folder="app/logs/logs_data")
setup_logger(log_folder="app/logs/logs_data", logger_name="auth")
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
