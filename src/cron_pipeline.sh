#!/bin/bash
LOG="/app/data/cron.log"  

sleep 30

echo "Start cron $(date)" >> "$LOG"

# Trigger the dataset creation, preprocessing, and training via API
echo "curl -s ${MODEL_URI}/make_dataset" >> "$LOG"
curl -s ${MODEL_URI}/make_dataset >> "$LOG"
echo "curl -s ${MODEL_URI}/preprocessing" >> "$LOG"
curl -s ${MODEL_URI}/preprocessing >> "$LOG"
echo "curl -s ${MODEL_URI}/training" >> "$LOG"
curl -s ${MODEL_URI}/training >> "$LOG"

echo "End cron $(date)" >> "$LOG"