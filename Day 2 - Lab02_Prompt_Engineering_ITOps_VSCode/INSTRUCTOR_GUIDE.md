# Lab 2 Instructor Guide
## Prompt Engineering for IT Infrastructure Operations Using OpenAI API

**Module:** Module 02 - Introduction of GenAI (4 hours)  
**Difficulty Level:** Intermediate  
**Prerequisites:** Python basics, familiarity with APIs, IT operations knowledge  
**Target Audience:** IT professionals, DevOps engineers, infrastructure specialists

---

## Table of Contents

1. [Lab Overview](#lab-overview)
2. [Learning Outcomes](#learning-outcomes)
3. [Time Allocation](#time-allocation)
4. [Prerequisites & Setup](#prerequisites--setup)
5. [Section-by-Section Teaching Guide](#section-by-section-teaching-guide)
6. [Quiz Answers & Rubric](#quiz-answers--rubric)
7. [Common Student Challenges](#common-student-challenges)
8. [Assessment Strategy](#assessment-strategy)
9. [Extension Activities](#extension-activities)
10. [Best Practices & Tips](#best-practices--tips)
11. [Troubleshooting Guide](#troubleshooting-guide)

---

## Lab Overview

### Purpose
This lab bridges the gap between GenAI theory and practical IT operations by having students build a real-world prompt-engineered assistant that solves actual infrastructure problems. Students experience how different prompting strategies directly impact model performance on production-like scenarios.

### Key Innovation
- **Real data**: 100 realistic infrastructure incidents with 11 operational metrics
- **Progressive complexity**: Starts with basic prompts, evolves to sophisticated prompt engineering
- **Hands-on experimentation**: Students compare prompt strategies side-by-side
- **Cost awareness**: Teaches students to track and optimize API usage
- **Practical architecture**: Shows transformer theory applied to concrete problems

### Lab Context in 4-Hour Module
```
00:00-00:30  → Introduction to Generative AI (Lecture)
00:30-01:00  → Transformer Architecture Deep-Dive (Lecture + Demos)
01:00-02:00  → LAB 2: Notebook Sections 1-5 (Hands-on)
02:00-02:45  → LAB 2: Exercises 1-5 (Practical experimentation)
02:45-03:15  → Quiz & Discussion (Assessment)
03:15-04:00  → Extension activities & Troubleshooting (Advanced topics)
```

---

## Learning Outcomes

By the end of this lab, students will be able to:

### Knowledge (Bloom's L1-2)
- ✓ Explain how transformers use self-attention to process sequences
- ✓ Describe the role of system messages in controlling model behavior
- ✓ Identify how context injection improves response quality
- ✓ Compare temperature settings and their effects

### Application (Bloom's L3)
- ✓ Apply prompt engineering techniques to real IT scenarios
- ✓ Build a functional GenAI assistant using OpenAI API
- ✓ Implement structured prompting (role + goal + context + examples)
- ✓ Optimize prompts for accuracy vs. creativity tradeoff

### Analysis (Bloom's L4)
- ✓ Compare effectiveness of different prompt strategies
- ✓ Analyze model outputs for accuracy and completeness
- ✓ Evaluate cost-effectiveness of API usage
- ✓ Diagnose why prompts fail or succeed

### Synthesis (Bloom's L5-6)
- ✓ Design custom prompts for new IT operations scenarios
- ✓ Create feedback loops to iteratively improve assistant
- ✓ Integrate GenAI into existing monitoring/alerting systems
- ✓ Develop domain-specific prompt templates for their organization

---

## Time Allocation

### Within the Lab (120 minutes)

| Section | Duration | Activity | Notes |
|---------|----------|----------|-------|
| **Notebook Setup** | 10 min | Installation, API key setup | Assist slower students |
| **Section 1: Intro to GenAI** | 10 min | Reading + Q&A | Quick recap from lecture |
| **Section 2: Transformers** | 10 min | Review architecture | Reference to slides |
| **Section 3: Setup & Load Data** | 10 min | Run cells, explore CSV | Check API connectivity |
| **Section 4: Prompt Engineering** | 20 min | Read templates, discuss patterns | Key teaching moment |
| **Section 5: Build Assistant** | 15 min | Walk through class, explain methods | Pause at each method |
| **Exercise 1: Incident Analysis** | 15 min | Students run + analyze output | Monitor API credits |
| **Exercise 2: Alert Triage** | 10 min | Run, discuss results | Compare outputs |
| **Exercise 3: Strategy Comparison** | 15 min | Experiment with prompts | This is WHERE learning happens |
| **Exercise 4: Data Analysis** | 10 min | Explore patterns | Quick visualization |
| **Exercise 5: Cost Report** | 5 min | Check usage | Budget awareness |
| **Quiz** | 15 min | Complete 5 questions | Individual assessment |
| **Debrief & Discussion** | 5 min | What worked? What didn't? | Capture insights |

**Total: ~145 minutes** (Allow flexibility for debugging)

---

## Prerequisites & Setup

### Student Prerequisites
- [ ] Python 3.7+ installed
- [ ] Jupyter Notebook or JupyterLab running
- [ ] Basic understanding of REST APIs
- [ ] Familiarity with CSV data and pandas
- [ ] Prior lecture on Transformers and GenAI fundamentals

### Lab Environment Setup

#### Option 1: Local Machine
```bash
# Clone lab materials
git clone <repo-url>
cd lab2-prompt-engineering

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install openai pandas numpy jupyter python-dotenv

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Start Jupyter
jupyter notebook
```

#### Option 2: Cloud Environment (Google Colab)
```python
# In first cell:
!pip install openai pandas numpy python-dotenv
from google.colab import userdata
import os

# Store API key securely
os.environ['OPENAI_API_KEY'] = userdata.get('OPENAI_API_KEY')
```

#### Option 3: Classroom Lab Setup (Recommended)
- Pre-configure lab machines with Python + Jupyter
- Create a shared `.env` file with valid API key
- Set spending limits on OpenAI account ($20-30 per class)
- Have backup API key in case of account issues

### Pre-Lab Checklist (Instructor)
- [ ] Test all notebook cells with your API key
- [ ] Verify CSV file loads correctly
- [ ] Set spending limit on OpenAI account
- [ ] Create shared class API key (NOT personal keys)
- [ ] Test video playback/screen sharing if online
- [ ] Download backup dataset in case API is down
- [ ] Prepare example outputs for demo
- [ ] Have troubleshooting script ready

### API Key Management
**IMPORTANT:** Never share personal API keys with students
- Create dedicated organization account with parent credit card
- Set up sub-accounts or team access if available
- Monitor usage daily: `curl https://api.openai.com/v1/account/usage`
- Recommend monthly budget: $50-100 for 20-30 students

---

## Section-by-Section Teaching Guide

### Section 1: Introduction to Generative AI (10 min)

#### Teaching Objectives
- Clarify what "generative" means (generates NEW content)
- Contrast with discriminative models
- Connect to IT operations use cases

#### Key Concepts to Emphasize

**Autoregressive Generation:**
```
"Incident on SRV-DB-01" → Model predicts → "shows high"
"Incident on SRV-DB-01 shows high" → Model predicts → "CPU"
"Incident on SRV-DB-01 shows high CPU" → Model predicts → "usage"
```
Each token is predicted one at a time, sequentially.

**Probabilistic Nature:**
- Not deterministic (unlike calculators)
- Same prompt can give different outputs
- Temperature controls this variability
- Useful for creative tasks, requires control for operational decisions

**Context Window:**
- GPT-3.5: ~4K tokens
- GPT-4: ~8K-128K tokens
- Each token ≈ 0.75 words
- Design prompts accordingly

#### Interactive Activity (5 min)
**"Guess the Next Token"**
- Show prompt: "Alert: High memory usage on SRV-APP-01. Possible cause:"
- Ask students to guess model's completion
- Run it (if API available) and compare
- Discuss why model chose that response

#### Common Misconceptions to Address
- ❌ "GenAI understands IT like a human engineer" → ✓ "It predicts patterns from training data"
- ❌ "GenAI always gives correct answers" → ✓ "Accuracy depends on prompting quality"
- ❌ "GenAI is just copying training data" → ✓ "It combines patterns in novel ways"

---

### Section 2: Transformer Architecture (10 min)

#### Teaching Objectives
- Explain self-attention mechanism at conceptual level
- Show how attention enables parallel processing
- Connect architecture to prompt engineering implications

#### Key Concepts to Emphasize

**Self-Attention in Plain English:**
```
Query: "What is causing high CPU?"
Keys:   [memory issues, high load, inefficient code, network problem]
Values: [disk bottleneck, concurrent requests, unoptimized SQL, latency]

Attention asks: Which keys are relevant to my query?
→ Scores: [0.1, 0.8, 0.9, 0.3]
→ Selects values: [concurrent requests, unoptimized SQL]
→ These are attended to most
```

**Why Transformers Work for Prompting:**
1. **Parallel processing** = fast inference (vs RNNs)
2. **Long-range dependencies** = understands full context (vs CNNs)
3. **Attention weights** = can explain what it's focusing on
4. **Scalability** = trained on massive datasets

**Positional Encoding Important Insight:**
```
"Service failed then restarted" ≠ "Restarted then service failed"
Positional encoding captures this difference
This is why prompt ORDERING matters!
```

#### Visual Learning Aid
Draw on whiteboard/screen:
```
Token 1: "Alert"     ←→ (Self-attention to all tokens)
Token 2: "High CPU"  ←→ (Learns relationships)
Token 3: "on Server" ←→ (Understands context)
Token 4: "X"         ←→ (Predicts next token)

All processed in PARALLEL (not sequentially like RNN)
```

#### Connection to Prompt Engineering
- **Order matters**: Put most important info first
- **Attention to context**: Include all relevant details
- **Length considerations**: Longer context = more computation
- **Clarity helps**: Simple language gets better attention

---

### Section 3: Setup & Data Loading (10 min)

#### Pre-Cell Checklist
Run each cell with students, pause after each:

```python
# Cell 1: Installations
```
**What to watch for:**
- Network issues blocking pip (corporate firewall?)
- Version conflicts (openai version must be >= 1.0)
- Show progress bar, takes ~30 seconds

```python
# Cell 2: API Connection Test
```
**Demo point:** If API fails here:
- Check internet connectivity
- Verify API key format (should be `sk-...`)
- Test with curl: `curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models`

```python
# Cell 3: Load CSV Data
```
**Discussion points:**
- What do 11 columns represent? (Ask students)
- Why 100 rows? (Realistic but manageable)
- Spot check data quality: "Why is this error message generic?"
- **Teaching moment:** Real data is messy! Let's see pattern analysis

#### Data Exploration Talking Points

**"Why these specific metrics?"**
- CPU/Memory/Disk = Resource utilization (golden signals)
- Network latency = Performance impact
- Error message = Root cause hints
- Status = Incident lifecycle
- Service = Blast radius assessment

**"What patterns do you notice?"**
Facilitate discussion:
- Are critical alerts associated with high resource usage?
- Do certain services fail together?
- What's the distribution of resolution times?

---

### Section 4: Prompt Engineering Strategies (20 min)
**This is the CORE of the lab. Spend time here!**

#### 4.1: System Messages (8 min)

**Conceptual Understanding:**
```
System Message = "Here's who you are and how you should behave"
User Message   = "Here's the specific task"
```

**Why it matters:**
- Sets the expertise level
- Defines output format
- Establishes personality/tone
- Controls scope of reasoning

#### Teaching Activity: System Message Deconstruction
Show the three system messages side-by-side:

```markdown
## Basic (❌ Don't use)
"You are a helpful IT support assistant."

## Better (✓ Use this)
"You are an expert IT infrastructure engineer with 15 years of experience..."

## Best (✓✓ Recommended)
[Full system message with role, responsibility, output format]
```

**Ask students:** "What's the difference between these? Which would YOU trust with a critical incident?"

#### Key Principles to Teach
1. **Role definition**: "Expert with 15 years" > "Helpful assistant"
2. **Output structure**: Specify exactly how to format responses
3. **Constraints**: What should the model NOT do?
4. **Scope**: IT infrastructure, not general knowledge

#### Hands-On Activity (5 min)
**Have students write their own system message** for "Database Performance Specialist":
- Should include: role, expertise, responsibilities, output format
- Share 2-3 examples with class
- Compare to provided template
- Discuss differences

---

#### 4.2: Context Injection (7 min)

**The Problem:**
```
Model doesn't know:
- What "normal" CPU usage is (50% normal? 80%?)
- How services depend on each other
- Your company's escalation procedures
```

**The Solution: Inject Context**
```
User query: "CPU is at 85%, memory at 75%, what's the issue?"

With context:
- Normal baseline: CPU 40-60%, Memory 50-70%
- Service map: API depends on Database
- Policy: CPU >80% = High severity

Now model can reason properly!
```

#### Interactive Demo: Context Effect
**Side-by-side comparison:**
```
WITHOUT context:
"CPU at 85% seems high, recommend monitoring"
(Generic, not actionable)

WITH context:
"CPU at 85% is 42% above baseline, 
likely impacting API service. 
High severity, escalate to DBA."
(Specific, actionable, follows policy)
```

**Key Teaching Point:** Context injection is often MORE important than the model size!

#### Context Templates Explained
Walk through each:
- **Infrastructure baseline**: What's "normal"?
- **Service dependencies**: Blast radius of failures
- **Escalation policy**: Who to notify when

**Ask:** "Why would each of these matter for incident analysis?"

---

#### 4.3: Few-Shot Prompting (5 min)

**The Principle:** "Learn from examples"

Show the 3 incident examples:
```
Example 1:
Incident: CPU spike to 95%, API response degraded
Root cause: Unoptimized query triggered connection storm
Action: Kill query, optimize SQL, implement pooling

Example 2:
Incident: Database replication lag exceeded 30s
Root cause: Network saturation during backup
Action: Stop backup, reschedule, implement bandwidth management
```

**Discussion:**
- "What pattern do you see?" (Identify root cause, then fix)
- "How does this shape the model's reasoning?" (Examples provide template)
- "Why 3 examples? Why not 1 or 10?" (2-3 is optimal; too many confuses, too few doesn't help)

**Key Insight:** Few-shot examples are like showing someone HOW to solve problems, not just WHAT to solve.

---

### Section 5: Building the Assistant (15 min)

#### 5.1: Class Architecture Walkthrough (10 min)

Display the `ITOperationsAssistant` class and walk through:

```python
class ITOperationsAssistant:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        # Initialize OpenAI client
        # Set up conversation history
        # Start cost tracking
```

**Design decision point:** "Why track costs?" 
→ Answer: Real-world constraint; can't be wasteful

```python
    def call_api(self, system_message, user_message, temperature, max_tokens):
        # This is the core method
        # Combines system + user message
        # Returns response + tracks tokens
```

**Pause here:** "What's the relationship between max_tokens and cost?"
→ More tokens = higher cost (linear relationship)

```python
    def analyze_incident(self, incident_data):
        # Composes full prompt:
        # system_message + context + examples + user_data
```

**Teaching moment:** "This is where all the prompt engineering comes together!"

#### 5.2: Method Demonstrations (5 min)

Show how different methods reuse the core `call_api()`:
- `analyze_incident()` = expert role + full context
- `interpret_logs()` = analyzer role + medium context
- `triage_alerts()` = triage role + minimal context

**Question:** "Why different levels of context? Why not maximum for all?"
→ Answer: Cost, context length limits, task complexity

#### Code Quality Teaching Points
- **Error handling**: Real API calls fail; catch exceptions
- **Modularity**: Each method has one responsibility
- **Extensibility**: Easy to add new methods (e.g., `predict_failure()`)
- **Monitoring**: Cost tracking is essential for production

---

### Section 6: Practical Exercises (45 min)

#### Exercise 1: Incident Analysis (15 min)

**Student Task:**
1. Run cell to load critical incident
2. Format incident data properly
3. Call assistant.analyze_incident()
4. Compare output to expected response

**Teaching during this exercise:**

**Before running:**
- "What do you expect the model to say?"
- "What information is crucial for analysis?"
- "How would YOU solve this incident?"

**After running:**
- "Did the output structure match the system message?"
- "Was the root cause correct?"
- "Would you act on this recommendation?"
- **Critical:** Point out any hallucinations or errors

**Common issues:**
- Output too generic: "This is why temperature=0.5 (deterministic)"
- Missing reasoning: "Context injection solved this"
- Wrong format: "System message defines structure"

**Success criteria:**
- ✓ Output matches expected format (5 sections from system message)
- ✓ Root cause identified
- ✓ Actionable recommendations provided
- ✓ Severity assessed correctly

---

#### Exercise 2: Alert Triage (10 min)

**Student Task:**
1. Load multiple alerts of different severities
2. Ask model to triage and route
3. Evaluate correctness of severity assignments

**Teaching during this exercise:**

**Key question:** "How does context about service dependencies change triaging?"

**Before:**
- "Which alert would you handle first?"
- "Why?"

**After:**
- "Did the model match your prioritization?"
- "Did it consider service dependencies?"
- "Which escalation decisions make sense?"

**Connection to theory:**
- This is where context + few-shot + role combination really shines
- Temperature=0.2 for consistency (we need reproducible triage)

**Business impact point:**
- Proper triage can reduce MTTR (Mean Time To Resolution) by 30-40%
- Costs thousands per minute in downtime
- This is why GenAI is valuable here

---

#### Exercise 3: Prompt Strategy Comparison (15 min)
**This is the MOST IMPORTANT exercise for learning**

**Student Task:**
Compare three strategies on same incident:
1. Basic system message (generic)
2. Role-defined (expert)
3. Full context injection (production)

**Teaching approach: Socratic method**

Ask students BEFORE showing output:
- "Predict: which will be most detailed?"
- "Which will be most actionable?"
- "Which will have best structure?"
- "Rank them 1-3"

Show outputs and discuss:
- Output quality: Which is better? Why?
- Token usage: More context = more tokens (cost impact)
- Accuracy: Which recommendation would you trust?

**Quantitative comparison:**
```
Strategy         | Tokens | Quality | Clarity | Actionability
Basic           |   245  |    2/5  |   2/5  |      1/5
Role-defined    |   387  |    4/5  |   3/5  |      4/5
Full context    |   623  |    5/5  |   5/5  |      5/5
```

**Cost analysis:** "Is the extra 236 tokens worth it?" → YES, for critical incidents!

**Key learning:** This demonstrates the prompt engineering tradeoff:
- More effort (longer prompt)
- Higher cost (more tokens)
- Better output (higher quality)

**Real-world consideration:** For high-volume triage, might use Strategy 1 to filter, then Strategy 3 for critical items.

---

#### Exercise 4: Data Analysis (10 min)

**Student Task:**
1. Explore infrastructure patterns
2. Answer: "What's the most common alert type?"
3. "Which service has most incidents?"
4. "Correlation between CPU and severity?"

**Teaching during this exercise:**

This is about **context for prompt engineering**:
- "Before we write prompts, we should understand our data"
- "Patterns in data → patterns in prompts"
- "If Database has most incidents, should we mention this in system message?"

**Connection back to theory:**
- This is why few-shot examples are valuable (drawn from your data patterns)
- Real data distributions matter for model reasoning

**Bonus analysis:**
- High CPU correlates with High/Critical severity?
- Certain error messages always appear together?
- Escalated incidents take longer to resolve?

These patterns should inform your prompts!

---

#### Exercise 5: Cost Report (5 min)

**Student Task:**
1. Call `assistant.get_cost_report()`
2. Understand pricing breakdown
3. Discuss implications

**Teaching during this exercise:**

**Reality check moment:**
- Show actual cost incurred (probably $0.50-$2.00 for lab)
- "For your organization with 1000 incidents/day..."
- Calculate: 1000 incidents × $0.02/incident = $20/day = $600/month

**Budget management:**
- Why you need cost controls
- Optimization strategies:
  - Use cheaper model (gpt-3.5-turbo vs gpt-4)
  - Reduce context size (context pruning)
  - Batch similar incidents
  - Use caching for repeated queries

**Career skill:** Cost-aware AI engineering is highly valued!

---

### Section 7: Quiz Assessment (15 min)

#### Quiz Administration

**Format:**
- 5 multiple-choice questions
- 3 minutes per question
- Individual work (no collaboration)
- Open-book (students can reference notebook)

**Grading:**
- Each question: 20 points
- Total: 100 points
- 70+ = Pass, 85+ = Excellent

#### Quiz Answer Key & Teaching Notes

**Question 1: "What is the primary mechanism that allows transformers to process sequences in parallel?"**

Correct Answer: **B) Self-attention mechanism**

Why this matters:
- RNNs must process token-by-token (sequential, slow)
- Transformers use self-attention on all tokens simultaneously
- This is THE key architectural advantage

Common misconception:
- Students might choose "Convolutional filters" (that's CNNs)
- Remind: Transformers are attention-based, not convolution-based

Teaching note: If student struggles, ask "How does token 4 know about token 1?" → Through attention mechanism

---

**Question 2: "In the attention formula Attention(Q,K,V), what does the temperature parameter control?"**

Correct Answer: **B) The randomness/creativity of responses**

Technical explanation:
```
Attention score before softmax = Query · Key / √d_k
Softmax is applied with temperature scaling:
softmax(score / temperature)

Temperature effects:
- 0.0 = Only highest probability token (deterministic)
- 0.7 = Balanced (default)
- 1.5+ = All tokens equally likely (random)
```

Practical implications:
- Incident analysis: Use low temperature (reliable, consistent)
- Brainstorming: Use high temperature (creative, diverse)

Common error: "Temperature controls token count" → No, that's max_tokens

Teaching point: Temperature is ONE of the most important prompt engineering levers!

---

**Question 3: "What is the primary benefit of few-shot prompting in IT operations?"**

Correct Answer: **B) Provides examples for the model to learn from**

Why in-context learning:
- Model learns from examples without retraining
- Shows expected format and reasoning style
- Dramatically improves accuracy on domain-specific tasks

Real example:
```
Few-shot example teaches: 
"When I see High CPU + High Memory, 
the cause is usually connection pool exhaustion"
```

This is NOT in the model's training data but you're teaching it now!

Misconception check:
- "It reduces costs" → Actually might increase (more tokens)
- "Eliminates system message" → No, they complement each other

Assessment variation: Ask "How would you adapt few-shot examples for payment processing alerts vs. database alerts?" → Shows deep understanding

---

**Question 4: "Which prompt engineering technique is most effective for incident root cause analysis?"**

Correct Answer: **B) Chain-of-thought with context injection**

Why this combination works:
- Chain-of-thought: "Let me reason through this step-by-step..."
- Context injection: "Here's your infrastructure baseline..."
- Together: Structured reasoning + informed decision making

The notebook doesn't explicitly call it "chain-of-thought" but the system message induces it:
```
"INCIDENT SUMMARY" → "ROOT CAUSE ANALYSIS" → "SEVERITY ASSESSMENT" → ...

This IS chain-of-thought! Step-by-step reasoning.
```

Why other options are wrong:
- A) Random sampling: No structure, unreliable
- C) Single-word prompts: Insufficient information
- D) No system message: Model defaults to unhelpful behavior

Teaching point: Notice how Exercise 3 demonstrated this (full context + role = best results)

---

**Question 5: "What is the role of positional encoding in transformer models?"**

Correct Answer: **B) Provide information about token positions in sequences**

Why positional information matters:
```
Without positional encoding:
"Service failed then restarted" 
= 
"Restarted then service failed"

Model would see same token set, but meaning is completely different!

Positional encoding preserves order:
Position 1: "Service"
Position 2: "failed"
Position 3: "then"
Position 4: "restarted"

This information is encoded in embeddings.
```

Practical implication for prompting:
- **Order matters in your prompts!**
- Put most important information first
- "Critical: high CPU AND database lag" should come before "Service is Database"

Why other answers are wrong:
- A) Compress model size: Wrong, embedding dimension is separate
- C) Speed up GPU: No, slightly adds computation
- D) Reduce overfitting: Unrelated to positional encoding

---

#### Quiz Difficulty Analysis

**Easy (Expected 90%+ correct):**
- Question 1: Core architecture concept

**Medium (Expected 70-80% correct):**
- Questions 2, 3, 4: Require connecting lecture to practical lab

**Hard (Expected 60-70% correct):**
- Question 5: Deeper mathematical concept

**Adjust scoring** if students struggle:
- If <50% get Q5 correct: Maybe it was too abstract
- If <70% get Q1 correct: Reteach self-attention

---

## Assessment Strategy

### Formative Assessment (During Lab)

**Observation checkpoints:**
- [ ] Students correctly load and explore data
- [ ] Students can articulate difference between system messages
- [ ] Students notice improvements in Exercise 3
- [ ] Students understand cost implications

**Discussion prompts:**
- "Why did the detailed prompt work better?"
- "When would you use temperature=0.2 vs 0.7?"
- "What context would you add for YOUR infrastructure?"

### Summative Assessment (After Lab)

**Quiz (40 points):**
- 5 questions × 4 points each
- Measures knowledge and application

**Lab Notebook Submission (60 points):**
- **Completeness (20 pts):** All exercises attempted
- **Correctness (20 pts):** Proper execution of code, valid API calls
- **Analysis (15 pts):** Insightful commentary on Exercise 3 results
- **Reflection (5 pts):** Summary of key learnings

### Rubric for Lab Notebook Analysis

**Excellent (18-20):**
- Thoughtful comparison of prompt strategies
- Identifies which technique made biggest impact
- Connects results back to theory
- Suggests improvements to prompts

**Good (15-17):**
- Compares different approaches
- Notes quality differences
- References lectures/concepts
- Minor gaps in explanation

**Satisfactory (12-14):**
- Recognizes some differences between strategies
- Attempts explanation
- Missing depth or connections to theory

**Needs Improvement (< 12):**
- Limited comparison
- Superficial analysis
- Doesn't connect to concepts

---

## Common Student Challenges

### Challenge 1: "My API key doesn't work"

**Symptoms:**
```
OpenAIError: AuthenticationError: Invalid API key
```

**Root causes & solutions:**
- [ ] Key has leading/trailing spaces: `key = key.strip()`
- [ ] Wrong environment variable name: Should be `OPENAI_API_KEY`
- [ ] Key expired: Check OpenAI dashboard
- [ ] Key not regenerated after viewing: Need to create new key
- [ ] Network firewall: Try VPN or check corporate proxy settings

**Prevention:**
- Provide pre-configured .env file
- Test API key before class starts
- Have backup key ready

**Troubleshooting script:**
```python
import os
from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key format: {api_key[:10]}...{api_key[-10:]}")

try:
    client = OpenAI(api_key=api_key)
    response = client.models.list()
    print(f"✓ Connected! Available models: {len(response.data)}")
except Exception as e:
    print(f"✗ Error: {e}")
```

---

### Challenge 2: "The model's output is wrong/nonsensical"

**This is actually a TEACHING OPPORTUNITY!**

**Symptoms:**
- Output doesn't match incident analysis structure
- Factually incorrect reasoning
- Recommends unsafe actions

**Root causes:**
1. **System message not followed:** Temperature too high (>0.8)
2. **Insufficient context:** Model doesn't understand infrastructure
3. **Poor prompt design:** Ambiguous or conflicting instructions
4. **Model hallucination:** Inventing facts that aren't supported

**Teaching approach:**
- This is where debugging and prompt engineering happens!
- Ask: "What did the system message say should happen?"
- Compare to actual output
- Identify what's missing or wrong
- Revise and retry

**Solution process:**
```python
# Run with lower temperature for debugging
response = assistant.call_api(
    system_msg,
    user_msg,
    temperature=0.1  # Debug mode: most deterministic
)

# If still wrong, add explicit instructions
better_system_msg = """...[original]...
IMPORTANT: You MUST output in exactly this format:
1. INCIDENT SUMMARY
2. ROOT CAUSE ANALYSIS
3. SEVERITY ASSESSMENT
Do NOT deviate from this structure."""
```

**Key learning:** This IS prompt engineering - iterative refinement!

---

### Challenge 3: "I don't understand the Transformer architecture"

**Symptoms:**
- "Why self-attention?"
- "How is this different from RNNs?"
- Confusion about positional encoding

**Teaching strategy:**
Don't teach mathematics, teach intuition!

**Analogy:** Self-attention is like reading comprehension
```
Read sentence: "The API returned an error because the cache was full"

Self-attention asks:
- "What does 'cache' refer to?"
- "Why did it fill up?"
- "Why does this cause API error?"

Model attends (focuses) to relevant relationships.
```

**Visual explanation:**
```
I attended to:
   API ←→ ERROR (related)
   Cache ←→ FULL (related)
   ERROR ←→ Cache (related)
   
Not as much:
   API ←→ CACHE (indirect)
```

**Why this matters for IT ops:**
- Alerts mention multiple symptoms (CPU, memory, latency)
- Self-attention learns which are related
- This is why transformers are good at analysis

**If still confused:**
- Skip mathematics
- Focus on practical: "System message + Context + Examples = Better output"
- That's enough for this lab

---

### Challenge 4: "I ran out of API credits"

**Prevention:**
- [ ] Set API spend limit on OpenAI account ($20 total)
- [ ] Monitor usage daily
- [ ] Warn students before running expensive operations
- [ ] Have backup key/budget

**If it happens:**
- Acknowledge the learning ("APIs have costs!")
- Switch to demo mode (show pre-saved responses)
- Use different API (Hugging Face free tier, local model)
- Discuss this is real concern in production

**Teaching moment:**
```
Each API call costs money:
- Reading prompt: ~$0.001
- Generating response: ~$0.002
- Total: ~$0.003-0.01 per call

With 1000 queries/day = $3-10/day = $90-300/month

This is why:
- You optimize prompts
- You reduce context size
- You cache results
- You choose right model size
```

---

### Challenge 5: "The CSV data looks unrealistic"

**This is EXCELLENT if students notice!**

**Student observation:** "Real infrastructure data is messier"

**Response:**
- ✓ Correct! This is simplified for teaching
- Point out simplifications:
  - No nested error traces
  - Timestamps are evenly spaced
  - No missing values
  - Error messages are generic

**Teaching opportunity:**
- "Real data preparation is 80% of ML work"
- "You'd spend time parsing, cleaning, deduplicating"
- "GenAI would help with unstructured logs"

**Extension:** "Bring real log data from your infrastructure"

---

## Extension Activities

### Extension 1: Custom Incident Scenario (30 min)

**Objective:** Students design and analyze their own incident

**Task:**
1. Create a realistic incident record (any values)
2. Describe expected root cause
3. Prompt the model to analyze
4. Compare model's analysis to expected answer
5. Refine prompt if model was wrong

**Example:**
```python
custom_incident = {
    'timestamp': '2024-08-02 15:45:00',
    'server': 'SRV-PAYMENT-01',
    'service': 'PaymentGateway',
    'cpu': 92,
    'memory': 88,
    'disk': 45,
    'latency': 250,
    'error': 'Transaction timeout'
}

# Format as incident summary
incident_text = f"""
Payment processing is timing out on {custom_incident['server']}
CPU: {custom_incident['cpu']}% (Baseline: 50%)
Memory: {custom_incident['memory']}% (Baseline: 60%)
Network Latency: {custom_incident['latency']}ms (Normal: 20ms)
Error: {custom_incident['error']}
"""

# What would YOU predict?
expected_cause = "Connection pool exhausted due to unusual traffic spike"

# Ask model
analysis = assistant.analyze_incident(incident_text)

# Compare and discuss
print(f"Expected: {expected_cause}")
print(f"Model said: [analysis]")
```

**Grading:**
- Realism of incident design
- Quality of expected cause
- Analysis of model performance
- Suggestions for prompt improvement

---

### Extension 2: Prompt Engineering Competition (45 min)

**Objective:** Students compete to write the best prompt

**Setup:**
1. Provide same incident to all students
2. Each student writes system message + context + examples
3. Submit prompt as text file
4. Instructor runs all prompts against incident
5. Grade based on output quality

**Evaluation criteria:**
- Conciseness: Fewest tokens while maintaining quality
- Accuracy: Best root cause analysis
- Clarity: Easiest to understand output
- Structure: Follows requested format

**Winning prompt gets:**
- Recognition in class
- Badge on lab submission
- Shared with next cohort as example

**This teaches:** Prompt engineering is a skill, improvable through practice

---

### Extension 3: Integration with Real Monitoring System (60 min)

**Objective:** Connect GenAI assistant to actual monitoring system

**Options:**
1. **Datadog/Prometheus:** Query real metrics, send to model
2. **Splunk:** Extract alerts, ask model for remediation
3. **Custom Python script:** Monitor local system, analyze with GenAI

**Example:**
```python
import psutil
from assistant import ITOperationsAssistant

# Get real system metrics
cpu = psutil.cpu_percent()
memory = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent

# Format as incident
incident = f"""
Real-time system status:
CPU: {cpu}%
Memory: {memory}%
Disk: {disk}%
"""

# Analyze
if cpu > 80:
    analysis = assistant.analyze_incident(incident)
    print(analysis)
    # In production: send alert to team
```

**Challenge:** Real systems have noise, false positives

**Learning:** Production GenAI is harder than lab exercises

---

### Extension 4: Multilingual Prompt Engineering (30 min)

**Objective:** Understand how language affects model behavior

**Task:** Translate incident description to another language, compare outputs

```python
incident_english = "High CPU and memory usage causing API timeouts"
incident_spanish = "Alto uso de CPU y memoria causando tiempos de espera de API"
incident_japanese = "CPU とメモリの高使用率により API のタイムアウトが発生しています"

# Analyze in each language
for lang, incident in [("English", incident_english), 
                       ("Spanish", incident_spanish),
                       ("Japanese", incident_japanese)]:
    analysis = assistant.analyze_incident(incident)
    print(f"{lang}:\n{analysis}\n")
```

**Findings:**
- Model behavior consistent across languages
- Some languages might be "stronger" in model (trained on more data)
- Implications for global IT teams

---

### Extension 5: Few-Shot Example Optimization (45 min)

**Objective:** Learn how examples affect accuracy

**Task:**
1. Start with 0 examples (no few-shot)
2. Add 1 example, test accuracy
3. Add 2nd example, test accuracy
4. Add 3rd example, test accuracy
5. Graph accuracy vs. number of examples

**What you'll find:**
```
Examples | Accuracy | Tokens | Cost
---------|----------|--------|------
0        |   60%    |  200   | $0.001
1        |   75%    |  350   | $0.002
2        |   88%    |  500   | $0.003
3        |   92%    |  650   | $0.004
4        |   92%    |  800   | $0.005  ← Diminishing returns!
5        |   91%    |  950   | $0.006  ← Actually getting worse!
```

**Insight:** Optimal few-shot examples ≈ 2-3 (not more!)

**Why?** Too many examples confuse the model's reasoning

---

## Best Practices & Tips

### Classroom Management

**Before Lab:**
- Print quick-reference card with API key, common errors, troubleshooting
- Set expectations: "You'll get errors, that's normal in data science"
- Pair up students if some have slower machines
- Have demo account for projection/teaching

**During Lab:**
- Circulate every 5-10 minutes
- When student asks question, answer with question: "What does the error say?"
- Use "strong pairing" (good + struggling student)
- Celebrate debugging: "Great troubleshooting!"
- Track common issues for later discussion

**Classroom Culture:**
- Normalize failures: "What error did you get? Cool, let's debug"
- Celebrate insight: "You noticed the model structure changed - good eye!"
- Encourage experimentation: "What if we tried X instead?"
- Create psychological safety: No stupid questions

### Pacing Strategies

**If ahead of schedule:**
- Run Extension activities
- Have students write custom incidents
- Deep dive into particular concepts
- Discuss real-world prompt engineering at their company

**If behind schedule:**
- Skip Exercise 4 (data analysis is least critical)
- Shorten Exercise 3 (use 2 strategies instead of 3)
- Pre-record Exercise 5 (cost analysis can be demo)
- Extend quiz time if needed

**Timing rule:** Prefer deep understanding over coverage!

### API Management Best Practices

**Cost control:**
```python
# Set hard limits
MAX_SPEND_PER_CLASS = 30  # dollars
MAX_TOKENS_PER_CALL = 1000

# Before API call:
if total_tokens > MAX_TOKENS_PER_CLASS / 0.002:
    raise Exception("Approaching budget limit")
```

**Monitoring script:**
```bash
#!/bin/bash
# Daily cost check
curl -s https://api.openai.com/v1/account/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.total_usage'
```

**Account setup:**
- Organization account (not personal)
- API key usage is tracked per key
- Create separate key for each class (easy audit trail)
- Delete old keys after semester

### Teaching Prompt Engineering Like An Expert

**Common mistake:** Reading prompt engineering guides sequentially

**Better approach:**
1. **Show output first:** "Look at this incident analysis"
2. **Ask question:** "Why is this better than basic prompt?"
3. **Reveal technique:** "Because of X prompt engineering technique"
4. **Deep dive:** Explain the technique
5. **Practice:** Have them apply it

This is **inductive learning** (examples → principles) vs. deductive (principles → examples). It's more effective!

**Golden rules:**
- ✓ Show don't tell
- ✓ Compare side-by-side
- ✓ Let students discover patterns
- ✓ Connect to student's domain
- ✓ Measure improvement quantitatively

### Grounding in Real-World Context

**Critical:** Students need to understand WHY this matters

**Connect to business impact:**
- "Every minute of downtime = thousands in lost revenue"
- "Poor incident analysis = wrong fix = more downtime"
- "GenAI can triage alerts 10x faster than human"
- "This skill is worth $150K+ salary in tech"

**Tell stories:**
- "I once spent 8 hours debugging wrong issue (bad analysis)"
- "GenAI caught the real cause immediately"
- "This lab could have saved me days"

**Show examples from real companies:**
- Google uses ML for incident prediction
- Netflix uses GenAI for debugging
- Meta has autonomous systems managing infrastructure

---

## Troubleshooting Guide

### Jupyter Notebook Issues

**Problem:** Kernel crashes or restarts unexpectedly
```
Solution:
1. Restart kernel: Kernel → Restart & Clear Output
2. Run setup cells again
3. Check if code is infinite loop or huge memory allocation
4. If persistent, restart JupyterLab process
```

**Problem:** Cells take a very long time to run
```
Solution:
1. It's normal for first cell (pip install)
2. API calls take 5-30 seconds - that's expected
3. If >60 seconds, check internet connection
4. Verify model exists: client.models.list()
```

**Problem:** Plot/visualization doesn't show
```
Solution: Add before plotting code:
%matplotlib inline
import matplotlib.pyplot as plt
```

---

### API Issues

**Problem:** "openai.error.RateLimitError: Rate limit exceeded"
```
Cause: Making requests too fast
Solution:
import time
for i in range(100):
    response = assistant.call_api(...)
    time.sleep(1)  # Wait 1 second between calls
```

**Problem:** "openai.error.APIConnectionError"
```
Causes:
1. Network timeout: Wait and retry
2. API outage: Check https://status.openai.com
3. Firewall blocking: Try VPN or different network

Solution: Implement retry logic
import time
max_retries = 3
for attempt in range(max_retries):
    try:
        return client.chat.completions.create(...)
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

**Problem:** "tokens = encode(prompt) # Exception"
```
Cause: Prompt too long for model's context window
Solution:
1. Check model limits: GPT-3.5 = 4K tokens
2. Reduce context size
3. Summarize old conversation history
4. Switch to longer-context model (GPT-4)
```

---

### Data Issues

**Problem:** CSV file not found
```
Solution:
import os
print(os.getcwd())  # Check current directory
print(os.listdir())  # List files in directory
# Make sure it_infrastructure_data.csv is in current directory
```

**Problem:** Pandas raises "DtypeWarning"
```
Cause: CSV data type inference
Solution:
df = pd.read_csv('it_infrastructure_data.csv')
# Usually safe to ignore, but if issues:
df = pd.read_csv(..., dtype={'Timestamp': str, 'CPUUsage(%)': int})
```

---

### Student Frustration Red Flags

**"This is too hard"**
→ Breakdown into smaller steps, pair with stronger student, offer office hours

**"This is too easy"**
→ Offer extensions: custom incidents, competition, real integration

**"Why are we doing this?"**
→ Reiterate business value, show real-world examples, discuss job market

**"My code doesn't work"**
→ Normalize debugging, treat as learning opportunity, don't just fix it for them

---

## Assessment Rubric Summary

### Quiz (100 points)
| Criteria | Poor | Fair | Good | Excellent |
|----------|------|------|------|-----------|
| Concept understanding | <50% | 50-70% | 70-85% | 85-100% |
| Connections to practice | Missing | Weak | Clear | Insightful |
| Technical accuracy | Multiple errors | Some errors | Mostly correct | Perfect |

### Lab Notebook (100 points)
| Criteria | Poor (0-40) | Fair (40-60) | Good (60-80) | Excellent (80-100) |
|----------|-------------|--------------|--------------|------------------|
| Completeness | Missing sections | Some sections incomplete | All sections present | Thorough, detailed |
| Code functionality | Many errors | Some errors | Works with minor issues | Perfect execution |
| Analysis quality | Superficial | Basic | Thoughtful | Deep insights |
| Prompt engineering insights | Limited | Adequate | Strong understanding | Mastery evident |

---

## Final Checklist for Instructors

### Before Lab
- [ ] API key tested and working
- [ ] Spend limit set on OpenAI account
- [ ] Notebook run-through completed
- [ ] Data file verified (100 rows, 11 columns)
- [ ] Backup plan if API is down
- [ ] Student handout prepared
- [ ] Troubleshooting guide printed
- [ ] Timer/clock visible to class

### During Lab
- [ ] Welcome and overview (2 min)
- [ ] Setup and API verification (5-10 min)
- [ ] Live-code through Section 5 (10 min)
- [ ] Circulate during Exercises (45 min)
- [ ] Collect observations of student work
- [ ] Quiz administration (15 min)
- [ ] Debrief and Q&A (10 min)

### After Lab
- [ ] Collect submissions
- [ ] Review quiz answers
- [ ] Calculate cost incurred
- [ ] Note areas for next iteration
- [ ] Prepare feedback for next session
- [ ] Archive successful prompts for next class

---

## References & Resources

### Documentation
- OpenAI API Docs: https://platform.openai.com/docs/api-reference
- OpenAI Cookbook: https://github.com/openai/openai-cookbook
- Prompt Engineering Guide: https://www.promptingguide.ai

### Papers
- "Attention is All You Need" (Vaswani et al., 2017) - Transformer paper
- "Language Models are Few-Shot Learners" (Brown et al., 2020) - GPT-3
- "Chain-of-Thought Prompting Elicits Reasoning" (Wei et al., 2022)

### Tools
- LangChain: Framework for LLM applications
- Prompt Fixer: Tool for debugging prompts
- OpenAI Playground: Interactive API testing

### Teaching Resources
- Bloom's Taxonomy for learning objectives
- Socratic method for teaching problem-solving
- Active learning strategies

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-08-02 | Initial instructor guide created |
| 1.1 | [Future] | Add video walkthrough links |
| 1.2 | [Future] | Include student testimonials |
| 1.3 | [Future] | Add follow-up lab exercises |

---

**Last Updated:** August 2, 2026  
**Author:** AI Training Curriculum  
**Contact:** [Your contact info]

For questions or suggestions, please reach out to the training team.

---

**Happy teaching! Remember: The best prompt engineering comes from understanding both the AI AND the business problem. Help your students see both.** 🚀
