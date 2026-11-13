# LAB 02: QUICK REFERENCE GUIDE
## OpenAI API & Prompt Engineering

---

## QUICK START (3 minutes)

### 1. Set API Key
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### 2. Import Libraries
```python
from openai import OpenAI
import json

client = OpenAI()
```

### 3. Make First Call
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## API REFERENCE

### Chat Completion Call
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",           # Model name
    messages=[...],                 # Message list
    temperature=0.7,                # Creativity (0-1)
    max_tokens=500,                 # Response length
    top_p=1.0                       # Diversity (0-1)
)
```

### Extract Response
```python
# Get the text response
text = response.choices[0].message.content

# Get usage info
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

# Calculate cost
cost = (input_tokens * 0.15 + output_tokens * 0.60) / 1_000_000
```

### Message Format
```python
messages = [
    # Optional: Set system context
    {"role": "system", "content": "You are an IT expert"},
    
    # Required: User input
    {"role": "user", "content": "Analyze this incident..."},
    
    # Optional: Add conversation history
    {"role": "assistant", "content": "Previous response..."},
    {"role": "user", "content": "Follow-up question..."}
]
```

---

## PROMPT ENGINEERING CHEAT SHEET

### Pattern 1: Role Assignment
```python
prompt = """
You are an expert IT incident analyst.
Analyze this incident: {incident}
"""
```

**Effect:** 10-20% quality improvement

### Pattern 2: Structured Output
```python
prompt = """
Respond ONLY with JSON:
{
  "summary": "...",
  "root_cause": "...",
  "next_actions": [...]
}
Incident: {incident}
"""
```

**Effect:** 100% parseable, enables automation

### Pattern 3: Few-Shot Examples
```python
prompt = """
Example:
Incident: "Database timeout"
Response: {"summary": "Pool exhausted", ...}

Now analyze: {incident}
"""
```

**Effect:** 20-30% quality improvement

### Pattern 4: Chain-of-Thought
```python
prompt = """
Step 1: Identify symptoms
Step 2: Determine root cause
Step 3: Recommend actions
Incident: {incident}
"""
```

**Effect:** Better reasoning on complex tasks

### Pattern 5: Temperature Control
```python
# Deterministic (analysis, summary)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0  # ← Always same response
)

# Balanced (general purpose)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0.7  # ← Balanced
)

# Creative (brainstorming)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=1.0  # ← Varied responses
)
```

---

## COMMON PATTERNS

### Pattern: Error Handling
```python
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        timeout=30
    )
    return response.choices[0].message.content
except Exception as e:
    print(f"API Error: {str(e)}")
    return None
```

### Pattern: Batch Processing
```python
results = []
for idx, incident in enumerate(incidents, 1):
    print(f"[{idx}/{len(incidents)}]", end=" ")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Analyze: {incident}"}]
    )
    
    results.append(response.choices[0].message.content)
    print("✓")
    time.sleep(1)  # Rate limiting

return results
```

### Pattern: JSON Parsing
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": f"Return JSON: {prompt}"}]
)

try:
    data = json.loads(response.choices[0].message.content)
    return data
except json.JSONDecodeError:
    print("Failed to parse JSON")
    return {"error": "parse_failed"}
```

### Pattern: Cost Tracking
```python
total_cost = 0

for incident in incidents:
    response = client.chat.completions.create(...)
    
    tokens_in = response.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens
    cost = (tokens_in * 0.15 + tokens_out * 0.60) / 1_000_000
    
    total_cost += cost
    print(f"Cost so far: ${total_cost:.4f}")
```

---

## MODELS COMPARISON

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| gpt-4o-mini | ⚡⚡⚡ Fast | $ Cheap | 8/10 | Incident analysis ✅ |
| gpt-4o | ⚡ Slow | $$$ Expensive | 9/10 | Complex reasoning |
| gpt-3.5-turbo | ⚡⚡ Fast | $$ | 6/10 | Deprecated |

**Recommendation:** Use gpt-4o-mini for most tasks

---

## PRICING GUIDE

### GPT-4o-mini Pricing
- **Input:** $0.15 per 1M tokens
- **Output:** $0.60 per 1M tokens

### Example Costs
| Task | Input Tokens | Output Tokens | Cost |
|------|--------------|---------------|------|
| Simple question | 50 | 100 | $0.0001 |
| Incident analysis | 350 | 200 | $0.0018 |
| Long document | 2000 | 1000 | $0.0009 |

### Cost per Scenario
| Scenario | Incidents | Cost |
|----------|-----------|------|
| Pilot test | 10 | $0.02 |
| Weekly batch | 100 | $0.18 |
| Monthly batch | 1,000 | $1.80 |
| Full processing | 10,000 | $18.00 |

---

## DEBUGGING TIPS

### Issue: "Module openai not found"
```bash
pip install openai
```

### Issue: "API key not found"
```python
import os
print(os.getenv('OPENAI_API_KEY'))  # Should print your key
```

### Issue: "JSON decode error"
```python
# Add 'respond only with JSON' to prompt
prompt = f"Respond ONLY with JSON: {original_prompt}"
```

### Issue: "Rate limit exceeded"
```python
# Increase delay between calls
time.sleep(2.0)  # Wait 2 seconds instead of 1
```

### Issue: "Response too long"
```python
# Reduce max_tokens
response = client.chat.completions.create(
    ...,
    max_tokens=300  # Reduce from 500
)
```

