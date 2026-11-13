# LAB 02: INSTRUCTOR GUIDE
## AI-Powered IT Incident Summarization Assistant

---

## TEACHING OVERVIEW

**Lab Duration:** 2.5 - 3.5 hours  
**Difficulty Level:** Intermediate (assumes basic Python knowledge)  
**Key Skills:** GenAI, prompt engineering, API integration, batch processing  
**Real-World Relevance:** High (directly applicable to IT operations)

---

## LEARNING OBJECTIVES

### Primary Objectives
1. Build a working GenAI application from scratch
2. Master OpenAI Chat API usage
3. Apply prompt engineering techniques for structured output
4. Implement batch processing and error handling
5. Analyze ROI and deployment considerations

### Secondary Objectives
1. Understand token economics and API costs
2. Design effective prompts for domain-specific tasks
3. Parse and structure LLM responses
4. Deploy GenAI applications to production

---

## TIME ALLOCATION

| Section | Duration | Notes |
|---------|----------|-------|
| 1. Setup & Configuration | 15 min | Demo API key setup, handle Q&A |
| 2. Data Loading | 10 min | Show CSV exploration, discuss data quality |
| 3. API Fundamentals | 15 min | Demonstrate correct vs incorrect syntax |
| 4. Prompt Engineering | 20 min | Compare 5 techniques live, discuss tradeoffs |
| 5. Core Function | 10 min | Live coding walkthrough of analyze_incident() |
| 6. Batch Processing | 15 min | Demonstrate rate limiting and error handling |
| 7-9. Application Demo | 20 min | Run full pipeline, show results |
| 10-13. Analysis & Deployment | 30 min | Discuss costs, production patterns, next steps |
| Buffer/Discussion | 15 min | Q&A, troubleshooting, extended examples |
| **Total** | **2.5 hrs** | Can extend to 3.5 hrs with exercises |

---

## TEACHING STRATEGY

### 1. Live Coding Approach (Recommended)
- **Start with the notebook already open**
- **Run cells one at a time**
- **Pause for discussion after each section**
- **Allow learners to follow along**
- **Field questions naturally**

### 2. Demonstration-First Method
- **Show working examples first**
- **Explain why things work**
- **Then discuss edge cases and errors**
- **Builds confidence before diving deep**

### 3. Problem-Solving Perspective
- **Frame each section around a real problem**
- **"We want to summarize 10,000 IT incidents automatically"**
- **"How do we do this efficiently?"**
- **"What are the costs and ROI?"**

---

## SECTION-BY-SECTION TEACHING GUIDE

### SECTION 1: Environment Setup & API Configuration (15 min)

**Key Teaching Points:**
1. API keys are credentials - never hardcode or commit
2. Environment variables are the standard way to manage secrets
3. Python's OpenAI library abstracts HTTP details
4. Configuration parameters affect response quality and cost

**Demo Script:**
```python
# Show students how to set API key
import os
api_key = os.getenv('OPENAI_API_KEY')

# Explain the model choices
# gpt-4o-mini: Fast, cheap, good for most tasks
# gpt-4o: More capable, 10x more expensive
# gpt-3.5-turbo: Legacy, not recommended

# Show temperature effects
# 0.0 = deterministic (always same output)
# 0.7 = balanced (default)
# 1.0 = creative (very different each run)
```

**Discussion Questions:**
- "Why shouldn't we hardcode API keys?"
- "What's the difference between gpt-4o-mini and gpt-4o?"
- "When would we use high vs low temperature?"

**Common Issues:**
- API key not set → Show environment variable setup
- Wrong model name → Mention available models
- Rate limiting → Explain token limits

---

### SECTION 2: Data Loading & Exploration (10 min)

**Key Teaching Points:**
1. Real-world data is messy
2. Need to understand data before processing
3. Sample before full processing (cost savings)
4. Check for missing values and data quality

**Demo Script:**
```python
# Load data
df = pd.read_csv('sample_incidents_10000.csv')

# Show shape and structure
print(df.shape)  # (10000, 12)
print(df.columns)  # Show all incident fields

# Look at sample
print(df.head())

# Check for issues
print(df.info())  # Data types and missing values
```

**Discussion Questions:**
- "What does each column represent?"
- "Are there any data quality issues?"
- "Why do we check data before processing?"

**Key Insight:**
"Before building a GenAI application, understand your data. If incidents are poorly structured, the AI will struggle."

---

