import sys
sys.path.append("./")
sys.path.append("./src")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

from src.config import CharacterModelTrainingServiceConfig
from src.controller.character_model_training_controller import CharacterModelTrainingController

class FakeBackgroundTasks: 
    def add_task(self, function, arg):
        self.__function = function
        self.__arg = arg

    def run(self):
        self.__function(self.__arg)

config = CharacterModelTrainingServiceConfig("development")

def test_get_controller_from_submodule():
    controller = CharacterModelTrainingController(FakeBackgroundTasks(), config)
    assert controller != None