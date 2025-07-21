# AI Operating System - Training Datasets

This directory contains comprehensive JSONL datasets for training and fine-tuning AI agents and language models for the AI Operating System framework.

## Dataset Overview

### 🤖 Agent Training Data (`agent_training.jsonl`)
- **Purpose**: Train individual AI agents for specific tasks and domains
- **Samples**: 1,000 training examples
- **Use Cases**: Agent behavior modeling, task-specific fine-tuning, capability learning

**Schema:**
```json
{
  "id": "unique_identifier",
  "timestamp": "ISO_timestamp",
  "agent": "agent_name",
  "role": "agent_role_description", 
  "context": {
    "current_task": "task_type",
    "system_state": {},
    "available_resources": {},
    "constraints": [],
    "goals": []
  },
  "input": "human_readable_task_description",
  "output": {
    "status": "completion_status",
    "summary": "task_summary", 
    "details": {},
    "recommendations": [],
    "metrics": {},
    "confidence_score": 0.0-1.0
  },
  "metadata": {
    "capabilities": [],
    "domains": [],
    "confidence": 0.0-1.0,
    "execution_time_ms": 0
  }
}
```

### 🔄 System Interactions (`system_interactions.jsonl`)
- **Purpose**: Train multi-agent orchestration and coordination
- **Samples**: 500 interaction scenarios
- **Use Cases**: Agent coordination, workflow orchestration, system-level decision making

**Schema:**
```json
{
  "id": "unique_identifier",
  "timestamp": "ISO_timestamp",
  "scenario": "interaction_scenario_type",
  "involved_agents": [],
  "orchestration": {
    "execution_order": [],
    "parallel_stages": [],
    "decision_points": [],
    "rollback_strategy": {},
    "success_criteria": []
  },
  "execution_flow": [],
  "dependencies": {},
  "expected_outcomes": {},
  "coordination_messages": [],
  "metadata": {
    "complexity": "low|medium|high",
    "estimated_duration": 0,
    "resource_requirements": {}
  }
}
```

### 📊 Monitoring Data (`monitoring_data.jsonl`)
- **Purpose**: Train system monitoring and anomaly detection models
- **Samples**: 2,000 monitoring snapshots
- **Use Cases**: Health monitoring, performance prediction, anomaly detection

**Schema:**
```json
{
  "id": "unique_identifier",
  "timestamp": "ISO_timestamp",
  "system_metrics": {
    "cpu_usage": 0.0-100.0,
    "memory_usage": 0.0-100.0,
    "disk_usage": 0.0-100.0,
    "network_io": 0.0-100.0
  },
  "agent_metrics": {},
  "performance_indicators": {},
  "health_score": 0.0-1.0,
  "alerts": [],
  "trends": {},
  "anomalies": [],
  "metadata": {}
}
```

### 💬 Conversations (`conversations.jsonl`)
- **Purpose**: Train human-AI interaction and natural language understanding
- **Samples**: 800 conversation examples
- **Use Cases**: Chat interfaces, voice assistants, natural language processing

**Schema:**
```json
{
  "id": "unique_identifier",
  "timestamp": "ISO_timestamp",
  "conversation_type": "task_assignment|status_inquiry|troubleshooting|...",
  "human_input": "natural_language_input",
  "ai_response": "natural_language_response",
  "context": {},
  "intent": "extracted_intent",
  "entities": [],
  "sentiment": {},
  "follow_up_actions": [],
  "metadata": {}
}
```

### 📝 Execution Logs (`execution_logs.jsonl`)
- **Purpose**: Train debugging, optimization, and performance analysis models
- **Samples**: 1,500 execution records
- **Use Cases**: Performance optimization, error prediction, resource planning

**Schema:**
```json
{
  "id": "unique_identifier",
  "execution_id": "execution_identifier",
  "agent_name": "agent_name",
  "agent_version": "version_string",
  "start_time": "ISO_timestamp",
  "end_time": "ISO_timestamp", 
  "duration_ms": 0,
  "status": "success|failed|timeout|error",
  "input_parameters": {},
  "output_data": {},
  "error_details": {},
  "resource_usage": {},
  "performance_metrics": {},
  "trace_data": [],
  "metadata": {}
}
```

## Generation Process

The datasets are generated using the `generate_datasets.py` script, which creates realistic, diverse, and comprehensive training data covering:

### Agent Types Covered
- **CostOptBot**: Cost optimization and analysis
- **SecuBot**: Security hardening and monitoring
- **ComplianceBot**: Regulatory compliance auditing
- **TestGenie**: Automated testing and QA
- **PrivacyGuard**: Data privacy and protection
- **InsightsBot**: Analytics and business intelligence
- **ConvDesignBot**: Conversation design and UX
- **ModelRefactor**: Code refactoring and optimization
- **ArchitectureBot**: System architecture design

### Scenario Types
- Cost optimization workflows
- Security audit procedures
- Compliance checking processes
- Performance analysis tasks
- System upgrade scenarios
- Incident response protocols
- Capacity planning exercises
- Risk assessment procedures

### Data Characteristics
- **Temporal Distribution**: 90-day historical data range
- **Realistic Metrics**: CPU, memory, network, and performance data
- **Error Scenarios**: Failures, timeouts, and edge cases
- **Multi-Agent Coordination**: Complex interaction patterns
- **Human-AI Conversations**: Natural language interactions
- **Execution Tracing**: Detailed performance and debugging data

## Usage Examples

### Training Agent-Specific Models

