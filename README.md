Event-Based Sentiment Monitoring System
=======================================

We propose a machine learning system that enables real-time monitoring of public sentiment in response to specific events (e.g., product launches, policy decisions, earnings calls). Traditionally, PR and analytics teams manually track social media and news for sentiment analysis, leading to delays and limited scalability.

Our system automates this process by:
- Ingesting tweets and news articles related to specified events via APIs.
- Classifying the sentiment of each item using a fine-tuned transformer model.
- Aggregating and visualizing sentiment trends on a live dashboard.

Value Proposition
-----------------
This enables faster, more actionable insights for PR, marketing, and policy teams:
- Identify and respond to spikes in negative sentiment in near real-time.
- Evaluate public perception of announcements, compare reactions across demographics or regions.
- Monitor ongoing events or campaigns with quantifiable metrics.

Baseline Comparison (non-ML status quo): Manual search and review of social media/news by humans.

Business Metrics:
- Sentiment classification F1 score (≥ 85%)
- System latency from ingestion to dashboard update (≤ 10 seconds)
- Analyst "time to insight" vs. manual workflow (≥ 3x speedup)

Contributors
------------
| Name         | Responsible for                                                  | Link to their commits in this repo |
|--------------|------------------------------------------------------------------|------------------------------------|
| All Members  | System design, integration, DevOps and CI/CD pipeline (Unit 3)   |                                    |
| Imani Gomez  | Model training, experiment tracking (Units 4 & 5)                |                                    |
| Asrita Bobba | Model serving, system and model monitoring (Units 6 & 7)         |                                    |
| Erxi Liu     | Data pipelines (Unit 8)       |                                  |

System Diagram
--------------
System Flow:

    [User Input: Events]
            ↓
    [Twitter Stream] ←→ [NewsAPI]
            ↓
    [Preprocessing Pipeline (ETL)]
            ↓
    [Sentiment Model API (FastAPI)]
            ↓
    [Real-Time Dashboard (Grafana/Streamlit)]
            ↕
    [Monitoring & Logging]
            ↕
    [MLflow Tracking / Feedback Loop]

All components containerized and orchestrated via CI/CD on Chameleon Cloud.

Summary of Outside Materials
----------------------------
| Name              | How it was created                                                | Conditions of use                     |
|-------------------|-------------------------------------------------------------------|---------------------------------------|
| Sentiment140      | Labeled using emoticons on 1.6M tweets (Go et al. 2009)           | Open for academic/research use        |
| TweetEval         | HuggingFace benchmark for Twitter-specific tasks                 | Research license                      |
| Twitter API v2    | Live streaming and search endpoints, based on hashtags/keywords   | Requires dev key, TOS applies         |
| NewsAPI           | Aggregates news articles from major publishers via REST API       | Free tier: dev use only               |
| BERT-base/RoBERTa | Pretrained transformer models from HuggingFace                    | Apache/MIT licenses, research-friendly|

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
- Strategy: Fine-tune RoBERTa-base on Sentiment140 and TweetEval using PyTorch.
- Infrastructure: Train models on A100 GPUs using Ray + HuggingFace Transformers.
- Experiment Tracking: MLflow hosted on Chameleon will log hyperparameters, metrics, artifacts.
- Unit 4 Compliance: Re-training pipeline triggered automatically with new labeled data.
- Unit 5 Compliance: Training jobs submitted to Ray cluster with experiment tracking via MLflow.

Model Serving & Monitoring (Asrita – Units 6 & 7)
-------------------------------------------------
- Serving: Containerized FastAPI endpoint for online and batch inference.
- Optimizations: Apply ONNX conversion + quantization to reduce inference latency.
- Deployment: Use both GPU and CPU serving for performance comparison.
- Monitoring:
  - Offline eval on standard + edge-case slices.
  - Load tests in staging (with Locust).
  - Canary testing with simulated traffic.
  - Feedback loop with flagged examples for retraining.

Difficulty Point:
Compare GPU-based vs. CPU-based vs. quantized inference backends.

Data Pipeline (Erxi – Unit 8)
-----------------------------
- Offline ETL:
  - Ingest data using Twitter API (search endpoint) and NewsAPI.
  - Filter by keywords, remove duplicates, clean and store to mounted persistent volume.
- Online Stream:
  - Simulated stream using tweet/news replay scripts.
  - Real-time processing and classification, push to dashboard and logs.
- Storage: Preprocessed data, raw sources, predictions saved in structured format for re-training.

Difficulty Point:
Build an interactive sentiment dashboard (Grafana or Streamlit + Redis + WebSocket backend).

Continuous X / DevOps (All group members – Unit 3)
-------------------------------------
- IaC: Use Terraform and Ansible to provision infrastructure and attach persistent volumes.
- CI/CD: GitHub Actions + Argo Workflows trigger the full training → testing → deployment pipeline.
- Environments: Deploy to staging → canary → production via Helm + ArgoCD.
- Testing: Unit tests, load tests, offline evaluation all automated.
- Cloud-Native: Everything in containers, immutable infra, microservice architecture.

Extra “Difficulty Points” Summary
---------------------------------
| Unit   | Extra Difficulty Point                                      |
|--------|-------------------------------------------------------------|
| Unit 6 | Multi-backend serving performance comparison                |
| Unit 8 | Interactive dashboard for streaming sentiment visualization |

Date: 2025-03-31