### SECTION 3: OpenAI API Fundamentals (15 min)

**Key Teaching Points:**
1. Correct API syntax (VERY important)
2. Common mistakes to avoid
3. Response structure
4. Error handling

**CRITICAL: Show WRONG vs RIGHT**

**WRONG (Common Mistake):**
```python
# ❌ This code doesn't work!
response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)
output = response.output_text
```

**RIGHT (Correct):**
```python
# ✅ This is the correct syntax
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=500
)
output = response.choices[0].message.content
```

**Demo with Real API:**
```python
# Make a test call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Say hello"}
    ]
)

# Show response structure
print(response)
print(response.choices[0].message.content)
```

**Discussion Questions:**
- "What's the difference between the wrong and right code?"
- "Why do we need role and content in messages?"
- "Where does the actual text appear in the response?"

**Interactive Activity:**
"Everyone write one API call. Run it. See it work."

---

### SECTION 4: Prompt Engineering Techniques (20 min)

**Key Teaching Points:**
1. Prompt quality = output quality
2. Different techniques for different problems
3. Structured output is essential for automation
4. JSON format enables downstream processing

**Demonstrate all 5 techniques:**

**Technique 1: Basic Prompting**
```python
prompt = "Analyze this incident: {incident}"
# Simple but often insufficient
```

**Technique 2: Role Prompting**
```python
prompt = """
You are a senior IT analyst.
Analyze this incident: {incident}
"""
# Adding context improves results ~10-20%
```

**Technique 3: Structured Output (BEST)**
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
# Enables automation and parsing
```

**Technique 4: Few-Shot**
```python
prompt = """
Example:
Incident: "Database timeout"
Response: {"summary": "...", "root_cause": "..."}

Now analyze: {incident}
"""
# Provides format by example
```

**Technique 5: Chain-of-Thought**
```python
prompt = """
Step 1: Identify symptoms
Step 2: Determine root cause
Step 3: Recommend actions
Incident: {incident}
"""
# Encourages step-by-step reasoning
```

**Comparison Chart:**

| Technique | Quality | Parseability | Recommended |
|-----------|---------|--------------|-------------|
| Basic | 6/10 | N/A | No |
| Role | 8/10 | N/A | Yes |
| Structured | 8/10 | 10/10 | ✅ YES |
| Few-Shot | 9/10 | 10/10 | Yes |
| CoT | 8/10 | 6/10 | Yes |

**Why Structured Output Wins:**
1. Returns valid JSON (100% parseable)
2. Forces LLM to structure thinking
3. Eliminates hallucination
4. Enables automation

**Interactive Demo:**
"Let's send the SAME incident through all 5 prompts and compare outputs."

---

### SECTION 5: Building the Core Function (10 min)

**Key Teaching Points:**
1. Encapsulation: Put API calls in reusable functions
2. Error handling: Always use try-except
3. JSON parsing: Handle parsing failures gracefully
4. Documentation: Clear docstrings

**Code Walkthrough:**
```python
def analyze_incident(incident_description: str) -> Dict:
    """
    Analyze a single IT incident using OpenAI API.
    
    Args:
        incident_description: Text description of incident
    
    Returns:
        Dict with analysis results
    """
    try:
        # 1. Format the prompt
        prompt = prompt_best.format(incident=incident_description)
        
        # 2. Call API
        response = call_openai_api(prompt)
        
        # 3. Parse JSON
        result = json.loads(response)
        result['status'] = 'success'
        
        return result
    
    except json.JSONDecodeError:
        # Handle parsing failures
        return {'error': 'JSON parse error', 'raw': response}
    
    except Exception as e:
        # Handle other errors
        return {'error': str(e)}
```

**Key Principles:**
1. **Error handling** - Always wrap API calls
2. **Type hints** - Make inputs/outputs clear
3. **Docstrings** - Explain what function does
4. **Return consistent structure** - Always return Dict

**Discussion:**
"Why is error handling important? What could go wrong?"

---

### SECTION 6: Batch Processing (15 min)

**Key Teaching Points:**
1. Rate limiting - APIs have quotas
2. Progress tracking - Show what's happening
3. Retry logic - Handle transient failures
4. Cost tracking - Know what you're spending

**Code Walkthrough:**
```python
def process_incidents_batch(incidents_df, max_incidents=None):
    results = []
    incidents_to_process = incidents_df.head(max_incidents)
    
    for idx, (_, row) in enumerate(incidents_to_process.iterrows(), 1):
        # 1. Show progress
        print(f'[{idx}/{total}] Processing...', end=' ')
        
        # 2. Analyze incident
        analysis = analyze_incident(row['incident_description'])
        
        # 3. Collect results
        result = {
            'incident_id': row['incident_id'],
            'analysis': analysis,
            'timestamp': datetime.now()
        }
        results.append(result)
        
        # 4. Rate limiting - wait between calls
        time.sleep(1.0)  # 1 second delay
        
        print('✓')
    
    return results
