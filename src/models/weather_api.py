#!/usr/bin/env python3
from fastapi import FastAPI


responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

api = FastAPI(
    title='weather forcasting api'
)

@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting api!'}

@api.get('/predict', responses=responses)
def get_predict():
    try:
        # TODO: call the prediction model routine
        return {'predict': 'sunny'}
    except Exception as e:
        return {'error': str(e)}

@api.get('/training', responses=responses)
def get_training():
    try:
        # TODO: call the traning model routine
        return {'status': 'training finished'}
    except Exception as e:
        return {'error': str(e)}
