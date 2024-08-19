import base64
import sys
sys.path.append("./")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

import gzip
import json

from config import CharacterModelTrainingServiceConfig
from model_training_base.controller.model_training_base_controller import ModelTrainingBaseController
from model_training_base.types.trainer_types import ReceivedTrainingData, TrainedModelFile

class CharacterModelTrainingController(ModelTrainingBaseController): 
    def __init__(self, config = None, background_tasks_interface = None, model_training_model = None):
        self.__config = config or CharacterModelTrainingServiceConfig()
        super().__init__(self.__config, background_tasks_interface, model_training_model)

    def upload_training_data(self, received_training_data):
        return super()._upload_training_data(ReceivedTrainingData(json.loads(received_training_data)))
    
    def start_and_train_model(self):
        return super()._start_and_train_model().json()
    
    def get_model_training_execution(self, execution_id):
        execution_json_dict = super()._get_model_training_execution(execution_id).json()
        if "modelPath" in execution_json_dict:
            del execution_json_dict["modelPath"]
        return execution_json_dict
    
    def get_latest_trained_model(self):
        return TrainedModelFile(super()._get_latest_trained_model())
    
    def get_trained_model_by_execution_id(self, execution_id):
        return TrainedModelFile(super()._get_trained_model_by_execution_id(execution_id))
        