import sys
sys.path.append("./")
sys.path.append("./src")
sys.path.append("./Chisel-Model-Training-Base")
sys.path.append("./Chisel-Model-Training-Base/model_training_base")
sys.path.append("./Chisel-Model-Training-Base/test")

import requests
import json

from fastapi import status
from test_helpers.test_helper_functions import load_and_compress_neural_net_training_images
from model_training_base.types.trainer_types import COMPRESSIONTYPE, TRAININGDATATYPE

service_url = "https://127.0.0.1:3001"

http_request = requests.Session()
http_request.verify = False

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
   

        


    