### Issue: "High cost"
```python
# Use cheaper model or reduce tokens
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Instead of gpt-4o
    messages=[...],
    max_tokens=300  # Reduce output length
)
```

---

## PARAMETER TUNING GUIDE

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| temperature | 0.7 | 0.0-2.0 | 0=deterministic, 1=balanced, 2=creative |
| max_tokens | N/A | 1-2000+ | Response length limit |
| top_p | 1.0 | 0.0-1.0 | Diversity control |
| frequency_penalty | 0 | -2.0-2.0 | Reduce repetition |
| presence_penalty | 0 | -2.0-2.0 | Encourage new topics |

**Recommended Settings:**
```python
# For structured analysis
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0.3,    # More deterministic
    max_tokens=500,
    top_p=0.9           # Slightly focused
)

# For creative brainstorming
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=1.0,    # Balanced
    max_tokens=1000,
    top_p=1.0          # Full diversity
)
```

---

## PROMPT OPTIMIZATION CHECKLIST

- [ ] Clear instruction (what to do)
- [ ] Context (who/why/when)
- [ ] Format specification (JSON/text/markdown)
- [ ] Examples (few-shot if complex)
- [ ] Constraints (be concise, etc.)
- [ ] Output structure (fields expected)

### Example Optimized Prompt
```python
prompt = """
You are an expert IT incident analyst with 15 years of experience.

Analyze the incident below and respond ONLY with JSON containing:
- summary (2-3 sentences)
- root_cause (technical reason)
- impact (business effect)
- next_actions (array of 3 steps)

Keep responses concise and actionable.

Incident: {incident_description}
"""
```

---

## BEST PRACTICES

### DO ✅
- Use environment variables for API keys
- Add error handling to all API calls
- Set appropriate max_tokens
- Implement rate limiting
- Track costs
- Test on small batch first
- Validate JSON responses
- Add logging
- Monitor API usage
- Set budget alerts

### DON'T ❌
- Hardcode API keys
- Ignore rate limits
- Process unlimited incidents
- Send raw user input
- Skip error handling
- Use high temperature for analysis
- Forget about costs
- Assume perfect JSON responses
- Process without logging
- Leave resources running

---

## TOKEN COUNTING

### How to Estimate Tokens
```python
# Rough estimate: 1 token ≈ 4 characters ≈ 1 word
text = "This is a sample incident description"
approx_tokens = len(text) / 4  # ≈ 8 tokens

# Exact count (requires API call)
from openai import Client
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
)
tokens = response.usage.total_tokens
```

### Cost Calculation
```python
tokens_in = 350
tokens_out = 200
cost = (tokens_in * 0.15 + tokens_out * 0.60) / 1_000_000
print(f"Cost: ${cost:.6f}")  # $0.000171
```

---

## REAL-WORLD EXAMPLES

### Example 1: Single Incident
```python
incident = "Database connection timeout. Users unable to access CRM."

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an IT analyst"},
        {"role": "user", "content": f"Analyze: {incident}"}
    ]
)

print(response.choices[0].message.content)
```

### Example 2: Structured JSON Output
```python
prompt = f"""
Analyze incident and respond with JSON:
{{"summary": "...", "root_cause": "...", "next_actions": [...]}}
Incident: {incident}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

data = json.loads(response.choices[0].message.content)
print(data['summary'])
print(data['root_cause'])
print(data['next_actions'])
```

### Example 3: Batch Processing
```python
incidents = [...]
results = []

for incident in incidents:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Analyze: {incident}"}]
    )
    results.append(response.choices[0].message.content)
    time.sleep(1)  # Rate limiting

pd.DataFrame({"analysis": results}).to_csv("results.csv")
```

---

## USEFUL LINKS

### Documentation
- OpenAI API: https://platform.openai.com/docs/api-reference
- Models: https://platform.openai.com/docs/models
- Pricing: https://openai.com/pricing

### Tools
- Playground: https://platform.openai.com/playground
- API Keys: https://platform.openai.com/api-keys
- Usage: https://platform.openai.com/account/usage/overview

### Learning
- Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- Best Practices: https://platform.openai.com/docs/guides/safety-best-practices
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits

---

## TROUBLESHOOTING FLOWCHART

```
API Call Fails?
├─ Authentication Error
│  └─ Check API key: os.getenv('OPENAI_API_KEY')
├─ Rate Limit Error
│  └─ Add delay: time.sleep(2.0)
├─ Timeout Error
│  └─ Increase timeout or reduce max_tokens
├─ JSON Parse Error
│  └─ Add "respond only with JSON" to prompt
└─ Other Error
   └─ Print full error: print(str(e))
```

---

## SUMMARY

| Concept | Key Point |
|---------|-----------|
| API Key | Store in environment, never hardcode |
| Model | Use gpt-4o-mini for cost efficiency |
| Temperature | 0.3 for analysis, 0.7 for balanced, 1.0 for creative |
| max_tokens | Set based on expected response length |
| JSON | Request structured output for parsing |
| Cost | ~$0.002 per incident analysis |
| Rate Limit | Add 1-2 second delay between calls |
| Error Handling | Always use try-except |
| Validation | Check JSON parsing, handle failures |
| Logging | Track all API calls and costs |

---

**Keep this guide handy for quick reference during development!**

**Questions?** See Lab02_README.md for detailed instructions.
