# LAB 02: AI-POWERED IT INCIDENT SUMMARIZATION ASSISTANT
## Building a Simple GenAI Application

---

## OVERVIEW

In this lab, you will build a **complete, production-ready GenAI application** that:
- ✅ Loads IT incident data from CSV files
- ✅ Uses OpenAI API to analyze incidents
- ✅ Generates structured summaries with root causes and next actions
- ✅ Processes multiple incidents in batch
- ✅ Exports results to CSV and JSON formats
- ✅ Demonstrates real-world deployment patterns

**No tool calling. No RAG. Simple GenAI application.**

---

## PREREQUISITES

### 1. OpenAI Account & API Key
- Create account at https://platform.openai.com
- Generate API key at https://platform.openai.com/api-keys
- Add credits to account (free trial: $5, paid: $0.003+ per incident)

### 2. Python Libraries
```bash
pip install openai pandas numpy
```

### 3. Data Files
- `sample_incidents_10000.csv` - 10,000 IT incidents
- `it_incident_dataset_genai_25000.csv` - Alternative dataset (1,250 incidents)

---

## SETUP INSTRUCTIONS

### Step 1: Install Required Libraries
```bash
pip install openai pandas numpy
```

### Step 2: Set OpenAI API Key
**Option A: Environment Variable (Recommended)**
```bash
# macOS/Linux
export OPENAI_API_KEY='sk-your-api-key-here'

# Windows (PowerShell)
$env:OPENAI_API_KEY='sk-your-api-key-here'

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-api-key-here
```

**Option B: In Jupyter Notebook**
```python
import os
os.environ['OPENAI_API_KEY'] = 'sk-your-api-key-here'
```

### Step 3: Upload to Google Colab (Optional)
1. Open the notebook in Google Colab
2. Upload the CSV files using: `files.upload()`
3. The notebook will automatically use uploaded files

---

## NOTEBOOK STRUCTURE

### Section 1: Environment Setup & API Configuration
- Install libraries
- Configure OpenAI API key
- Set model parameters (gpt-4o-mini)

### Section 2: Data Loading & Exploration
- Load incident CSV files
- Display sample incidents
- Show data shape and structure

### Section 3: OpenAI API Fundamentals
- Correct API syntax
- Error handling patterns
- Response parsing

### Section 4: Prompt Engineering Techniques
1. **Basic Prompting** - Simple instructions
2. **Role Prompting** - Assign expertise ("You are an IT analyst...")
3. **Structured Output** - JSON format responses
4. **Few-Shot Prompting** - Provide examples
5. **Chain-of-Thought** - Step-by-step reasoning

**Best Practice Selected:** Structured Output + Role + Chain-of-Thought

### Section 5: Building the Incident Summarization Function
- `analyze_incident()` - Single incident analysis
- Error handling and retry logic
- JSON response parsing

### Section 6: Batch Processing
- `process_incidents_batch()` - Multiple incidents
- Rate limiting (delay between calls)
- Progress tracking

### Section 7: Demonstrating the Application
- Run on 3 sample incidents
- Show real output
- Display structured results

### Section 8: Displaying Results
- Pretty-print analysis for each incident
- Show summary, root cause, urgency, next actions

### Section 9: Exporting Results
- Export to CSV (easy database import)
- Export to JSON (for APIs and logs)
- Save structured DataFrame

### Section 10: Quality Metrics & Analysis
- Success rate calculation
- Urgency distribution
- Performance statistics

### Section 11: Production Deployment Guide
- Full-scale batch processing
- Real-time API endpoint
- Service desk integration
- Scheduled jobs

### Section 12: Cost Analysis & Optimization
- Price per incident ($0.003)
- ROI calculation ($8.33 per incident)
- Scenario analysis (100 to 100,000 incidents)

### Section 13: Conclusion & Key Takeaways
- Summary of learning objectives
- Best practices checklist
- Next steps for deployment

---

## RUNNING THE APPLICATION

### Quick Start (3 Incidents)
```python
# Already configured in Section 7
# Just run all cells!
# Processes 3 sample incidents for demonstration
```

### Process All Incidents
```python
# Modify Section 6
all_results = process_incidents_batch(
    df_incidents,
    max_incidents=None,  # Process all incidents
    delay_between_calls=0.1
)
```

### Custom Incident Analysis
```python
from openai import OpenAI

# Single incident
incident = "Database connection timeout. Users unable to access application."
analysis = analyze_incident(incident)
print(analysis)
```

---

## EXPECTED OUTPUT

### Sample Analysis Result
```json
{
  "summary": "Database connection pool exhaustion preventing user access to the CRM application.",
  "root_cause": "Connection pool size insufficient for peak load or long-running queries not terminating.",
  "impact": "All users unable to access CRM. Revenue transactions blocked. Customer service degraded.",
  "urgency": "critical",
  "next_actions": [
    "Check database connection pool settings and increase if necessary",
    "Review slow query log and optimize long-running queries",
    "Implement connection timeout and kill idle connections",
    "Monitor database performance metrics and add alerts"
  ]
}
```

### Export Formats

**CSV Export (incident_summaries_output.csv)**
```
incident_id,application,priority,summary,root_cause,urgency,...
INC-001,CRM,High,"Database connection pool exhaustion...",Insufficient pool size,critical,...
```

**JSON Export (incident_summaries_output.json)**
```json
[
  {
    "incident_id": "INC-001",
    "application": "CRM",
    "priority": "High",
    "analysis": {
      "summary": "...",
      "root_cause": "...",
      ...
    }
  }
]
```

---

## COST ESTIMATION

### Pricing (GPT-4o-mini)
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

### Per-Incident Cost
- Average incident: ~350 input tokens + 200 output tokens
- **Cost: $0.0018 per incident**

