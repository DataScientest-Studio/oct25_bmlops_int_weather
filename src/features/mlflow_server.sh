#!/bin/bash

python -m mlflow server \
  --host localhost \
  --port 8080 \
  --backend-store-uri file:///models \
  --default-artifact-root file:///models \
  --serve-artifacts


