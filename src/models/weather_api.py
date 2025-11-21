#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from typing import Optional


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


@api.get('/')
def get_index():
    return {'greeting': 'Welcome to weather forcasting api!'}


@api.get('/predict', name='Predict The Weather', responses=responses)
def get_predict(day: Optional[int] = None):
    # TODO: call the prediction model routine
    try:
        # TODO: call the prediction model routine
        # predict the weather of following 7 days
        weather = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy',
                   'stormy', 'hazy']
    except Exception as e:
        return {'error': str(e)}

    if day:
        # how many days in the future
        try:
            return {'day': day,
                    'predict': weather[day]}
        except IndexError:
            raise HTTPException(
                status_code=404,
                detail='Unknown Index')
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail='Bad Type')
    else:
        # predict the weather of today
        try:
            return {'day': 0,
                    'predict': weather[0]}
        except IndexError:
            raise HTTPException(
                status_code=404,
                detail='Unknown Index')
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail='Bad Type')


@api.get('/training', name='Train The Model with existing data', 
         responses=responses)
def get_training():
    try:
        # TODO: call the traning model routine
        return {'status': 'training finished'}
    except Exception as e:
        return {'error': str(e)}
