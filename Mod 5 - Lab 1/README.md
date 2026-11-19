# Module 5 – Lab 1: Prompt Evaluation & Optimization Framework for Operations

## Lab overview

This lab is a small web application that teaches operations professionals how to improve GenAI output quality in a systematic way. Instead of trusting the first answer a prompt produces, participants:

1. Create several versions of a prompt.
2. Run the versions against the **same** business input.
3. Score each answer manually on four criteria.
4. Compare the average scores on a leaderboard.

Three business scenarios are included: **Incident Summarization**, **Ticket Classification** and **SOP Generation**.

No Python knowledge is needed to complete the lab. Everything is done in the browser.

## Learning outcomes

By the end of the lab, participants will be able to:

- Explain how prompt wording, role, context and output rules change the quality of an answer.
- Create and version prompts without losing earlier versions.
- Run a fair comparison by keeping the business input constant.
- Score responses with a consistent rubric (Groundedness, Intent Resolution, Relevance, Format Compliance).
- Use the evidence to choose the best prompt and decide what to improve next.

## Application architecture

The application is intentionally simple:

- **One Python file** (`app.py`) contains the whole Streamlit application.
- **Two CSV files** store all persistent data. No database is used.
- **Streamlit** provides the browser interface, the sidebar navigation, tables and charts.
- **OpenAI API** is called only in Live LLM Mode.
- **Session memory** keeps the responses generated during the current browser session, so that they can be evaluated.

```
Browser (Streamlit pages)
   │
   ├── Prompt Library ──────► prompt_versions.csv  (prompt catalogue, append-only)
   ├── Run & Compare ───────► OpenAI API (Live)  or  built-in demo answers (Demo)
   │                          └─► session memory (responses for evaluation)
   ├── Manual Evaluation ───► evaluation_results.csv
   └── Prompt Leaderboard ──► reads evaluation_results.csv and draws the charts
```

## File descriptions

| File | Purpose |
|---|---|
| `app.py` | The complete application: pages, business content, demo answers, CSV handling and leaderboard logic. |
| `prompt_versions.csv` | The prompt catalogue. Contains the nine sample prompt versions and every version created later. |
| `evaluation_results.csv` | One row per submitted evaluation. Starts with headers only (no pre-filled scores). |
| `requirements.txt` | The Python packages needed to run the application. |
| `.env.example` | Template for configuration (API key and model list). Copy it to `.env` to use Live LLM Mode. |
| `README.md` | This document (for trainers and technical readers). |
| `QUICKSTART.md` | Step-by-step guide for participants. |

If `prompt_versions.csv` or `evaluation_results.csv` is missing or empty, the application recreates it automatically.

## Prerequisites

- Python 3.9 or later, with `pip`.
- A web browser (Edge, Chrome or Firefox).
- For Live LLM Mode only: an OpenAI API key with available credit.

Demo Mode works without an internet connection or an API key.

## Technology stack

| Component | Technology |
|---|---|
| Language | Python |
| Web interface | Streamlit |
| Data storage | CSV files (pandas for reading and writing) |
| LLM integration | OpenAI Python SDK (Chat Completions) |
| Configuration | Environment variables, optionally read from `.env` (python-dotenv) |
| Charts | Streamlit charts and Altair (installed with Streamlit) |
| Execution | Local browser at `http://localhost:8501` |

## Installation and launch

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Application workflow

| Step | Page | What the participant does |
|---|---|---|
| 1 | Prompt Library | Chooses a scenario and reads the sample business input and objective. |
| 2 | Prompt Library | Views, edits (saved as a new version) or compares prompt versions. |
| 3 | Run & Compare | Selects at least two versions and runs them on the same input. |
| 4 | Manual Evaluation | Scores each response on four criteria (1–5) and adds comments. |
| 5 | Prompt Leaderboard | Reviews rankings, charts and the business interpretation. |

The **Home** page shows the workflow and highlights the next step based on the work done in the current session.

## Execution modes

**Demo Mode (default).** Each of the nine sample prompt versions has a pre-written answer. The answers are deliberately different in completeness, grounding, relevance and format, so that the evaluation shows a clear difference. They are illustrative and are labelled as such in the application. No API call is made.

