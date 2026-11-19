# Module 6 Lab 1 User Guide

*LangChain Basics for Routine Corporate Operations (version 2.0). Follow the steps in order. No programming experience is needed.*

## 1. What this lab does

In this lab you use an AI model to help with everyday office and operations work:

- Summarize a night-shift handover and list the tasks for the next shift.
- Sort helpdesk and office tickets into a team and a priority.
- Turn meeting notes into a status email.
- Triage a batch of eight tickets and save the results to a file.

You work in a Jupyter notebook. A notebook is a web page made of cells. Each cell is a small block of code or text, and you run one cell at a time.

> **Note:** Use sample data only. Do not paste real employee, customer or financial records.

## 2. Before you start

| Item | What you need |
|---|---|
| Computer | Windows with PowerShell (built into Windows) |
| Python | Python 3.10 or higher. Check it by typing `python --version` in PowerShell |
| OpenAI API key | Ask your facilitator for a key, or create one at platform.openai.com |
| Internet | Needed for every AI call |
| Time | About 2 to 3 hours |
| Cost | A few cents of AI usage (model: gpt-4o-mini) |

## 3. Files in the lab folder

```
Module 6 - Lab 1/
├── module6_lab1_langchain_basics.ipynb   # The notebook you run (12 sections)
├── lab1_m6_requirements.txt              # Python packages to install
├── .env                                  # Your settings and API key (keep private)
├── .env_lab1_m6_example                  # Settings template (optional)
├── data/
│   ├── sample_tickets.json               # 8 office and IT tickets
│   ├── sample_shift_notes.txt            # Night-shift handover log
│   └── sample_meeting_notes.txt          # Weekly operations meeting notes
└── docs/
    ├── user_guide.docx                   # This guide (Word)
    ├── user_guide.md                     # This guide (Markdown)
    ├── MODULE6_LAB1_README.md            # Full reference
    ├── LAB1_M6_QUICKSTART.md             # Five-minute start
    ├── LAB1_M6_MANIFEST.txt              # File list
    └── MODULE6_LAB1_DELIVERY_SUMMARY.txt # Delivery notes
```

Keep the files where they are. The notebook reads the sample files from the `data` folder and creates an `output` folder for its results.

## 4. Step-by-step setup

#### Step 1: Open PowerShell in the lab folder

- In File Explorer, open the folder **Module 6 - Lab 1**.
- Click once in the address bar at the top, type `powershell` and press Enter.
- Check that the window title ends with `Module 6 - Lab 1`.

To paste a command into PowerShell, right-click inside the window. Do not press Ctrl+V.

#### Step 2: Create the lab's toolbox (virtual environment)

Type this command and press Enter. Wait about one minute until the prompt comes back:

```
python -m venv .venv
```

A folder named `.venv` appears inside the lab folder.

> **Note:** If a `.venv` folder already exists from an older computer, right-click it, choose Delete, empty the Recycle Bin, and then run the command again.

#### Step 3: Install the lab packages

Type these two commands, one at a time. Wait for the cursor to come back after each one. This can take several minutes.

```
.\.venv\Scripts\python.exe -m pip install -r lab1_m6_requirements.txt
.\.venv\Scripts\python.exe -m pip install jupyter
```

#### Step 4: Add your API key to the .env file

- Right-click the file named `.env` and choose Open with > Notepad.
- Find the line that starts with `OPENAI_API_KEY=`.
- Put your key after the equals sign, on the same line, with no spaces and no quotation marks.
- Leave the other lines as they are. The line `OPENAI_MODEL=gpt-4o-mini` chooses the model.
- Press Ctrl+S to save, then close Notepad.

> **Note:** If you cannot see the file name `.env`, open File Explorer, click View, and tick File name extensions and Hidden items.

## 5. Run the notebook step by step

#### Step 5: Open the notebook

In PowerShell, type this command and press Enter:

```
.\.venv\Scripts\jupyter.exe notebook module6_lab1_langchain_basics.ipynb
```

A browser tab opens with the notebook. If it does not, copy the link that starts with `http://localhost` from the PowerShell window and paste it into your browser.

#### Step 6: Run the cells from top to bottom

- Click inside a cell, then press **Shift+Enter** to run it.
- Run every cell in order. Do not skip cells.
- Wait for each cell to finish before you run the next one. Cells that call the AI take a few seconds.
- AI answers vary from run to run, so your wording will differ from the examples. The structure should match.

#### What each section does and what you should see

