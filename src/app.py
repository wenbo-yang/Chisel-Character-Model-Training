import sys

from fastapi import status, FastAPI, Request, Response
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
async def upload_training_data(request: Request, response: Response):
    training_status = CharacterModelTrainingController(config).upload_training_data(await request.json())
    if training_status == TRAININGSTATUS.CREATED: 
        response.status_code = status.HTTP_201_CREATED
    elif training_status == TRAININGSTATUS.NOCHANGE:
        response.status_code = status.HTTP_208_ALREADY_REPORTED

