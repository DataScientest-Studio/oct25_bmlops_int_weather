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
    # status can have four states: inactive, running, completed, failed
    status: str = "inactive"
    progress: int = 0
    message: str = ""


training_status = curr_status()
predict_status = curr_status()
model_info = None
FILE_DATASET = None
FILE_PREPROCESSING = None
DATE = None


def update_training_progress(progress: int, message: str):
    training_status.progress = progress
    training_status.message = message


def update_predict_progress(progress: int, message: str):
    predict_status.progress = progress
    predict_status.message = message


def wrapper_train_model():
    training_status.status = "running"
    training_status.progress = 0
    training_status.message = "Starting training..."
    try:
        global model_info
        model_info = training(FILE_PREPROCESSING, callback=update_training_progress)
        training_status.status = "completed"
    except Exception as e:
        training_status.status = "failed"
        training_status.message = str(e)
        raise e


def wrapper_predict(model_info: mlflow.models.model.ModelInfo):
    predict_status.status = "running"
    predict_status.progress = 0
    predict_status.message = "Starting prediction..."
    try:
        predict(model_info, FILE_PREPROCESSING, callback=update_predict_progress)
        predict_status.status = "completed"
    except Exception as e:
        predict_status.status = "failed"
        predict_status.message = str(e)
        raise e


@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting app!'}


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
        if training_status.status != "completed":
            raise HTTPException(
                status_code=503,
                detail='Training is not finished, please try to train the model first')
        elif predict_status.status == "running":
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
    except HTTPException:
        raise
    except Exception as e:
        return {'error': str(e)}


@api.get('/training', name='Train The Model with existing data',
         responses=responses)
def get_training(background_tasks: BackgroundTasks):
    try:
        if training_status.status == "running":
            raise HTTPException(
                status_code=503,
                detail='Training is in progress, please try again later')
        elif training_status.status == "inactive" or training_status.status == "completed" or training_status.status == "failed":
            background_tasks.add_task(wrapper_train_model)
            return {'status': 'training started'}
    except HTTPException:
        raise
    except Exception as e:
        return {'error': str(e)}


@api.get('/training-status', name='Get Training Status', responses=responses)
def get_training_status():
    return {
        "status": training_status.status,
        "progress": training_status.progress,
        "message": training_status.message
    }

@api.get('/predict-status', name='Get Predict Status', responses=responses)
def get_predict_status():
    return {
        "status": predict_status.status,
        "progress": predict_status.progress,
        "message": predict_status.message
    }
