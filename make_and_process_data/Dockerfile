FROM python:3.12-slim

WORKDIR /make_and_process_data

COPY make_dataset.py /make_and_process_data/make_dataset.py
COPY preprocessing.py /make_and_process_data/preprocessing.py

CMD ["python", "/make_and_process_data/make_dataset.py", "/make_and_process_data/preprocessing.py"]