import sys

from fastapi import BackgroundTasks, status, FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
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

@app.get("/trainModel")
async def upload_training_data(background_tasks: BackgroundTasks):
    execution = CharacterModelTrainingController(config, background_tasks).start_and_train_model()
    execution_json = jsonable_encoder(execution)
    return JSONResponse(content=execution_json)

@app.get("/getModelTrainingExecution/{execution_id}")
async def get_model_training_status(execution_id: str):
    execution = CharacterModelTrainingController(config).get_model_training_execution(execution_id)
    execution_json = jsonable_encoder(execution)
    return JSONResponse(content=execution_json)

@app.get("/getLatestModel")
async def get_latest_trained_model():
    trained_model = CharacterModelTrainingController(config).get_latest_trained_model()
    return FileResponse(trained_model.file_path, media_type=trained_model.file_type, filename=trained_model.file_name)    

@app.get("/getTrainedModelByExecutionId/{execution_id}")
async def get_trained_model_by_execution_id(execution_id: str):
    trained_model = CharacterModelTrainingController(config).get_trained_model_by_execution_id(execution_id)
    return FileResponse(trained_model.file_path, media_type=trained_model.file_type, filename=trained_model.file_name)    
