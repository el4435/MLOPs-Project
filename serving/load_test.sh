#!/bin/bash
for i in {1..20}
do
  curl -X POST "http://localhost:8000/predict/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"features": [10, 161, 3, 0]}'
  echo ""
done