**Live LLM Mode.** The selected prompt text and the business input are sent to the OpenAI model chosen in the sidebar. The model list comes from `OPENAI_MODELS` in `.env`. If the call fails (missing key, invalid key, rate limit, network error), the exact error is shown. The application never replaces a failed live call with a demo answer. The participant can then choose **Switch to Demo Mode** explicitly.

Prompt versions created by participants have no pre-written demo answer, so they can be run only in Live LLM Mode. In Demo Mode they are skipped with a message.

## CSV data structure

### `prompt_versions.csv`

| Column | Description |
|---|---|
| Prompt ID | Unique ID, built from the scenario code and version, e.g. `INC-V3`, `TKT-V2`, `SOP-V1`. |
| Scenario | Incident Summarization, Ticket Classification or SOP Generation. |
| Version Number | 1, 2, 3 … for each scenario. |
| Prompt Name | Short name of the prompt. |
| Prompt Text | The full instruction given to the model. |
| Business Objective | What the answer must achieve. |
| Created Date | Date the version was saved (YYYY-MM-DD). |
| Version Description | What is different in this version and why. |

Saving a change always **appends** a new row. Existing rows are never edited, so earlier versions remain available for comparison.

### `evaluation_results.csv`

| Column | Description |
|---|---|
| Evaluation ID | Unique ID for the evaluation (`EV-…`). |
| Execution ID | ID of the response that was scored (`EX-…`). |
| Prompt ID | Prompt version that produced the response. |
| Scenario | Business scenario. |
| Prompt Version | Version number, e.g. `V3`. |
| Groundedness | Score 1–5. |
| Intent Resolution | Score 1–5. |
| Relevance | Score 1–5. |
| Format Compliance | Score 1–5. |
| Average Score | (Groundedness + Intent Resolution + Relevance + Format Compliance) / 4, rounded to 2 decimals. |
| Evaluator Comments | Free text. |
| Evaluation Date | Date and time of the evaluation. |

## Evaluation methodology

Each response is scored by a person, not by an AI judge. Scores use a 1–5 scale for four criteria:

| Criterion | Question | 1 means | 5 means |
|---|---|---|---|
| Groundedness | Is the response faithful to the business input? | Major unsupported information | Fully grounded |
| Intent Resolution | Does it fulfil the business objective? | Does not address the requirement | Completely fulfils it |
| Relevance | Is it focused and useful to an operations user? | Mostly irrelevant | Directly relevant and actionable |
| Format Compliance | Does it follow the requested structure? | Ignores the format | Fully follows the format |

- **Average Score** = (Groundedness + Intent Resolution + Relevance + Format Compliance) / 4. All criteria carry equal weight.
- **Prompt average** = the mean of the Average Scores of all evaluations for that prompt version.
- **Ranking** orders prompts by their average, highest first. Prompts with the same average share a rank and are marked **(Tied)**.
- **Duplicate protection:** each response can be scored once. Changing a score later requires ticking "update the existing evaluation", which replaces that row and keeps its Evaluation ID.
- The leaderboard uses only evaluations that were actually submitted. It never invents scores.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `streamlit` is not recognised | Run `python -m streamlit run app.py` instead. Or reopen the terminal after installing. |
| `pip install` fails | Check the internet connection. Run `python -m pip install -r requirements.txt`. |
| The browser shows "No API key found" | Create `.env` from `.env.example` and add your key. Restart the application. |
| "AuthenticationError" in Live mode | The API key is wrong or has been revoked. Check the key in `.env`. |
| "RateLimitError" or "APIConnectionError" in Live mode | Too many requests, or no network access. Wait a minute, check the connection, or use Demo Mode. |
| Manual Evaluation says there are no responses | Responses exist only in the current browser session. Run prompts again in **Run & Compare**. |
| Old responses are missing after restarting the application | Responses are kept in session memory and are cleared when the application restarts. The **evaluation scores** are saved in `evaluation_results.csv` and are not lost. |
| Prompt Library or Leaderboard shows the wrong data | Stop the application, check that `prompt_versions.csv` and `evaluation_results.csv` are not open in Excel or damaged, then restart. Or use **Reset Sample Data**. |
| A custom prompt is skipped in Demo Mode | Demo Mode has answers only for the nine sample versions. Use Live LLM Mode to run new versions. |
| Port 8501 is already in use | Run `streamlit run app.py --server.port 8502` and open the new address. |

**Tip:** Do not edit the CSV files while the application is running. Use the application pages to make changes.
