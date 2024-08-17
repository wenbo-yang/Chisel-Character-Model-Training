
import sys
sys.path.append("./")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

from src.config import CharacterModelTrainingServiceConfig
from model_training_base.controller.model_training_base_controller import ModelTrainingBaseController

class FakeBackgroundTasks: 
    def add_task(self, function, arg):
        self.__function = function
        self.__arg = arg

    def run(self):
        self.__function(self.__arg)


config = CharacterModelTrainingServiceConfig("development")

def test_get_controller_from_submodule():
    controller = ModelTrainingBaseController(config, FakeBackgroundTasks())
    assert controller != None