# Module 6 Lab 3 User Guide

*Conversational chains for routine corporate operations issues (version 2). Follow the steps in order. No programming experience is needed.*

## 1. What this lab does

In this lab you describe a routine operations issue to an AI assistant. The assistant asks follow-up questions first (the diagnosis step). Then it writes an action plan based on everything that was said (the solution step). The conversation is kept between turns, so each answer can use what came before.

The lab includes five sample scenarios:

- CONV-001: Employee account lockout (IT service desk).
- CONV-002: Month-end invoice processing backlog (finance).
- CONV-003: Shared drive storage nearly full (IT administration).
- CONV-004: New hire laptop setup delay (HR and IT onboarding).
- CONV-005: Weekly sales report not generated (business operations).

> **Note:** The scenarios are fictional. Do not type real names of employees or customers, or real financial records.

## 2. Before you start

| Item | What you need |
|---|---|
| Computer | Windows with PowerShell (built into Windows) |
| Python | Python 3.10 or higher. Check it by typing `python --version` in PowerShell |
| OpenAI API key | Ask your facilitator for a key, or create one at platform.openai.com |
| Time | About 30 to 45 minutes |
| Cost | A few cents of AI usage (model: gpt-4o-mini) |

## 3. Files in the lab folder

```
Module 6 - Lab 3/
├── module6_lab3_conversational_chain.ipynb   # Main notebook, step by step (12 parts)
├── conversational_workflow.py                # Script with three modes
├── requirements_module6_lab3.txt             # Python packages to install
├── .env                                      # Your API key (keep private)
├── data/
│   └── sample_conversations.json             # The five sample scenarios
└── docs/
    ├── user_guide.docx                       # This guide (Word)
    ├── user_guide.md                         # This guide (Markdown)
    ├── MODULE6_LAB3_README.md                # Full reference
    └── LAB3_DELIVERABLES_SUMMARY.md          # File list and learning outcomes
```

The notebook and the script must stay in the lab folder. The script writes `conversation_transcript.json` into the lab folder.

## 4. Step-by-step setup

#### Step 1: Open PowerShell in the lab folder

- In File Explorer, open the folder **Module 6 - Lab 3**.
- Click once in the address bar, type `powershell` and press Enter.
- Check that the window title ends with `Module 6 - Lab 3`.

#### Step 2: Create the lab's toolbox (virtual environment)

```
python -m venv .venv
```

Wait about one minute for the `.venv` folder to appear in the lab folder.

> **Note:** If a `.venv` folder already exists from an older computer, delete it first (right-click, Delete, empty the Recycle Bin), then run the command again.

#### Step 3: Install the lab packages

```
.\.venv\Scripts\python.exe -m pip install -r requirements_module6_lab3.txt
```

This list includes Jupyter. It also installs pandas, numpy and pytest, which the lab does not use directly. That is expected.

#### Step 4: Add your API key to the .env file

- Right-click the file named `.env` and choose Open with > Notepad.
- Replace the placeholder after `OPENAI_API_KEY=` with your key, on the same line, with no spaces and no quotation marks.
- Press Ctrl+S to save, then close Notepad.

> **Note:** This lab's .env file holds only the key. The model (gpt-4o-mini) and the temperature (0.7) are set in the code.

## 5. Option A: run the notebook (start here)

#### Step 5: Open the notebook

```
.\.venv\Scripts\jupyter.exe notebook module6_lab3_conversational_chain.ipynb
```

A browser tab opens. If it does not, copy the link that starts with `http://localhost` from PowerShell into your browser.

#### Step 6: Run the cells from top to bottom

Click inside a cell and press **Shift+Enter**. Run every cell in order.