```python
import json
import pandas as pd

# Load agent training data
def load_agent_data(agent_name):
    data = []
    with open('agent_training.jsonl', 'r') as f:
        for line in f:
            record = json.loads(line)
            if record['agent'] == agent_name:
                data.append(record)
    return data

# Example: Train CostOptBot
costopt_data = load_agent_data('CostOptBot')
print(f"CostOptBot training samples: {len(costopt_data)}")
```

### Training System Orchestration Models

```python
# Load system interaction data
def load_orchestration_data():
    data = []
    with open('system_interactions.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Analyze complexity distribution
interactions = load_orchestration_data()
complexity_dist = pd.Series([i['metadata']['complexity'] for i in interactions]).value_counts()
print("Complexity Distribution:", complexity_dist)
```

### Training Monitoring Models

```python
# Load monitoring data for anomaly detection
def load_monitoring_data():
    data = []
    with open('monitoring_data.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Extract features for ML training
monitoring_data = load_monitoring_data()
features = []
for record in monitoring_data:
    features.append([
        record['system_metrics']['cpu_usage'],
        record['system_metrics']['memory_usage'],
        record['system_metrics']['disk_usage'],
        record['health_score'],
        len(record['alerts'])
    ])
```

### Training Conversation Models

```python
# Load conversation data for NLP training
def load_conversation_data():
    data = []
    with open('conversations.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Prepare for fine-tuning
conversations = load_conversation_data()
training_pairs = [
    {
        "input": conv['human_input'],
        "output": conv['ai_response'],
        "context": conv['context']
    }
    for conv in conversations
]
```

## Fine-Tuning Guidelines

### For Large Language Models (LLMs)

1. **Agent-Specific Fine-Tuning**:
   ```bash
   # Example using Hugging Face transformers
   python fine_tune.py \
     --model_name microsoft/DialoGPT-medium \
     --dataset agent_training.jsonl \
     --agent_filter CostOptBot \
     --output_dir ./models/costopt_bot
   ```

2. **Multi-Agent Coordination**:
   ```bash
   python fine_tune.py \
     --model_name facebook/opt-1.3b \
     --dataset system_interactions.jsonl \
     --task coordination \
     --output_dir ./models/orchestrator
   ```

3. **Conversation AI**:
   ```bash
   python fine_tune.py \
     --model_name microsoft/DialoGPT-large \
     --dataset conversations.jsonl \
     --task dialogue \
     --output_dir ./models/chat_assistant
   ```

### For Machine Learning Models

1. **Anomaly Detection**:
   ```python
   from sklearn.ensemble import IsolationForest
   from sklearn.preprocessing import StandardScaler
   
   # Train on monitoring data
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(features)
   
   model = IsolationForest(contamination=0.1)
   model.fit(X_scaled)
   ```

2. **Performance Prediction**:
   ```python
   from sklearn.ensemble import RandomForestRegressor
   
   # Predict execution time based on input parameters
   X = extract_features(execution_logs)
   y = [log['duration_ms'] for log in execution_logs]
   
   model = RandomForestRegressor(n_estimators=100)
   model.fit(X, y)
   ```

## Quality Assurance

### Data Validation
- **Schema Compliance**: All records follow defined JSON schemas
- **Temporal Consistency**: Timestamps are chronologically ordered
- **Referential Integrity**: Agent references are valid
- **Metric Ranges**: All numeric values within realistic bounds

### Diversity Metrics
- **Agent Distribution**: Balanced representation across all agent types
- **Scenario Coverage**: Full coverage of common operational scenarios
- **Complexity Levels**: Mix of simple, medium, and complex interactions
- **Success/Failure Ratios**: Realistic distribution of outcomes

### Data Quality Indicators
- **Completeness**: 95%+ of required fields populated
- **Accuracy**: Metrics within expected operational ranges
- **Consistency**: Coherent relationships between related fields
- **Realism**: Data patterns match real-world system behavior

## Extensions and Customization

### Adding New Agent Types
1. Update `agents` configuration in `generate_datasets.py`
2. Add agent-specific input/output templates
3. Define domain-specific capabilities and metrics
4. Regenerate datasets with new agent included

### Custom Scenarios
1. Extend `task_scenarios` list
2. Add scenario-specific orchestration patterns
3. Define expected outcomes and success criteria
4. Update coordination message templates

### Domain-Specific Data
1. Modify metric templates for specific domains
2. Add industry-specific compliance requirements
3. Include domain-relevant conversation patterns
4. Customize error and alert scenarios

## Integration with Training Pipelines

### Continuous Learning
```python
# Example: Incremental dataset updates
def update_datasets():
    new_data = collect_production_data()
    augmented_data = augment_with_synthetic(new_data)
    
    append_to_dataset('execution_logs.jsonl', augmented_data)
    retrain_models()
```

### Model Evaluation
```python
# Example: Evaluate model performance on test split
def evaluate_model(model, test_data):
    predictions = model.predict(test_data)
    metrics = calculate_metrics(predictions, test_data.labels)
    
    return {
        'accuracy': metrics.accuracy,
        'precision': metrics.precision,
        'recall': metrics.recall,
        'f1_score': metrics.f1
    }
```

### Production Deployment
```python
# Example: Deploy trained models
def deploy_model(model_path, endpoint_name):
    model = load_model(model_path)
    
    deploy_to_production(
        model=model,
        endpoint=endpoint_name,
        scaling_config=AutoScalingConfig()
    )
```

## Support and Documentation

For additional information:
- Review the `generate_datasets.py` script for implementation details
- Check `dataset_summary.json` for statistics and metadata
- Refer to the API documentation for integration patterns
- Contact the development team for custom requirements

## License and Usage

These datasets are provided for training AI systems within the AI Operating System framework. Please ensure compliance with data privacy regulations and organizational policies when using this data.
