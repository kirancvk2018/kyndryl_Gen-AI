# Module 6 Lab 2: Sequential LangChain Workflow - Deliverables

## Files

### Core lab files
| File | Purpose |
|------|---------|
| **module6_lab2_sequential_chain.ipynb** | Step-by-step notebook: prompts, chains, one request, all requests, report |
| **module6_lab2_corporate_ops.ipynb** | Shorter notebook that imports the functions in `ops_workflow.py` |
| **ops_workflow.py** | Plain functions: build the chains, run one request, format and save results |
| **data/ops_requests.json** | Five routine operations requests (fictional data) |
| **requirements_module6_lab2.txt** | Packages for both notebooks and the script |

### Documentation (folder docs/)
| File | Purpose |
|------|---------|
| **MODULE6_LAB2_README.md** | Guide: setup, workflow, functions, exercises, troubleshooting |
| **DELIVERABLES_SUMMARY.md** | This file |

---

## Quick Setup

```bash
pip install -r requirements_module6_lab2.txt
```

Put your key in `.env`:
```
OPENAI_API_KEY=your_key_here
```

Run the lab:
```bash
# Notebook
jupyter notebook module6_lab2_sequential_chain.ipynb

# Script (processes the first two requests)
python ops_workflow.py
```

---

## What the Lab Builds

A four-step chain for each request:

1. **Summary:** summary, category and priority
2. **Cause and blockers:** likely cause, blockers and confidence
3. **Business impact:** who is affected, impact if late, cost level and whether the deadline is at risk
4. **Action plan:** immediate, same-day and follow-up actions, each with an owner

The results are saved to **ops_analysis_results.json**.

---

## Code Structure

`ops_workflow.py` contains plain functions only:

- `build_chains(model_name, temperature)`
- `analyze_request(chains, request)`
- `format_report(result)`
- `load_requests(filepath)`
- `save_results(results, output_file)`

Prompt templates are plain strings. The data uses dictionaries and lists. The file has no classes and no Pydantic models.

---

## Learning Outcomes

- Build a sequential chain with LCEL: `prompt | llm | StrOutputParser()`
- Write a prompt template for each step
- Pass each step's output into the next step
- Run a chain on one request and on a batch
- Save the results to a JSON file

---

## Model and Requirements

- Model: `gpt-4o-mini` (set in `ops_workflow.py` and in both notebooks)
- LangChain versions are unchanged from the previous release
- Packages: see `requirements_module6_lab2.txt`