```

**Rate Limiting Strategy:**
- API tier 1: 10 requests/minute → 6 second delay
- API tier 2: 100 requests/minute → 0.6 second delay
- API tier 3: 3,500 requests/minute → 0.02 second delay

**Cost Awareness:**
- Each request costs money
- 100 incidents × $0.002 = $0.20
- 1,000 incidents = $2.00
- 10,000 incidents = $20.00

**Demo Calculation:**
"We're processing 10,000 incidents. Each costs $0.002. Total cost: $20."

---

### SECTION 7-9: Running the Application (20 min)

**Key Teaching Points:**
1. End-to-end pipeline from data to results
2. Results look professional and actionable
3. Export to multiple formats
4. Quality metrics

**Live Demo:**
1. Run Section 7 (shows 3 sample incidents being processed)
2. Run Section 8 (display pretty results)
3. Run Section 9 (export to CSV and JSON)

**Expected Output:**
```
[1/3] Processing INC-001... ✓
[2/3] Processing INC-002... ✓
[3/3] Processing INC-003... ✓

✓ Batch processing complete: 3 incidents analyzed
```

**Results Display:**
```
Incident ID: INC-001
Application: CRM
Priority: High

Original: Database connection pool exhaustion...

AI Analysis:
  Summary: Database connection pool exhaustion preventing user access
  Root Cause: Insufficient pool size or query performance issues
  Impact: All users unable to access CRM
  Urgency: critical
  Next Actions:
    • Check connection pool settings
    • Review slow query log
    • Monitor for leaks
```

**Discussion:**
- "Does this analysis look reasonable?"
- "Are the next actions actionable?"
- "How would a human analyze this differently?"

---

### SECTION 10-13: Analysis, Costs & Deployment (30 min)

**Key Teaching Points:**
1. Quality metrics - Success rate, distribution
2. Cost economics - Cost per incident, ROI
3. Production patterns - How to deploy at scale
4. Continuous improvement - How to get better over time

**Quality Metrics Discussion:**
```
Processing Statistics:
  Total: 3
  Success: 3
  Errors: 0
  Success Rate: 100%

Urgency Distribution:
  critical: 2
  high: 1
```

"This is a small sample, but in production, track these metrics continuously."

**Cost Analysis (Live Calculation):**

| Scenario | Incidents | Cost Per | Total |
|----------|-----------|----------|-------|
| Pilot | 100 | $0.002 | $0.20 |
| Small Org | 1,000 | $0.002 | $2.00 |
| Enterprise | 10,000 | $0.002 | $20.00 |
| Large Org | 100,000 | $0.002 | $200.00 |

**ROI Calculation (CRITICAL):**

```
Manual analysis time: 10 minutes per incident
Manual cost: 10 min × ($50/hour) / 60 = $8.33 per incident
AI analysis cost: $0.002 per incident
Net savings: $8.33 per incident
Break-even: Positive immediately

