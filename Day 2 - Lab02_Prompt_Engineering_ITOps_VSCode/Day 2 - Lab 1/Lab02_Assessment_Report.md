# LAB 02 ASSESSMENT REPORT
## Build an AI-Powered IT Incident Summarization Assistant

**Assessment Date:** August 2, 2026  
**Status:** ⚠️ **PARTIAL** - Datasets & Structure Ready, Application Incomplete

---

## REQUIREMENT SPECIFICATION

The lab asks learners to build a **simple GenAI application** that:

### Core Requirements ✅ 🔴
1. ✅ Use OpenAI API to build GenAI application
2. ✅ Automatically summarize IT incident tickets
3. ⚠️ Send incident data to LLM (Framework present, not implemented)
4. ✅ Generate concise summaries (Prompts shown, not tested)
5. ✅ Identify root causes (Prompts shown, not tested)
6. ✅ Produce recommended next actions (Prompts shown, not tested)
7. ✅ Help IT support teams resolve issues faster
8. ✅ No tool calling or RAG
9. ❌ **Simple GenAI Application** (Prompt comparison notebook, not a complete app)

### Deliverables Status
- **Notebook (Lab02_Prompt_Engineering_ITOps_Detailed.ipynb):** ⚠️ PARTIAL
- **Incident Dataset 1 (sample_incidents_10000.csv):** ✅ EXCELLENT
- **Incident Dataset 2 (it_incident_dataset_genai_25000.csv):** ✅ EXCELLENT

---

## DETAILED ANALYSIS

### ✅ STRENGTHS: High-Quality Datasets

#### Dataset 1: sample_incidents_10000.csv
- **Records:** 10,000 IT incidents
- **Columns:** 12 fields including:
  - incident_id, incident_datetime, application_name
  - infrastructure_component (Web Server, Database, Kubernetes, etc.)
  - incident_category (Availability, Performance, Security, Storage, etc.)
  - priority (Low to Critical)
  - region (US-West, US-East, APAC, Europe, MEA, India)
  - incident_description (100-200 words describing the issue)
  - assigned_team, status, resolution_required

**Data Quality:**
- No missing values evident
- Real-world incident patterns (repeatable descriptions with variations)
- Multiple categories and priorities
- Geographic distribution
- Realistic incident types and descriptions

**Example Incident:**
```
Incident: Database connection pool exhaustion detected for Payroll
Described as: Database transactions timing out, users cannot complete requests
Category: Performance/Availability
Priority: High
Infrastructure: Database/Kubernetes/Application
Root Cause: Query latency increased significantly
Impact: Service degradation, SLA breach
```

#### Dataset 2: it_incident_dataset_genai_25000.csv  
- **Records:** 1,250 incidents
- **Columns:** 8 fields:
  - incident_id, service_name, incident_type
  - priority, region, incident_description
  - status, resolution_required

**Data Quality:**
- Cleaner schema (fewer fields)
- Focused on common incident types
- High variation in descriptions
- Good for batch testing

**Good for:**
- Testing LLM performance on varied incident types
- Batch processing demonstrations
- Testing prompt robustness

---

### ⚠️ WEAKNESSES: Incomplete Application Implementation

#### Issue 1: API Syntax Error 🔴 CRITICAL

**Current Code:**
```python
response = client.responses.create(model="gpt-4.1-mini", input=prompt)
print(response.output_text)
```

**Problems:**
- `client.responses.create()` - WRONG (not an OpenAI API method)
- `input=prompt` - WRONG parameter
- `response.output_text` - WRONG attribute
- Model name "gpt-4.1-mini" - INCORRECT (current model is gpt-4o-mini)

