#!/bin/bash

set -e

echo "[1/5] Create /mnt/block mount directory (if not exists)..."
sudo mkdir -p /mnt/block

echo "[2/5] Detect block volume device (e.g., /dev/vdb1)..."
lsblk

read -p "Enter your block volume device name (e.g., /dev/vdb1): " VOLUME_DEVICE

echo "Mounting $VOLUME_DEVICE to /mnt/block..."
sudo mount $VOLUME_DEVICE /mnt/block

echo "[3/5] Listing contents of /mnt/block:"
ls -l /mnt/block

echo "[4/5] Checking for MLflow artifact directory:"
ls /mnt/block/mlruns || echo "mlruns not found. Please verify the mount."

echo "[5/5] Example: load model using MLflow in Python:"
echo "
import mlflow.sklearn
model = mlflow.sklearn.load_model('file:///mnt/block/mlruns/1/<run_id>/artifacts/random_forest_model')
"

echo "Environment recovery complete. You can now start Jupyter or run prediction scripts."
