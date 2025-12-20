FROM python:3.12-slim

WORKDIR /make_and_process_data

COPY make_and_process_data/make_dataset.py ./make_dataset.py
COPY make_and_process_data/preprocessing.py ./preprocessing.py
COPY requirements.txt ./
RUN pip install -r requirements.txt

# CMD ["python", "/make_and_process_data/make_dataset.py", "/make_and_process_data/preprocessing.py"]
CMD ["python", "/make_and_process_data/make_dataset.py"]