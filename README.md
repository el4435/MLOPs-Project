Player Pulse: Event-Based Sentiment Monitoring System for Athlete Endorsements
=======================================

We propose a machine learning system that enables real-time monitoring of public sentiment in response to specific events (e.g., player performances, controversies, awards). Traditionally, brand marketing and sponsorship teams rely on manual or delayed reports to assess a player's reputation, making endorsement decisions slow or risky.

Our client is a sports sponsor company (e.g., Nike, Red Bull, Adidas) that invests in athlete endorsements. The goal is to help sponsors evaluate how athletes are being perceived publicly on social media before and after major events—by displaying traits, trending descriptors, and sentiment scores derived from Twitter data.

Our system automates this process by:

Ingesting tweets related to specific athletes and events via APIs.
Classifying the sentiment of each tweet using a fine-tuned transformer model.
Aggregating, analyzing, and visualizing sentiment trends alongside performance stats on a live dashboard.

Value Proposition
-----------------
Value Proposition
This enables faster and more confident decision-making for sponsorship and PR teams:

Identify and respond to spikes in negative sentiment in near real-time.
Compare athlete perceptions across geographies or time periods (e.g., pre/post-match).
Understand public attribution of traits like “clutch,” “overrated,” “team player,” etc.
Quantify brand risk and media value before signing endorsement deals.
Baseline Comparison: Manual PR scanning, static reports, post-hoc surveys.

Business Metrics:

Sentiment classification F1 score (≥ 85%)
Dashboard update latency (≤ 10 seconds)
Sponsorship team time-to-insight (≥ 3x faster)


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