Conclusion: Massive ROI from day 1
```

**Production Deployment Patterns:**

**Pattern 1: Batch Processing (Recommended)**
- Process incidents daily/weekly
- 10,000 incidents per run
- Cost: $20 per run
- Best for: IT operations that can batch

**Pattern 2: Real-Time API**
- Process incidents as they arrive
- Integration with service desk
- On-demand analysis
- Best for: Critical incidents needing immediate analysis

**Pattern 3: Hybrid**
- Real-time for critical incidents
- Batch for medium/low priority
- Optimizes cost vs speed

**Deployment Checklist:**
```
- [ ] Set API key in environment
- [ ] Implement error handling
- [ ] Add rate limiting
- [ ] Monitor costs
- [ ] Store results in database
- [ ] Set up logging
- [ ] Test on sample data
- [ ] Validate output quality
- [ ] Document integration
- [ ] Train users
```

**Discussion Questions:**
- "Which deployment pattern fits your organization?"
- "What's your incident volume?"
- "How would you integrate with existing tools?"

---

## ASSESSMENT & RUBRIC

### Participation Rubric (20 points)

| Criteria | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Engagement | Asks thoughtful questions, follows along | Pays attention, takes notes | Somewhat distracted | Not engaged |
| Collaboration | Helps others, shares insights | Works independently | Minimal interaction | No participation |
| Experimentation | Tries extensions, modifies code | Runs provided code | Follows steps mechanically | Doesn't engage |
| **Points** | **20** | **15** | **10** | **0** |

### Knowledge Rubric (30 points)

**Question 1:** "Explain why we use structured JSON output in prompts." (10 points)
- ✅ Excellent (10): Mentions parseability, automation, reduces hallucination
- ✅ Good (7): Explains it enables downstream processing
- ⚠️ Fair (4): Mentions JSON but doesn't explain why it matters
- ❌ Poor (0): Incorrect or no answer

**Question 2:** "What's the cost to analyze 5,000 incidents?" (10 points)
- ✅ Excellent (10): Calculates correctly and explains assumptions
- ✅ Good (7): Gets close to correct answer ($10)
- ⚠️ Fair (4): Attempts calculation but makes errors
- ❌ Poor (0): Wrong or no attempt

**Question 3:** "Describe the batch processing flow." (10 points)
- ✅ Excellent (10): Includes loading, looping, API calls, error handling, export
- ✅ Good (7): Covers main steps
- ⚠️ Fair (4): Describes some steps
- ❌ Poor (0): Incorrect or incomplete

### Application Rubric (50 points)

**Coding Challenge:** "Modify the notebook to analyze 10 incidents instead of 3"

| Criteria | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Correctness | Code runs without errors | Minor issues that don't prevent execution | Several errors | Code doesn't run |
| Understanding | Changes show deep understanding | Understands the changes | Follows examples mechanically | Doesn't understand what changed |
| Results Quality | Output is properly formatted and complete | Most results are correct | Some results are missing or incorrect | Results are completely wrong |
| **Points** | **50** | **35** | **20** | **0** |

---

## COMMON STUDENT MISTAKES

### Mistake 1: Wrong API Syntax
**What students do:**
```python
response = client.responses.create(...)  # ❌ WRONG
```

**What you should see:**
```python
response = client.chat.completions.create(...)  # ✅ RIGHT
```

**How to teach it:**
"The responses module doesn't exist. Chat API is the right endpoint. Show the OpenAI documentation."

### Mistake 2: Not Setting API Key
**Error:** `"openai.error.AuthenticationError"`

**Solution:**
```python
os.environ['OPENAI_API_KEY'] = 'your-key'
```

**Prevention:** Check setup before lab starts

### Mistake 3: Parsing Non-JSON Responses
**Problem:** LLM returns text instead of JSON

**Solution:** Add error handling:
```python
try:
    result = json.loads(response)
except json.JSONDecodeError:
    # Fall back to raw response
    result = {'raw': response}
