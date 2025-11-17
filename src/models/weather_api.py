#!/usr/bin/env python3


from fastapi import FastAPI
api = FastAPI(
    title='weather forcasting api'
)

@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting api!'}

@api.get('/predict')
def get_predict():
    try:
        # TODO: call the prediction model routine
        return {'predict': 'sunny'}
    except Exception as e:
        return {'error': str(e)}

@api.get('/training')
def get_training():
    try:
        # TODO: call the traning model routine
        return {'status': 'training finished'}
    except Exception as e:
        return {'error': str(e)}
