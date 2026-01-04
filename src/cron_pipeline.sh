#!/bin/bash
LOG="/app/data/cron.log"  # ← hier ins Docker-Volume

echo "Start cron $(date)" >> "$LOG"

curl -s http://localhost:8000/make_dataset >> "$LOG"
curl -s http://localhost::8000/preprocessing >> "$LOG"
curl -s http://localhost::8000/training >> "$LOG"

echo "End cron $(date)" >> "$LOG"