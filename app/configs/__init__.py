# import yaml
# import json
# import pathlib
# import sys
# import os
# import requests

# from omegaconf import OmegaConf
# from vss_controller.logs.log_handler import LogHandler

# class ConfigManager:
#     @classmethod
#     def __init__(self, config_folder="configs"):
#         self.logger = LogHandler.get_logger("general")
#         if not os.path.exists(config_folder):
#             raise Exception(f"Config folder {config_folder} does not exist")
        
#         elif not config_folder.split("/")[-2] != "configs":
#             raise Exception(f"Path to configs folder must be absolute path or "\
#                              "relative path but it must contain 'configs'." \
#                              "For example: '/media/data/vss-management-server/vss_management_server/configs' "\
#                              "or './configs/'")

#         self.accepted_file_extensions = ["yaml", "json"]
#         self.config = None

#         self.cfg_files = []
#         for path, subdirs, files in os.walk(config_folder):
#             for f in files:
#                 if self.check_valid_config(f):
#                     self.cfg_files.append(os.path.join(path, f))

#     @classmethod
#     def check_valid_config(self, cfg_path):
#         for e in self.accepted_file_extensions:
#             if e in cfg_path:
#                 return True
#         return False

#     @classmethod
#     def load_configs_from_local(self):
#         try:
#             cfgs = []
#             for cfg in self.cfg_files:
#                 if cfg.split("/")[-2] != "configs":
#                     cfgs.append(
#                         OmegaConf.create({
#                             cfg.split("/")[-2] : {
#                                 cfg.split("/")[-1].split(".")[0] : OmegaConf.load(cfg)
#                             }
#                         })
#                     )
#                 else:
#                     cfgs.append(OmegaConf.load(cfg))
#             config = OmegaConf.merge(*cfgs)
#             self.config = config
#             self.logger.success("Load config from local success!")
#         except Exception as e:
#             raise Exception(f"Load config error: {e}")
    
#     @classmethod
#     def load_configs_from_management_server(self):
#         ms_host = self.config["management_server"]["host"]
#         ms_port = self.config["management_server"]["port"]

#         try:
#             self.logger.info("Trying to load configs from management server")

#             # Load config for database/message-queue/storage
#             self.logger.info("______________________Trying to load core configs______________________")
#             for core, core_config in self.config['core_configs'].items():
#                 url = f"http://{ms_host}:{ms_port}" \
#                       f"/core-component/{core}/{core_config['type']}/{core_config['tag']}"
#                 response = requests.get(url)
#                 if response.status_code == 200:
#                     if response.json()["detail"] is not None:
#                         self.config["core_configs"][core] = response.json()["detail"]
#                         self.logger.success(f"Update config success for core {core} from management server")
#                     else:
#                         self.logger.warning(f"No config for {core} found from management server. " \
#                                              "Use default config instead!") 
#                 else:
#                     self.logger.warning(f"Can not load config from management server due to following error {response.text}. " \
#                                          "Use default config instead!")

#             # Load config for service_config
#             self.logger.info("______________________Trying to load service configs____________________")
#             for service, service_config in self.config["service_configs"].items():
#                 url = f"http://{ms_host}:{ms_port}" \
#                       f"/vss-controller/solution-config/{service_config['solution']}"
#                 response = requests.get(url)
#                 if response.status_code == 200:
#                     if response.json()["detail"] is not None:
#                         self.config["service_configs"][service] = response.json()["detail"]
#                         self.logger.success(f"Update config success for service {service} from management server")
#                     else:
#                         self.logger.warning(f"No config for {service} found from management server. " \
#                                              "Use default config instead!") 
#                 else:
#                     self.logger.warning(f"Can not load config from management server due to following error {response.text}. " \
#                                          "Use default config instead!")

#             # Load config for triton config
#             self.logger.info("______________________Trying to load triton configs____________________")
#             for model, triton_config in self.config["triton_configs"].items():
#                 url = f"http://{ms_host}:{ms_port}" \
#                       f"/vss-controller/triton-config/{triton_config['model_name']}"
#                 response = requests.get(url)
#                 if response.status_code == 200:
#                     if response.json()["detail"] is not None:
#                         self.config["triton_configs"][model] = response.json()["detail"]
#                         self.logger.success(f"Update config success for triton config of {model} model from management server")
#                     else:
#                         self.logger.warning(f"No triton config for {model} model found from management server. " \
#                                              "Use default config instead!") 
#                 else:
#                     self.logger.warning(f"Can not load config from management server due to following error {response.text}. " \
#                                          "Use default config instead!")
            
#         except Exception as e:
#             self.logger.warning(f"Can not load config from management server due to following error {e}. " \
#                                  "Use default config instead!")


from .config_handler import ConfigManager, load_configs