| Section | What you do | What you should see |
|---|---|---|
| 1. Setup | Run the setup cell | "LangChain Lab 1 setup complete" and "OpenAI API key found: True" |
| 2. Building blocks | Run the cell | A short table of the building blocks. No AI call |
| 3. Working with the LLM | Run the settings cell, then the basic question cell | "Model: gpt-4o-mini \| temperature ... \| max tokens ...", then a one-sentence answer about shift handovers |
| 4. Prompt templates | Run the three template cells | Filled-in prompt text, including a helpdesk prompt with system and human roles. No AI call |
| 5. Chains | Run the shift handover cell | A summary of the shift notes with open issues, actions for the next shift and items completed |
| 6. Multi-step chain | Run the cell | A numbered list of next-shift tasks, each with an owner (IT, Facilities, Security or Finance) |
| 7. Output parsing | Run the JSON triage cell | One line in the form: team \| priority \| reason, for a printer ticket |
| 8. Exercise | Read the instructions, then run the starter cell | A status email with a subject line. You change the instructions as described in Step 7 below |
| 9. Best practices | Run the cell | Tips grouped by topic. No AI call |
| 10. Patterns | Run the cell | Four routine-operations patterns with their inputs and outputs. No AI call |
| 11. Batch triage | Run the cell | One line for each ticket (TKT-101 to TKT-108), then "Saved 8 results to output/ticket_triage.json" |
| 12. Summary | Run the cell | A list of what you learned. No AI call |

#### Step 7: Do the Section 8 exercise

- Open the Section 8 cell. Find the line that starts with `# TODO`.
- Change the instructions in the prompt so the email also has **3 bullet points** and **one line listing owners and due dates**.
- Run the cell again and compare the two emails.
- Optional: change `LLM_TEMPERATURE` in `.env` (for example to 0.2 or 1.0), save, then restart the kernel with Kernel > Restart & Run All and compare the wording.

#### Step 8: Stop the notebook

- Close the browser tab.
- Go back to the PowerShell window, press Ctrl+C, type y and press Enter.

## 6. Check the results

After Section 11 runs, open the file `output\ticket_triage.json` in Notepad. It holds one entry per ticket with the fields `id`, `team`, `priority` and `reason`. An example run gave these teams and priorities:

| Ticket | Team | Priority |
|---|---|---|
| TKT-101 (locked account) | IT | High |
| TKT-102 (air conditioning) | Facilities | High |
| TKT-103 (address update) | HR | Medium |
| TKT-104 (expense report) | Finance | Medium |
| TKT-105 (laptop battery) | IT | High |
| TKT-106 (supply cabinet) | Facilities | Medium |
| TKT-107 (new hire laptop) | IT | High |
| TKT-108 (past-due invoice) | Finance | High |

The model may choose differently on another run. A ticket marked `UNPARSED` means the model did not return valid JSON for it.

## 7. Optional: the QuickStart examples

The file `docs\LAB1_M6_QUICKSTART.md` has short examples: a one-line reminder, a shift summary, one ticket triage and a status email. Copy an example into a new notebook cell and run it. Examples that contain `your_prompt` or `handover_chain` are illustrations only and will not run as they are.

## 8. Settings in the .env file

| Setting | What it does | Value used |
|---|---|---|
| OPENAI_API_KEY | Your private key. Required | Your key |
| OPENAI_MODEL | The model that writes the answers | gpt-4o-mini |
| LLM_TEMPERATURE | Lower values give more consistent answers. Higher values give more varied answers | 0.7 in the .env file (the code default is 0.2) |
| MAX_TOKENS | The longest reply the model may write | 1000 |

> **Note:** Other lines in the .env file (DEBUG, LOG_LEVEL, DATA_DIR, OUTPUT_DIR, RATE_LIMIT_RPM and RATE_LIMIT_TPM) are not used by this lab. Leave them unchanged.

## 9. Troubleshooting

| What you see | What to do |
|---|---|
| 'No module named langchain' (or another name) | Run the install commands in Step 3 again, inside the lab folder |
| 401 or 'Incorrect API key' | Copy the key into .env again, on the OPENAI_API_KEY= line, with no spaces. If it still fails, ask your facilitator for a valid key |
| 404 or 'model does not exist' | Set `OPENAI_MODEL=gpt-4o-mini` in .env, then choose Kernel > Restart & Run All |
| 429, 'quota' or 'billing' | Your OpenAI account has no credit or has reached its limit. Ask your facilitator |
| 'OpenAI API key found: False' in Section 1 | The key is missing from .env, or the file is not named exactly `.env` |
| A ticket shows UNPARSED in Section 11 | The model did not return valid JSON for that ticket. Run Section 11 again |
| Old results still show, or a cell fails after an edit | Choose Kernel > Restart & Run All |
| The browser does not open | Copy the link that starts with http://localhost into your browser |
| A cell runs for a long time | Wait up to a minute. If nothing happens, press Ctrl+C in PowerShell and run the notebook again |
| No output folder after Section 11 | Section 11 stopped with an error. Read the message above the cell, fix the cause, and run the cell again |

## 10. Safety and privacy

- Use sample data only.
- Keep your API key private. Do not paste it into chats, emails or screenshots.
- Do not send the `.env` file to anyone.

## 11. Checklist

- The packages installed without errors.
- OPENAI_API_KEY is set in `.env`.
- Section 1 shows "OpenAI API key found: True".
- Section 3 returned an answer.
- Section 5 returned a shift handover summary.
- Section 11 saved `output\ticket_triage.json` with eight results.
- I can explain the pattern `prompt | llm | parser`.

Related documents in the docs folder: MODULE6_LAB1_README.md (full reference) and LAB1_M6_QUICKSTART.md (five-minute start).
