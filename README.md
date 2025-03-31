# MLOPs-Project
**Event-Based Sentiment Monitoring System**

We propose a machine learning system that enables real-time monitoring of public sentiment in response to specific events (e.g., product launches, political announcements, financial reports). In many organizations today, understanding public reaction relies on manual review of social media and news, often lacking scalability, timeliness, and quantifiable metrics.

Our system addresses this by automatically ingesting online content from Twitter and news outlets based on tracked events, classifying each message's sentiment using a fine-tuned language model, and visualizing sentiment trends in real time.

This allows teams (e.g., PR, marketing, policy analysts) to:
- Detect spikes in negative sentiment and mitigate crises
- Assess public reception of announcements or campaigns
- Compare emotional impact across events or geographies

We will measure success with:
- Sentiment classification accuracy
- System latency from ingestion to dashboard update
- Time-to-insight for analysts compared to manual methods

---

### Contributors

| Name          | Responsible for                                           | Link to their commits in this repo |
|---------------|-----------------------------------------------------------|------------------------------------|
| All team members | Project design, event tracking logic, integration         |                                    |
| Imani Gomez   | Model training and experiment tracking (Units 4 & 5)       |                                    |
| Asrita Bobba  | Model serving and monitoring (Units 6 & 7)                 |                                    |
| Erxi Liu      | Data pipeline (Unit 8) and DevOps / continuous pipeline (Unit 3) |                              |

---

### System diagram

_(To be added – a flowchart showing: Event Input → Twitter/News Ingestion → Sentiment Classifier API → Dashboard & Feedback Loop. A PNG or draw.io diagram should be placed here before final submission.)_

---

### Summary of outside materials

| Name           | How it was created                                                                 | Conditions of use                 |
|----------------|--------------------------------------------------------------------------------------|-----------------------------------|
| Sentiment140   | 1.6 million tweets labeled via emoticons, preprocessed for ML tasks                | Open use for academic purposes    |
| TweetEval      | Benchmark collection of tweet classification tasks including sentiment             | HuggingFace, research license     |
| Twitter API v2 | Provides real-time streaming and historical tweets based on keywords/hashtags      | Requires developer key, TOS apply |
| NewsAPI        | Aggregates global headlines from major sources, queried by keyword                 | Free for non-commercial use       |
| BERT-base (or RoBERTa) | Pre-trained transformer models for general language understanding     | Open source (Apache/MIT licenses) |

---

### Summary of infrastructure requirements

| Requirement     | How many/when                                      | Justification                         |
|-----------------|----------------------------------------------------|---------------------------------------|
| `m1.medium` VMs | 3 total – used throughout project lifecycle        | Hosting ingestion pipeline, dashboard, MLflow |
| `gpu_a100`      | 4-hour blocks 2–3 times/week                       | Model training and tuning experiments |
| Floating IPs    | 1 persistent, 1 dynamic                            | Expose model API and dashboard        |
| Persistent volume | ~100GB attached storage                         | Store models, logs, ingestion cache   |

---

### Detailed design plan

#### Model training and training platforms (Imani)

We will fine-tune a BERT-based transformer model using the Sentiment140 and TweetEval datasets for tweet-level sentiment classification (positive / neutral / negative). Training will be performed on GPU instances using PyTorch and HuggingFace. Model performance (accuracy, F1) will be tracked in MLflow hosted on Chameleon cloud.  
Experiments will be submitted via Ray for scheduling and load balancing.

**Difficulty Point**:  
We will use **Ray Tune** for hyperparameter optimization with advanced schedulers (e.g., ASHA, PBT).

---

#### Model serving and monitoring platforms (Asrita)

The fine-tuned model will be wrapped in a FastAPI service and containerized for cloud deployment. The API will support batch and online inference for ingestion pipelines and for live dashboard visualization. We will test and report inference latency and throughput.

Monitoring will include:
- Offline evaluation after each training
- Online monitoring of traffic, latency, drift
- Feedback loop: samples from production flagged for retraining

**Difficulty Point**:  
We will deploy and compare **multiple serving backends** (GPU-based and CPU-optimized), tracking latency/cost tradeoffs.

---

#### Data pipeline (Erxi)

We will implement two pipelines:

1. **Offline pipeline**: Use Twitter Search API and NewsAPI to periodically ingest data related to specified events (e.g. "Apple Vision Pro", "#budget2025"). Apply preprocessing, deduplication, and save to persistent volume.

2. **Streaming pipeline**: Simulate real-time tweets/news using pre-collected data or the Twitter stream API. Clean, route to classifier API, and log prediction results.

All pipeline code and configurations will be managed via version control and integrated into the CI/CD flow.

**Difficulty Point**:  
We will implement an interactive streaming sentiment **dashboard** using Streamlit or Grafana, updated in real time.

---

#### Continuous X (Erxi)

We will adopt full DevOps best practices:
- Infrastructure-as-code: Use Terraform and Ansible to provision services on Chameleon.
- CI/CD: A GitHub Actions or Argo Workflow pipeline will trigger:
  - Data ingestion (offline)
  - Model training + evaluation
  - Container build + deployment
  - Testing in staging → canary → production
- Cloud-native: All services will be containerized and independently deployable.

This approach enables traceability, reproducibility, and automated iteration across the system.

---