```

### Mistake 4: Not Handling Rate Limits
**Error:** Too many API requests → gets blocked

**Solution:** Add delay:
```python
time.sleep(1.0)  # Wait 1 second between calls
```

### Mistake 5: Underestimating Costs
**Mistake:** "10,000 incidents won't cost much"

**Reality:** 10,000 × $0.002 = $20

**Prevention:** Do cost calculation early

---

## DISCUSSION TOPICS

### 1. Prompt Quality
**Discussion:** "Why does the prompt we chose (structured + role + CoT) work better?"

**Key Points:**
- Role establishes context
- Structured output enables parsing
- Chain-of-thought encourages reasoning

### 2. Hallucination & Errors
**Discussion:** "When would the AI get the root cause wrong?"

**Examples:**
- Insufficient incident context
- Ambiguous descriptions
- False patterns from training data

**Prevention:**
- Detailed incident descriptions
- Validation rules
- Human review for critical incidents

### 3. Privacy & Security
**Discussion:** "What if incidents contain sensitive data?"

**Solutions:**
- Redact PII before sending to API
- Use self-hosted models if needed
- Compliance with data regulations (GDPR, HIPAA)

### 4. Continuous Improvement
**Discussion:** "How do we make the system smarter over time?"

**Strategies:**
- Collect feedback on analyses
- Measure accuracy on known outcomes
- Retrain/optimize prompts
- A/B test different approaches

### 5. Integration Challenges
**Discussion:** "How do we connect this to our existing systems?"

**Integration Points:**
- Jira/ServiceNow API
- Slack notifications
- Email alerting
- Dashboard visualization

---

## HANDS-ON EXERCISES

### Exercise 1: Modify the Prompt (10 min)
"Change the prompt to also ask for 'time_to_resolve' estimate."

**Solution:**
```python
prompt = """
...existing prompt...
"time_to_resolve": "estimated minutes to resolve"
}
"""
```

### Exercise 2: Add a Custom Field (15 min)
"Add 'affected_systems' field to capture all systems impacted."

**Solution:**
```python
prompt = """
...
"affected_systems": ["system1", "system2"]
...
"""
```

### Exercise 3: Process More Incidents (10 min)
"Change max_incidents from 3 to 10. What's the cost?"

**Solution:**
- Cost: 10 incidents × $0.002 = $0.02
- Time: ~30 seconds to 1 minute

### Exercise 4: Export Analysis (10 min)
"Load the exported CSV and calculate average urgency score."

**Challenge:** Analyze the results programmatically

---

## CLOSING ACTIVITY

### Group Discussion: "What's Next?"

**Questions to Ask:**
1. "How would you integrate this into your IT operations?"
2. "What other data could we enrich with GenAI?"
3. "What concerns do you have about this approach?"
4. "How would you measure success?"

**Recording Student Ideas:**
- Capture on whiteboard/virtual board
- Discuss feasibility and ROI
- Identify next steps for real-world adoption

### Next Labs in Sequence:
- **Lab 03:** Advanced Prompt Engineering (few-shot, chain-of-thought at scale)
- **Lab 04:** Building a Multi-Agent System (multiple AI models working together)
- **Lab 05:** Deploying to Production (containerization, scaling, monitoring)

---

## MATERIALS CHECKLIST

### Before the Lab
- [ ] Test notebook in environment (run all cells)
- [ ] Verify datasets are available
- [ ] Confirm API access and limits
- [ ] Create sample OpenAI account for demo
- [ ] Set up backup demo video (in case API issues)
- [ ] Prepare slides with discussion questions
- [ ] Print handouts (README, prompt engineering guide)

### During the Lab
- [ ] Display notebook on screen
- [ ] Have technical support available
- [ ] Monitor student questions and issues
- [ ] Adjust pace based on comprehension
- [ ] Keep track of time allocation

### After the Lab
- [ ] Collect feedback from students
- [ ] Note common issues for next time
- [ ] Share recorded session (if applicable)
- [ ] Provide follow-up resources and next steps
- [ ] Answer follow-up questions

---

## FAQ FOR INSTRUCTORS

**Q: What if students don't have API keys?**
A: Use a shared demo account or provide sample outputs ahead of time.

**Q: What if API calls fail during demo?**
A: Have sample outputs saved. Walk through the code without live execution.

**Q: Is this too advanced for beginners?**
A: Yes, requires comfort with Python and APIs. Recommend prerequisite on Python basics.

**Q: Can we use a different LLM?**
A: Yes! Code works with Claude API with minor modifications. Great comparison exercise.

**Q: How do we teach prompt engineering?**
A: Show different prompts, run them, compare outputs. Live experimentation is key.

**Q: What about ethical concerns?**
A: Great discussion point. Address bias, hallucination, data privacy.

---

## REFERENCE: OPENAI API PARAMETERS

### Temperature (0 to 2)
- 0 = Deterministic (best for analysis)
- 0.7 = Balanced (default, recommended)
- 1.0+ = Creative (not for incident analysis)

### max_tokens
- Small (100-200) = Quick, cheap, concise
- Medium (500) = Default, recommended
- Large (2000+) = Very detailed responses

### top_p (0 to 1)
- Lower = More focused
- Higher = More diverse
- Generally leave at default (1.0)

---

## SUMMARY FOR INSTRUCTORS

This lab is **production-grade**, **immediately applicable**, and **highly engaging**. Students learn:
- Real-world GenAI application development
- Practical prompt engineering
- API integration and batch processing
- Cost analysis and ROI calculation
- Deployment strategies

The lab solves a **real business problem** (incident summarization) with immediate **ROI** and **scalability**.

**Teaching focus:** Live coding + discussion + experimentation

**Success indicator:** Students can explain why structured JSON output matters and calculate ROI for their organization.

---

**Happy Teaching! 🚀**
