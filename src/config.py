import sys
sys.path.append("./")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

import json
from model_training_base.types.config import ModelTrainingBaseConfig

class CharacterModelTrainingServiceConfig(ModelTrainingBaseConfig): 
    def __init__(self, env = None):
        f = open("./Chisel-Global-Service-Configs/configs/globalServicePortMappings.json")
        self.__global_service_port_mappings = json.load(f)
        f.close()

        f = open("./configs/service.config.json")
        self.__service_config = json.load(f)
        f.close()

        super().__init__(self.__service_config)
        
        self.env = env or "development"
        self.service_name = self.__service_config["serviceName"]
        self.short_name = self.__service_config["shortName"]
        self.storageUrl = [x for x in self.__service_config["storage"] if x["env"] == self.env][0]
        self.temp_image_path = [x for x in self.__service_config["tempImagePath"] if x["env"] == self.env][0]
        self.service_address = [x for x in self.__service_config["serviceAddress"] if x["env"] == self.env][0]["url"]
        self.service_port_http = self.__global_service_port_mappings[self.service_name][self.env]["http"]
        self.service_port_https = self.__global_service_port_mappings[self.service_name][self.env]["https"]