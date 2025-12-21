#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, BackgroundTasks
from src.models.train_model import training
from src.models.predict_model import predict
from src.data.make_dataset import make_dataset
from src.data.preprocessing import preprocessing
from dataclasses import dataclass
import mlflow


responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

api = FastAPI(
    title='API for weather forcasting',
    description="""
    This is a weather forcasting API controlling \
    the training and predicting processes.
    """,
    version='0.1.0'
)


@dataclass
class curr_status:
    status: str = "inactive"


training_status = curr_status()
predict_status = curr_status()
model_info = None
FILE_DATASET = None
FILE_PREPROCESSING = None
DATE = None


def wrapper_train_model():
    training_status.status = "active"
    global model_info
    model_info = training(FILE_PREPROCESSING)
    training_status.status = "inactive"


def wrapper_predict(model_info: mlflow.models.model.ModelInfo):
    predict_status.status = "active"
    predict(model_info, FILE_PREPROCESSING)
    predict_status.status = "inactive"


@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting api!'}


@api.get('/make_dataset', name='make sub-dataset from the raw data', responses=responses)
def get_make_dataset():
    global FILE_DATASET, DATE
    FILE_DATASET, DATE = make_dataset()
    return {'status': 'sub-dataset is created.'}


@api.get('/preprocessing', name='preprocess the data', responses=responses)
def get_preprocessing():
    global FILE_PREPROCESSING
    FILE_PREPROCESSING = preprocessing(FILE_DATASET, DATE)
    return {'status': 'data is preprocessed.'}


@api.get('/predict', name='Predict The Weather', responses=responses)
def get_predict(background_tasks: BackgroundTasks):
    try:
        if training_status.status == "active":
            raise HTTPException(
                status_code=503,
                detail='Training is in progress, please try again later')
        elif predict_status.status == "active":
            raise HTTPException(
                status_code=503,
                detail='Prediction is in progress, please try again later')
        elif model_info is None:
            raise HTTPException(
                status_code=404,
                detail='Model not found, please train the model first')
        else:
            background_tasks.add_task(wrapper_predict, model_info)
            return {'status': 'prediction started.'}
    except Exception as e:
        return {'error': str(e)}


@api.get('/training', name='Train The Model with existing data',
         responses=responses)
def get_training(background_tasks: BackgroundTasks):
    try:
        if training_status.status == "active":
            raise HTTPException(
                status_code=503,
                detail='Training is in progress, please try again later')
        elif training_status.status == "inactive":
            background_tasks.add_task(wrapper_train_model)
            return {'status': 'training started'}
    except Exception as e:
        return {'error': str(e)}


# if __name__ == "__main__":
#     wrapper_train_model()
#     wrapper_predict(model_info)