**Correct Syntax:**
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=500
)
print(response.choices[0].message.content)
```

**Impact:** All code cells will FAIL when executed. This is a blocking issue.

---

#### Issue 2: No Complete Application Implementation 🔴 CRITICAL

**Current Notebook Structure:**
- Section 1: Basic Prompting (single incident hardcoded)
- Section 2: Role Prompting
- Section 3: Goal Prompting
- Section 4: Context Prompting
- Section 5: Structured Prompting
- Section 6: Executive Tone Prompting
- Section 7: Zero-shot Prompting
- Section 8: Few-shot Prompting
- Section 9: JSON Prompting
- Section 10: Comparison Exercise (just lists techniques)

**Missing - Complete Application:**
```
❌ Data Loading
   - No code to load incident CSVs
   - No DataFrame creation from incident data
   - No data validation

❌ Batch Processing
   - No loop to process multiple incidents
   - No batch API calls
   - No result collection

❌ Structured Output
   - No extraction of summary, root cause, next actions
   - No JSON parsing from LLM responses
   - No result validation

❌ Pipeline
   - No end-to-end workflow
   - No incident → LLM → summary → storage flow
   - No demonstration of complete application

❌ Error Handling
   - No try-except blocks
   - No API error handling
   - No timeout management

❌ Results Management
   - No storage of summaries
   - No export functionality
   - No comparison of techniques on real data

❌ Demonstration
   - No working example of the assistant in action
   - No sample output showing summaries + root causes + actions
   - No proof that it actually works
```

---

#### Issue 3: Notebook Structure is Prompt Comparison, Not Application

**What It Is:** A showcase of different prompting techniques
**What It Should Be:** A working incident summarization assistant

**Current Flow:**
```
Hardcoded Incident
       ↓
9 Different Prompts
       ↓
9 Separate Responses
       ↓
"Observe the differences"
```

**Expected Flow:**
```
Load Incidents CSV
       ↓
Prepare Best Prompt
       ↓
Process Each Incident
       ↓
Extract & Structure Output
       ↓
Display Summaries + Root Causes + Next Actions
       ↓
Save Results
       ↓
