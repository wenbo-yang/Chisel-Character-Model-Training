import sys
sys.path.append("./")
sys.path.append("./src")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

from src.config import CharacterModelTrainingServiceConfig
from src.controller.character_model_training_controller import CharacterModelTrainingController

config = CharacterModelTrainingServiceConfig("development")
def test_get_controller_from_src_module():
    controller = CharacterModelTrainingController(config)
    assert controller != None