### Scenarios
| Incidents | Cost |
|-----------|------|
| 100 | $0.18 |
| 1,000 | $1.80 |
| 10,000 | $18.00 |
| 100,000 | $180.00 |

### ROI Calculation
- Manual incident analysis: 10 minutes × $50/hour = $8.33 per incident
- AI analysis cost: $0.0018 per incident
- **Net savings: $8.33 per incident**
- **Payback period: Immediate (ROI on first incident)**

---

## PROMPT ENGINEERING GUIDE

### The Best Prompt for Incident Analysis
```python
prompt = """
You are an expert IT incident analyst with deep expertise in infrastructure, 
databases, and systems.

Analyze the incident below systematically:
1. Identify symptoms and affected component
2. Determine root cause
3. Recommend resolution steps

Respond ONLY with valid JSON (no other text):
{
  "summary": "Brief 2-3 sentence summary",
  "root_cause": "Identified technical root cause",
  "impact": "Business/user impact",
  "urgency": "critical|high|medium|low",
  "next_actions": ["action 1", "action 2", "action 3"]
}

Incident: {incident_description}
"""
```

### Why This Works
1. **Role Assignment** - Establishes expertise
2. **Step-by-Step** - Encourages structured reasoning
3. **JSON Format** - Enables parsing and automation
4. **Clear Instructions** - Reduces hallucination
5. **Specific Output Format** - Guarantees parseable response

---

## PRODUCTION DEPLOYMENT CHECKLIST

- [ ] Set API key in environment variables (never hardcode)
- [ ] Implement error handling and retry logic
- [ ] Add rate limiting (respect API quotas)
- [ ] Monitor API costs (set budget alerts)
- [ ] Store results in database (audit trail)
- [ ] Cache responses for duplicate incidents
- [ ] Test on sample data first
- [ ] Validate output quality
- [ ] Add request/response logging
- [ ] Set up monitoring and alerting
- [ ] Document API integration
- [ ] Train support team on using results
- [ ] Create runbooks for common scenarios
- [ ] Set up cost tracking dashboard

---

## TROUBLESHOOTING

### Issue: "OpenAI API key not found"
**Solution:**
```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
```

### Issue: "Module 'openai' not found"
**Solution:**
```bash
pip install openai
```

### Issue: "JSON decode error"
**Solution:** The LLM response isn't valid JSON. Check:
- Model response contains only JSON (no preamble)
- All quotes are properly escaped
- No trailing commas in JSON objects

### Issue: "Rate limit exceeded"
**Solution:** Increase `delay_between_calls`:
```python
process_incidents_batch(
    df_incidents,
    delay_between_calls=2.0  # Increase delay
)
```

### Issue: "API cost too high"
**Solution:** Use `max_incidents` to test first:
```python
# Test with 10 incidents before full batch
test_results = process_incidents_batch(
    df_incidents,
    max_incidents=10
)
```

---

## EXTENSIONS & ENHANCEMENTS

### 1. Add Sentiment Analysis
```python
def analyze_with_sentiment(incident_description):
    analysis = analyze_incident(incident_description)
    # Add sentiment: positive, negative, neutral
    return analysis
```

### 2. Integrate with Service Desk
```python
# Connect to Jira
def auto_comment_jira(ticket_id, analysis):
    jira.issue(ticket_id).update(
        summary=analysis['summary']
    )
    jira.issue(ticket_id).add_comment(
        f"AI Analysis: {analysis['next_actions']}"
    )
```

### 3. Add Historical Context
```python
def analyze_with_history(incident, similar_past_incidents):
    # Include similar incidents in prompt
    # "Similar incidents in past 30 days: ..."
```

### 4. Create Dashboard
```python
# Use Streamlit for interactive dashboard
# Display incidents, analyses, metrics
```

### 5. Add Feedback Loop
```python
# Collect user feedback on analyses
# Retrain/optimize prompts based on feedback
```

---

## LEARNING OUTCOMES

By completing this lab, you will understand:

1. ✅ How to use OpenAI Chat API correctly
2. ✅ Best practices for prompt engineering
3. ✅ Building batch processing workflows
4. ✅ Parsing and structuring LLM responses
5. ✅ Error handling and validation
6. ✅ Cost analysis and ROI calculation
7. ✅ Production deployment patterns
8. ✅ Real-world GenAI application development

---

## REFERENCE MATERIALS

### OpenAI Documentation
- API Reference: https://platform.openai.com/docs/api-reference
- Models: https://platform.openai.com/docs/models
- Pricing: https://openai.com/pricing

### Best Practices
- Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- Safety Best Practices: https://platform.openai.com/docs/guides/safety-best-practices
- Rate Limiting: https://platform.openai.com/docs/guides/rate-limits

### Python Libraries
- OpenAI Python: https://github.com/openai/openai-python
- Pandas: https://pandas.pydata.org/docs/
- JSON: https://docs.python.org/3/library/json.html

---

## SUPPORT & QUESTIONS

- **API Issues**: Check OpenAI documentation and status page
- **Code Issues**: Review error messages and stack traces
- **Dataset Issues**: Verify CSV file format and column names
- **Cost Issues**: Review OpenAI pricing and set budget limits

---

## SUMMARY

This lab demonstrates building a **complete GenAI application** that:
- Solves a real business problem (faster incident resolution)
- Uses modern LLM APIs (OpenAI)
- Applies prompt engineering best practices
- Scales from 10 to 100,000+ incidents
- Delivers immediate ROI ($8+ value per incident)
- Integrates with existing enterprise systems

**You now have a production-ready incident summarization assistant!**

---

**Lab Version:** 1.0  
**Last Updated:** August 2, 2026  
**Status:** ✅ Complete & Production-Ready