"Application Complete - Demonstrating End-to-End"
```

---

## REQUIREMENT COVERAGE MATRIX

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Use OpenAI API | ⚠️ PARTIAL | Code present but has syntax errors |
| Summarize incidents | ⚠️ PARTIAL | Prompts shown, not tested on real data |
| Send data to LLM | ❌ | No CSV loading or data processing |
| Generate summaries | ⚠️ PARTIAL | Prompts designed but not executed |
| Identify root causes | ⚠️ PARTIAL | Prompts designed but not executed |
| Recommend next actions | ⚠️ PARTIAL | Prompts designed but not executed |
| No tool calling | ✅ | Correctly avoids RAG/tools |
| Simple GenAI App | ❌ | Prompt comparison notebook, not complete app |
| IT Support Value | ❌ | No demonstration of helping teams |
| Works on Real Data | ❌ | Hardcoded example only |

**Overall Coverage: 25-30%** (Concepts present, implementation missing)

---

## WHAT'S MISSING

### Must-Have (For Complete Application)

1. **Data Loading Module**
   ```python
   import pandas as pd
   
   df = pd.read_csv('sample_incidents_10000.csv')
   df_head = df.head(10)  # Show sample incidents
   ```

2. **Incident Summarization Function**
   ```python
   def summarize_incident(incident_description, client):
       """Send incident to LLM and get structured response"""
       prompt = f"""...structured prompt..."""
       response = client.chat.completions.create(
           model="gpt-4o-mini",
           messages=[{"role": "user", "content": prompt}]
       )
       return response.choices[0].message.content
   ```

3. **Batch Processing**
   ```python
   summaries = []
   for idx, row in df.iterrows():
       summary = summarize_incident(row['incident_description'], client)
       summaries.append({
           'incident_id': row['incident_id'],
           'original': row['incident_description'],
           'summary': summary
       })
   ```

4. **Results Collection & Display**
   ```python
   results_df = pd.DataFrame(summaries)
   results_df.to_csv('summarized_incidents.csv', index=False)
   
   # Display first few results
   for result in summaries[:3]:
       print(f"Incident: {result['incident_id']}")
       print(f"Summary: {result['summary']}\n")
   ```

5. **Best Prompt Selection**
   ```python
   # After testing 9 techniques, identify which works best
   # Then use ONLY that for the full batch
   best_prompt = """
   You are a senior IT incident analyst...
   
   Analyze this incident and provide:
   1. Summary (2-3 sentences)
   2. Root Cause (identified technical cause)
   3. Next Actions (3-5 recommended steps)
   
   Incident: {incident}
   """
   ```

6. **Structured Output Extraction**
   ```python
   # Parse LLM response into structured format
   summary_text = parse_response(response)
   structured_output = {
       'summary': extract_summary(summary_text),
       'root_cause': extract_root_cause(summary_text),
       'next_actions': extract_actions(summary_text)
   }
   ```

---

## SEVERITY ASSESSMENT

| Issue | Severity | Impact |
|-------|----------|--------|
| API syntax error | 🔴 CRITICAL | Code won't run at all |
| No data loading | 🔴 CRITICAL | Can't process real incidents |
| No batch processing | 🔴 CRITICAL | Not a scalable application |
| No complete workflow | 🔴 CRITICAL | Not demonstrating the application |
| Hardcoded example only | 🔴 CRITICAL | Can't process other incidents |
| No error handling | 🔴 CRITICAL | Production-unsafe |
| Prompt comparison only | 🟠 HIGH | Doesn't meet "build an application" requirement |

---

## VERDICT

### Current State: **⚠️ PARTIAL (25-30% Complete)**

**What Works:**
- ✅ Excellent incident datasets (10,000 + 1,250 samples)
- ✅ Good notebook structure and organization
- ✅ Clever prompt engineering examples (conceptually sound)
- ✅ Correct understanding of what needs to be done

**What's Broken:**
- 🔴 OpenAI API syntax errors (blocking)
- 🔴 No actual application - just prompt comparison
- 🔴 No data loading or processing
- 🔴 No batch incident handling
- 🔴 No structured output extraction
- 🔴 No complete end-to-end demonstration

### Gap to Production Readiness: **70-75%**

The notebook needs substantial implementation work to become a "simple GenAI application" that learners can run, test, and use to actually build an incident summarization assistant.

---

## RECOMMENDATIONS

### Priority 1: Fix API Syntax (Blocking)
- Replace all `client.responses.create()` with `client.chat.completions.create()`
- Use correct messages format
- Update model name to `gpt-4o-mini`
- Fix attribute access from `response.output_text` to `response.choices[0].message.content`

### Priority 2: Implement Complete Application
- Add CSV loading and initial data exploration
- Show 5 sample incidents from the dataset
- Select the best prompt from the 9 options (based on prompt engineering principles)
- Build batch processing loop
- Display 5 summarized incidents with all three components (summary, root cause, next actions)
- Export results to CSV

### Priority 3: Add Production Features
- Error handling and retry logic
- Cost tracking (tokens, API calls, estimated cost)
- Result validation
- Performance metrics
- Lessons learned from comparing techniques

### Priority 4: Enhanced Documentation
- Learning objectives for each section
- Explanations of why each technique matters
- Code comments explaining OpenAI API usage
- Best practices for production use

---

## TIME TO COMPLETION

- **Fix API errors:** 15 minutes
- **Add data loading:** 20 minutes
- **Implement batch processing:** 30 minutes
- **Add output extraction:** 20 minutes
- **Testing & refinement:** 30 minutes
- **Documentation:** 30 minutes

**Total: ~2.5 hours to make it production-ready**

---

## CONCLUSION

The lab has **excellent raw materials** (good datasets, sound prompting concepts) but is **incomplete as a "simple GenAI application."** It currently reads as a prompt engineering comparison notebook rather than a working incident summarization assistant.

**To fix:** Implement the complete end-to-end application that loads real incidents, processes them through the OpenAI API, and produces actionable summaries with root causes and next actions. This will transform it from a theoretical exercise to a practical tool.

**Recommendation:** Enhance the notebook with complete implementation before deployment to learners.

