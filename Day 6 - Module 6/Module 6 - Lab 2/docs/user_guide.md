# Module 6 Lab 2 User Guide

*Sequential chains for routine corporate operations requests (version 2). Follow the steps in order. No programming experience is needed.*

## 1. What this lab does

This lab runs a four-step AI workflow on routine office and operations requests: supplies, building badges, equipment faults, vendor invoices and meeting room problems. Each step uses the answer from the step before it:

- **Summary:** what is being asked, its category and its priority.
- **Cause and blockers:** why the issue happened and what is stopping it.
- **Business impact:** who is affected and what happens if it is late.
- **Action plan:** next steps, each with an owner and a time target.

The lab has two notebooks and one script. All three use the same five sample requests in the `data` folder.

> **Note:** The sample requests are fictional. Do not paste real employee, customer or financial records.

## 2. Before you start

| Item | What you need |
|---|---|
| Computer | Windows with PowerShell (built into Windows) |
| Python | Python 3.10 or higher. Check it by typing `python --version` in PowerShell |
| OpenAI API key | Ask your facilitator for a key, or create one at platform.openai.com |
| Time | About 30 to 45 minutes for the first run |
| Cost | A few cents of AI usage (model: gpt-4o-mini) |

## 3. Files in the lab folder

```
Module 6 - Lab 2/
├── module6_lab2_sequential_chain.ipynb   # Main notebook, step by step (7 parts)
├── module6_lab2_corporate_ops.ipynb      # Shorter notebook that uses ops_workflow.py
├── ops_workflow.py                       # Script and functions for the workflow
├── requirements_module6_lab2.txt         # Python packages to install
├── .env                                  # Your API key (keep private)
├── data/
│   └── ops_requests.json                 # Five sample operations requests
└── docs/
    ├── user_guide.docx                   # This guide (Word)
    ├── user_guide.md                     # This guide (Markdown)
    ├── MODULE6_LAB2_README.md            # Full reference
    └── DELIVERABLES_SUMMARY.md           # File list and learning outcomes
```

The notebooks and the script must stay in the lab folder. They write `ops_analysis_results.json` into the lab folder.

## 4. Step-by-step setup

#### Step 1: Open PowerShell in the lab folder

- In File Explorer, open the folder **Module 6 - Lab 2**.
- Click once in the address bar, type `powershell` and press Enter.
- Check that the window title ends with `Module 6 - Lab 2`.

#### Step 2: Create the lab's toolbox (virtual environment)

```
python -m venv .venv
```

Wait about one minute for the `.venv` folder to appear in the lab folder.

> **Note:** If a `.venv` folder already exists from an older computer, delete it first (right-click, Delete, empty the Recycle Bin), then run the command again.

#### Step 3: Install the lab packages

```
.\.venv\Scripts\python.exe -m pip install -r requirements_module6_lab2.txt
```

This list includes Jupyter, so you do not need a separate install step. It also installs pandas, numpy and pytest. The lab does not use them directly, and that is expected.

#### Step 4: Add your API key to the .env file

- Right-click the file named `.env` and choose Open with > Notepad.
- Replace the placeholder after `OPENAI_API_KEY=` with your key, on the same line, with no spaces and no quotation marks.
- Press Ctrl+S to save, then close Notepad.

> **Note:** This lab's .env file holds only the key. The model (gpt-4o-mini) and the temperature (0.3) are set in the code.

## 5. Option A: run the sequential notebook (start here)

#### Step 5: Open the notebook

```
.\.venv\Scripts\jupyter.exe notebook module6_lab2_sequential_chain.ipynb
```

A browser tab opens. If it does not, copy the link that starts with `http://localhost` from PowerShell into your browser.

#### Step 6: Run the cells from top to bottom

Click inside a cell and press **Shift+Enter**. Run every cell in order. Parts 5 and 6 call the AI many times, so they take a few minutes.

