from src.models.train_model import training
from src.models.predict_model import predict
from src.data.make_dataset import make_dataset
from src.data.preprocessing import preprocessing


model_info = None
FILE_DATASET = None
FILE_PREPROCESSING = None
DATE = None
df = None

FILE_DATASET, DATE = make_dataset()
FILE_PREPROCESSING = preprocessing(FILE_DATASET, DATE)
model_info = training(FILE_PREPROCESSING)
predict(model_info, FILE_PREPROCESSING)