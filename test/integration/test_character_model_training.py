import sys
import time

sys.path.append("./")
sys.path.append("./src")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")
sys.path.append("./Chisel-Model-Training-Base/test")

import pytest
import requests
import json

from config import CharacterModelTrainingServiceConfig
from fastapi import status
from test_helpers.test_helper_functions import load_and_compress_neural_net_training_images
from model_training_base.types.trainer_types import COMPRESSIONTYPE, TRAININGDATATYPE, TRAININGSTATUS
from model_training_base.dao.model_local_storage_dao import ModelLocalStorageDao
from model_training_base.dao.training_data_local_storage_dao import TrainingDataLocalStorageDao
from model_training_base.utils.data_piper import DataPiper

service_url = "https://127.0.0.1:3001"

http_request = requests.Session()
http_request.verify = False

config = CharacterModelTrainingServiceConfig("development")
model_local_storage_dao = ModelLocalStorageDao(config)
training_data_local_storage_dao = TrainingDataLocalStorageDao(config)
data_piper = DataPiper(config)

@pytest.fixture(autouse=True)
def run_after_tests():
    yield
    model_local_storage_dao.delete_all_training_executions()
    training_data_local_storage_dao.delete_all_training_data()

def test_get_health_check(): 
    health_check_url = service_url + "/healthcheck"
    response = http_request.get(health_check_url)

    print(response.json())
    assert response.status_code == 200
    assert response.json() == "I am healthy!!!"

def test_upload_new_training_data_should_return_201_created():
    upload_data_url = service_url + "/uploadTrainingData"
    training_data = load_and_compress_neural_net_training_images("./test/integration/test_data")
    
    for td in training_data:
        td["dataType"] = TRAININGDATATYPE.PNG
        td["compression"] = COMPRESSIONTYPE.GZIP
        response = http_request.post(upload_data_url, json=json.dumps(td))
        assert response.status_code == status.HTTP_201_CREATED

def test_upload_existing_training_data_should_return_208_created():
    upload_data_url = service_url + "/uploadTrainingData"
    training_data = load_and_compress_neural_net_training_images("./test/integration/test_data")
    
    for td in training_data:
        td["dataType"] = TRAININGDATATYPE.PNG
        td["compression"] = COMPRESSIONTYPE.GZIP
        response = http_request.post(upload_data_url, json=json.dumps(td))
        assert response.status_code == status.HTTP_201_CREATED 

        response = http_request.post(upload_data_url, json=json.dumps(td))
        assert response.status_code == status.HTTP_208_ALREADY_REPORTED 

def test_start_and_training_data_should_return_inprogress_training():
    test_upload_new_training_data_should_return_201_created()

    train_model_url = service_url + "/trainModel"
    response = http_request.get(train_model_url)
    execution = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert execution["executionId"] != None
    assert execution["status"] == TRAININGSTATUS.INPROGRESS
    assert execution["updated"] != None
    assert ("modelPath" not in execution) or (execution["modelPath"] == None)
    
def test_train_model_and_poll_status_should_return_finished_execution_eventually():
    test_upload_new_training_data_should_return_201_created()
    train_model_url = service_url + "/trainModel"
    execution = json.loads(http_request.get(train_model_url).content)

    get_model_execution_url = service_url + "/getModelTrainingExecution/" + execution["executionId"]
    count = 0
    while count < 100 and (json.loads(http_request.get(get_model_execution_url).content)["status"] != TRAININGSTATUS.FINISHED):
        time.sleep(0.6)
        count +=1

    execution = json.loads(http_request.get(get_model_execution_url).content)
    assert execution["status"] == TRAININGSTATUS.FINISHED
    assert ("modelPath" not in execution) or (execution["modelPath"] == None)
    assert count < 100

    get_latest_model_url = service_url + "/getLatestModel"
    latest_model_response = http_request.get(get_latest_model_url)

    assert latest_model_response.status_code == status.HTTP_200_OK
    assert latest_model_response.content != None
    
    get_trained_model_by_execution_id_url = service_url + "/getTrainedModelByExecutionId/" + execution["executionId"]
    model_by_execution_id_response = http_request.get(get_trained_model_by_execution_id_url)

    assert model_by_execution_id_response.status_code == status.HTTP_200_OK
    assert model_by_execution_id_response.content != None
    assert model_by_execution_id_response.content == latest_model_response.content

    
            


    