| Part | What you should see |
|---|---|
| 1. Setup | "OpenAI API key configured: Yes" |
| 2. Load the requests | "Loaded 5 requests", then one line for each request (OPS-101 to OPS-105) |
| 3. Prompt templates | "Prompt templates ready: summary, cause, impact, action". No AI call |
| 4. Build the chains | "Chains ready: summary, cause, impact, action" |
| 5. One request | The four steps for OPS-101, printed in order: summary, cause and blockers, business impact, action plan |
| 6. All requests | Each request is processed, then "Saved 5 results to ops_analysis_results.json" |
| 7. Read the report | A printed report for each request, with the four sections |

#### Step 7: Stop the notebook

Close the browser tab. In PowerShell, press Ctrl+C, type y and press Enter.

## 6. Option B: run the corporate notebook (shorter)

Start this notebook after you have stopped the first one (Step 7). Type this command in PowerShell and press Enter:

```
.\.venv\Scripts\jupyter.exe notebook module6_lab2_corporate_ops.ipynb
```

Run the cells from top to bottom with Shift+Enter.

| Part | What you should see |
|---|---|
| 1. Setup | "OpenAI API key configured: Yes" |
| 2. Load the requests | One line for each request (ID, type and department) |
| 3. Build the chains | "Chains ready: ['summary', 'cause', 'impact', 'action']" |
| 4. One request | A full report for OPS-101 |
| 5. All requests | "Results saved to: ops_analysis_results.json" |

> **Note:** The sequential notebook and the corporate notebook both write `ops_analysis_results.json`. The latest run replaces the older file.

## 7. Option C: run the script

The script runs without a notebook. Type this command in PowerShell and press Enter:

```
.\.venv\Scripts\python.exe ops_workflow.py
```

The script processes the first two requests (OPS-101 and OPS-102). It prints a report for each one, saves two results to `ops_analysis_results.json`, and ends with "Analysis complete."

> **Note:** Running the script or a notebook replaces `ops_analysis_results.json`. Copy the file somewhere safe first if you want to keep the old results.

## 8. Reading the results

The file `ops_analysis_results.json` is a list. Each item has these fields: `request_id`, `request_type`, `summary`, `cause`, `impact` and `action_plan`. Open it in Notepad to read it. The file is saved in UTF-8.

## 9. Settings

| Setting | Where it is set | Value in this lab |
|---|---|---|
| OPENAI_API_KEY | .env file | Your key |
| Model | The notebooks and `build_chains()` in ops_workflow.py | gpt-4o-mini |
| Temperature | The same places as the model | 0.3 (steadier answers) |

To try another model, change the `model` line in the notebook, or the `model_name` default in `build_chains()` in `ops_workflow.py`.

## 10. Troubleshooting

| What you see | What to do |
|---|---|
| 401 or 'Incorrect API key' | Check the OPENAI_API_KEY= line in .env. Copy the key again with no spaces. If it still fails, ask your facilitator for a valid key |
| 404 or 'model does not exist' | Set the model to gpt-4o-mini in the notebook or in ops_workflow.py, then restart the kernel |
| 429, 'quota' or 'billing' | Your OpenAI account has no credit or has reached its limit. Ask your facilitator |
| 'No module named ...' | Run the install command in Step 3 again, inside the lab folder |
| 'Loaded 0 requests' or a file-not-found error | Run the notebook or script from the lab folder. Check that the file data\ops_requests.json exists |
| The results file was replaced | This is expected. Each run overwrites ops_analysis_results.json. Copy the file first if you need the old results |
| The script stops with an error about the key | The script prints the error message. Fix the key in .env, then run the script again |

## 11. Exercises

- Add a fifth step that lists the checks needed to confirm a request is closed.
- Add a request type that fits your team, such as a room booking or a parking pass.
- Compare the outputs at temperature 0 and temperature 0.7.
- Change the category list in the summary prompt to match your team's categories.

## 12. Checklist

- The packages from requirements_module6_lab2.txt installed without errors.
- OPENAI_API_KEY is set in .env.
- The sequential notebook ran from top to bottom without errors.
- The script ran and created ops_analysis_results.json.
- I can explain how the | operator passes each output to the next step.
- I changed one prompt template and saw the result change.

Related documents in the docs folder: MODULE6_LAB2_README.md (full reference) and DELIVERABLES_SUMMARY.md (file list).
