#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import Optional
from train_model import training
from predict_model import predict
from dataclasses import dataclass


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


def wrapper_train_model(status: curr_status):
    status.status = "active"
    training()
    status.status = "inactive"


def wrapper_predict(status: curr_status):
    status.status = "active"
    predict()
    status.status = "inactive"


@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting api!'}


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
        else:
            background_tasks.add_task(wrapper_predict, predict_status)
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
            background_tasks.add_task(wrapper_train_model, training_status)
            return {'status': 'training started'}
    except Exception as e:
        return {'error': str(e)}
