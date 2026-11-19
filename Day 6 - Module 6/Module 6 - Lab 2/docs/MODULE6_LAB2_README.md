# Module 6 Lab 2: Sequential LangChain Workflow for Routine Corporate Operations

## Overview

This lab teaches you to build a **four-step sequential chain** with LangChain Expression Language (LCEL). The chain helps an operations team handle everyday requests: office supplies, building badges, equipment faults, vendor invoices and meeting room problems.

Each step is `prompt | llm | StrOutputParser()`. The output of one step goes into the prompt of the next step.

The code uses plain functions, dictionaries and JSON files. There are no classes and no Pydantic models.

**Four steps:**
1. **Summary:** what is being asked, its category and its priority
2. **Cause and blockers:** why the issue happened and what is stopping it
3. **Business impact:** who is affected and what happens if it is late
4. **Action plan:** next steps, each with an owner

---

## Files

```
Module 6 - Lab 2/
├── module6_lab2_sequential_chain.ipynb       # Main notebook (step by step, 7 parts)
├── module6_lab2_corporate_ops.ipynb          # Shorter notebook that uses ops_workflow.py
├── ops_workflow.py                           # Reusable functions (run as a script or import)
├── data/
│   └── ops_requests.json                     # Five sample operations requests
├── requirements_module6_lab2.txt             # Python packages
├── .env                                      # Your API key (keep private)
└── docs/
    ├── MODULE6_LAB2_README.md                # This guide
    └── DELIVERABLES_SUMMARY.md               # File list and learning outcomes
```

Running the notebook or script creates `ops_analysis_results.json`.

---

## Quick Start (5 minutes)

### Step 1: Install the packages
```bash
pip install -r requirements_module6_lab2.txt
```

### Step 2: Add your API key
Open `.env` in this folder and set the key on the `OPENAI_API_KEY=` line, with no spaces and no quotation marks:
```
OPENAI_API_KEY=sk-your-key-goes-here
```

### Step 3: Run the notebook
```bash
jupyter notebook module6_lab2_sequential_chain.ipynb
```

Or run the script. It processes the first two requests and saves the results:
```bash
python ops_workflow.py
```

---

## Sample Data

`data/ops_requests.json` holds five routine requests:

| Request ID | Type | Department |
|---|---|---|
| OPS-101 | Office supplies restock | Finance |
| OPS-102 | Building access badge | Procurement |
| OPS-103 | Equipment repair | Sales |
| OPS-104 | Vendor invoice exception | Facilities |
| OPS-105 | Meeting room AV fault | Executive Office |

Each request has: `request_id`, `request_type`, `requester`, `department`, `details` and `due_date`. The data is fictional. Do not add real employee, customer or financial records.

---

## Learning Path

### Option A: Notebook (recommended for beginners)
1. Open `module6_lab2_sequential_chain.ipynb`.
2. Run the cells from top to bottom.
3. Change a prompt, run the step again and compare the output.

### Option B: Script or import (for batch work)
```python
from ops_workflow import build_chains, analyze_request, format_report, load_requests, save_results

chains = build_chains(model_name="gpt-4o-mini", temperature=0.3)
requests = load_requests("data/ops_requests.json")

results = [analyze_request(chains, r) for r in requests]
for result in results:
    print(format_report(result))

save_results(results, "ops_analysis_results.json")
```

---

## How the Workflow Runs

```
Request (type, requester, details, due date)
    |
[Step 1: Summary]           -> summary, category, priority
    |  (passes summary on)
[Step 2: Cause & blockers]  -> likely cause, blockers
    |  (passes summary and cause on)
[Step 3: Business impact]   -> who is affected, impact if late
    |  (passes all of the above on)
[Step 4: Action plan]       -> next steps with owners and time targets
    |
Result saved to ops_analysis_results.json
```

---

## Functions in `ops_workflow.py`

| Function | What it does |
|---|---|
| `build_chains(model_name, temperature)` | Creates the four chains and returns them in a dictionary |
| `analyze_request(chains, request)` | Runs the four steps in order on one request and returns a dictionary |
| `format_report(result)` | Turns one result into a readable text report |
| `load_requests(filepath)` | Reads the list of requests from a JSON file |
| `save_results(results, output_file)` | Saves all results to a JSON file |

The four prompt templates are at the top of `ops_workflow.py` as plain strings: `SUMMARY_TEMPLATE`, `CAUSE_TEMPLATE`, `IMPACT_TEMPLATE` and `ACTION_TEMPLATE`.

---

## Configuration

| Setting | Value in the lab | Where to change it |
|---|---|---|
| Model | `gpt-4o-mini` | `build_chains(model_name=...)` in `ops_workflow.py`, or the `model=` line in the notebook |
| Temperature | `0.3` (steadier answers) | `build_chains(temperature=...)` |
| API key | from `.env` | `.env` |

---

## Concepts

### LCEL (LangChain Expression Language)
```python
chain = prompt | llm | StrOutputParser()
```
Each `|` passes the output of one component to the next.

### Prompt templates
Reusable instructions with placeholders such as `{details}` and `{summary}`. The answer format is written into the prompt, so each step returns text that is easy to read and easy to pass on.

### Sequential chains
Each step waits for the step before it. A later step can use the output of any earlier step.

---

## Exercises

1. Add a fifth step that lists the checks needed to confirm a request is closed.
2. Add a request type that fits your team, such as a room booking or a parking pass.
3. Compare the outputs at `temperature=0` and `temperature=0.7`.
4. Change the category list in the summary prompt to match your team's categories.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "OPENAI_API_KEY" not set, or 401 "Incorrect API key" | Check the `OPENAI_API_KEY=` line in `.env`. Copy the key again with no spaces |
| 404 or "model does not exist" | Set the model to `gpt-4o-mini` in the notebook or in `ops_workflow.py` |
| 429 or quota or billing errors | Your OpenAI account has no credit or has hit a limit. Ask your facilitator |
| "No module named ..." | Run `pip install -r requirements_module6_lab2.txt` again |
| `ops_analysis_results.json` was replaced | Running the script again overwrites the results file. Copy it first if you need the old results |

---

## Checklist

- [ ] Installed the packages from `requirements_module6_lab2.txt`
- [ ] Set `OPENAI_API_KEY` in `.env`
- [ ] Ran the notebook from top to bottom without errors
- [ ] Ran `ops_workflow.py` and saw `ops_analysis_results.json`
- [ ] Can explain how the `|` operator passes outputs along
- [ ] Changed one prompt template and saw the result change
- [ ] Attempted one exercise

---

## Next Steps

- **Lab 3:** a conversational chain for routine issues that need follow-up questions
- **Module 7 (RAG):** add company procedures and knowledge bases to the prompts
- **Module 8 (Agents):** let the workflow suggest actions that a person then approves

---

**Happy learning!**
