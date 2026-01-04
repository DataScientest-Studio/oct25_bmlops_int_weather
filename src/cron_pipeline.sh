#!/bin/bash
LOG="/app/data/cron.log"  

sleep 30

echo "Start cron $(date)" >> "$LOG"

# Trigger the dataset creation, preprocessing, and training via API
curl -s http://localhost:8000/make_dataset >> "$LOG"
curl -s http://localhost::8000/preprocessing >> "$LOG"
curl -s http://localhost::8000/training >> "$LOG"

echo "End cron $(date)" >> "$LOG"