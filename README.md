Taxi Driver Event Time and Location Prediction
=======================================

This machine learning system will predict when the best taxi pick times and locations are based on future events. This will help drivers to know when and where the best times are and helps them to maximize revenue on a given date. 

Our system automates this process by:

Ingesting historical trip data, including time, pickup location, drop off location, fare amount, etc. 
Ingesting event data including event start and end times, event location, event side street, event type. 
Analyzing correlations between past events and ride demand
Visualizing predictions of optimal pickup zones and times of a high ride requests. 

Value Proposition
-----------------
Value Proposition
Most drivers are freelance. This system gives them the opportunity to better plan their driving schedules and routes, increasing efficiency and income. 

Business Metrics:
- Increase driver hourly revenue
- Reduce time in between rides


Contributors
------------
| Name         | Responsible for                                                  | Link to their commits in this repo |
|--------------|------------------------------------------------------------------|------------------------------------|
| All Members  | System design, integration, DevOps and CI/CD pipeline (Unit 3)   |                                    |
| Imani Gomez  | Model training, experiment tracking (Units 4 & 5)                | https://github.com/el4435/MLOPs-Project/commits/main/?author=ImaniGomez |
| Asrita Bobba | Model serving, system and model monitoring (Units 6 & 7)         | https://github.com/el4435/MLOPs-Project/commits/main/?author=asrita14      |
| Erxi Liu     | Data pipelines (Unit 8)                                          | https://github.com/el4435/MLOPs-Project/commits/main/?author=el4435   |

System Diagram
--------------
System Flow:

    [User Input: Event Calendar, Taxi Trip History]
            ↓
    [Preprocessing Pipeline (ETL)]
            ↓
    [Demand Forecasting Model API (FastAPI)]
            ↓
    [Visualization Dashboard (Grafana/Streamlit)]
            ↕
    [Monitoring & Logging]
            ↕
    [MLflow Tracking / Feedback Loop]

All components containerized and orchestrated via CI/CD on Chameleon Cloud.

Summary of Outside Materials
----------------------------
| Name              | How it was created                                                | Conditions of use                     |
|-------------------|-------------------------------------------------------------------|---------------------------------------|
| NYC Taxi Data     | Open dataset of yellow cabs from the city of New York             | Open data license                     |
| NYC Events Data   | Open data set of events from the city of New York                 | Open data license                     |
| OpenStreetMap     | Map and geologication data for venue matching                     | Open License                          |

Infrastructure Requirements
---------------------------
| Requirement       | Quantity / Timeline                         | Justification                                          |
|-------------------|---------------------------------------------|--------------------------------------------------------|
| m1.medium VMs     | 3 total, full duration                      | Hosts ingestion, dashboard, model API, MLflow          |
| gpu_a100          | 4-hour block, 2–3 times/week                | Required for fine-tuning transformer models            |
| Floating IPs      | 1 persistent, 1 temporary                   | Public access to dashboard and API                     |
| Persistent Volume | 100GB (throughout)                          | Storage for ingested data, model artifacts, logs       |
| Ray Cluster       | On-demand, on GPUs                          | Schedule HPO and training via Ray Tune/Train           |

Detailed Design Plan
--------------------

Model Training & Infrastructure (Imani – Units 4 & 5)
-----------------------------------------------------
- Strategy: Train demand prediction models using time-series and spatial data (LSTM + XGBoost)
- Infrastructure: Use Ray to run model selection and tuning jobs
- Experiment Tracking: MLflow logs all experiments, including event types, features, and metrics
- Unit 4 Compliance: Automated retraining pipeline on updated trip and event data
- Unit 5 Compliance: Scheduled Ray jobs for incremental learning and version tracking

Model Serving & Monitoring (Asrita – Units 6 & 7)
-------------------------------------------------
- Serving: FastAPI endpoints deliver real-time predictions (pickup density by hour + location)
- Optimizations: Prune models and test ONNX for faster inference
- Deployment: Compare CPU and GPU inference speeds for scalability
- Monitoring:
  - Evaluate performance in difference zones and event categories
  - Load tests API with simulated queries
  - Canary testing for new model releases
  - Feedback loopusing taxi location pings to assess prediction accuracy

Difficulty Point:
Evaluate difference time-series models (ARIMA, LSTM, Prophet) under variable event densities

Data Pipeline (Erxi – Unit 8)
-----------------------------
- Offline ETL:
  - Combine trip data with scheduled events
  - Perform spatial joins using H3 hex bins
  - Aggregate historical patterns for feature engineering
- Online Stream:
  - Simulated future event impact using past event signatures
  - Continuously update pickup hotspots on dashboard
- Storage: Maintain both raw and processed data for retraining and validation
  
Difficulty Point:
Efficiant spatial joins and indexing of dense urban data with event overlays

Continuous X / DevOps (All group members – Unit 3)
-------------------------------------
- IaC:Terraform + Ansible provisions and configurations compute and storage resources
- CI/CD: GitHub Actions + Argo automates ETL -> training -> deployment
- Environments: Helm + ArgoCD for multistage deployment
- Testing: Coverage inclused ETL unit tests, model accuracy, load testing of API
- Cloud-Native: Everything in containers, reproducable pipelines

Extra “Difficulty Points” Summary
---------------------------------
| Unit   | Extra Difficulty Point                                      |
|--------|-------------------------------------------------------------|
| Unit 6 | Model comparision across multiple time-series frameworks    |
| Unit 8 | Real-time geospatial visualization with live event overlays |

Date: 2025-04-15

