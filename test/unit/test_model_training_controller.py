
import sys
sys.path.append("./")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")

from model_training_base.controller.model_training_controller import ModelTrainingController

class FakeConfig:
    def __init__(self):
        self.env = "development"
        self.storage_url = "some_storage_url"

def test_get_controller_from_submodule():
    controller = ModelTrainingController(FakeConfig())
    assert controller != None