| Part | What you do | What you should see |
|---|---|---|
| 1. Setup | Run the cell | "Imports OK" and "OpenAI API key found: Yes" |
| 2. Conversation memory | Run the cell | "Messages in history: 2" and the message types, then the history is reset |
| 3. System prompts | Run the cell | "Prompts ready". No AI call |
| 4. Build the chains | Run the cell | "Chains ready" |
| 5. Helper function | Run the cell | "ask() ready". No AI call |
| 6. Load a sample | Run the cell | The five conversation IDs with their scenario names, then "User turns in scenario: 2" |
| 7. Multi-turn diagnosis | Run the cell | Two rounds: your message, then the assistant's question. The history grows from 2 to 4 messages |
| 8. Solution step | Run the cell | An action plan with immediate actions, short-term actions, risks, a fallback option and a confirmation step |
| 9. Review and save | Run the cell | A numbered list of the messages, then "Saved conversation_transcript.json" |
| 10. Another scenario | Change `scenario_index` (0 to 4), then run the cell | A diagnosis for that scenario and a solution plan. 0 = account lockout, 1 = invoice backlog (default), 2 = shared drive, 3 = new hire laptop, 4 = weekly sales report |
| 11 and 12. Concepts and exercises | Read | Text only. No AI call |

Part 10 does not save a transcript. Only Part 9 and the script save the transcript.

#### Step 7: Stop the notebook

Close the browser tab. In PowerShell, press Ctrl+C, type y and press Enter.

## 6. Option B: run the interactive script

Type this command in PowerShell and press Enter:

```
.\.venv\Scripts\python.exe conversational_workflow.py
```

The script asks you to choose a mode and type 1, 2 or 3 (or just press Enter for mode 1):

| Choice | Mode | What happens |
|---|---|---|
| 1, or just Enter | Sample scenario | Runs scenario CONV-001 (account lockout): two rounds of questions, then the action plan. Saves conversation_transcript.json |
| 2 | Your own issue | Type your issue, for example "Our invoice approvals are stuck at one manager". Answer the follow-up questions. Type `solution` to get the action plan, or `quit` to leave without a plan. The transcript is saved if you typed at least one message |
| 3 | List scenarios | Lists the five scenarios. No AI call |

After the script finishes, you can read the transcript in Notepad.

## 7. Reading the transcript

The file `conversation_transcript.json` holds the time the conversation was saved, the number of messages, and each message with its turn number, its role (`human` for you, `ai` for the assistant) and its text. Each run replaces the file.

## 8. Settings

| Setting | Where it is set | Value in this lab |
|---|---|---|
| OPENAI_API_KEY | .env file | Your key |
| Model | make_llm() in conversational_workflow.py, and the notebook | gpt-4o-mini |
| Temperature | The same places as the model | 0.7 |

To try another model, change the `model_name` and `temperature` values. For example: `make_llm(model_name="gpt-4o", temperature=0.5)`.

## 9. Troubleshooting

| What you see | What to do |
|---|---|
| 401 or 'Incorrect API key' | The script prints 'Error:' with the message, followed by a checklist. Fix the OPENAI_API_KEY= line in .env, then run the script again. The script does not stop with an error code, so read the message |
| 404 or 'model does not exist' | Change the model to gpt-4o-mini in the notebook or in make_llm(), then restart the kernel or run the script again |
| 429, 'quota' or 'billing' | Your OpenAI account has no credit or has reached its limit. Ask your facilitator |
| 'No module named ...' | Run the install command in Step 3 again, inside the lab folder |
| No transcript after mode 2 | The transcript is saved only if you typed at least one message before 'solution' or 'quit' |
| Any answer other than 2 or 3 starts mode 1 | This is expected. The script treats any other choice as the sample scenario |
| The notebook shows old results | Choose Kernel > Restart & Run All |

## 10. Exercises

- Write your own routine operations issue, for example a printer offline for a whole floor. Run it in mode 2.
- Compare the action plan after two of your messages with the plan after three.
- Change the diagnosis prompt in conversational_workflow.py to ask more or fewer questions.
- Add a third step that writes a short status update for managers, using the same history.
- For a long conversation, keep only the last few messages and a short summary of the earlier ones.

## 11. Checklist

- The packages from requirements_module6_lab3.txt installed without errors.
- OPENAI_API_KEY is set in .env.
- The notebook ran from top to bottom without errors.
- The script ran in mode 1 and created conversation_transcript.json.
- I used mode 2 with my own issue and asked for the solution.
- I can explain how the history is passed to each turn.

Related documents in the docs folder: MODULE6_LAB3_README.md (full reference) and LAB3_DELIVERABLES_SUMMARY.md (file list).
