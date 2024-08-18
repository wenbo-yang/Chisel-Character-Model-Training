import sys

from fastapi import FastAPI, Response
from config import CharacterModelTrainingServiceConfig
from controller.character_model_training_controller import CharacterModelTrainingController
from model_training_base.types.trainer_types import TRAININGSTATUS
from utils.helper_functions import get_env_from_system_args

config = CharacterModelTrainingServiceConfig(get_env_from_system_args(sys.argv))
app = FastAPI()

@app.get("/healthcheck")
async def health_check():
    return "I am healthy!!!"

@app.post("/uploadTrainingData")
async def upload_training_data(received_training_data, response: Response):
    status = CharacterModelTrainingController(config).upload_training_data(received_training_data)
    if status == TRAININGSTATUS.CREATED: 
        response.status_code = status.HTTP_201_CREATED
    elif status == TRAININGSTATUS.NOCHANGE:
        response.status_code = 208 # no change

