# Module 8 Lab 2: User Guide

Nomination Management Agent with Excel Integration (LangChain)

| Item | Details |
| --- | --- |
| Audience | Lab participants. No advanced Python knowledge is needed. |
| Time needed | About 1 to 2 hours, including the exercises. |
| Project folder | Module8_Lab2_Nomination_Management |
| Main file | module8_lab2_nomination_management.ipynb (the lab notebook) |
| Data | All employees, IDs and nominations are fictional. This is a training app, not an HR system. |

## What you will do

You will build a chat assistant that manages employee nominations. The assistant reads and writes a real Excel workbook. You will use it to:

- find nominations by employee ID or by employee name,
- answer counts such as how many nominations are pending,
- collect the details for a new nomination through conversation, check them, and save them after you confirm.

The assistant never saves a nomination without your explicit confirmation. A new nomination always starts with the status Pending. The assistant cannot approve anything.

## How the pieces work together

```text
You type a message
   -> the agent (a language model) reads it and chooses a tool
   -> the tool runs a Python function on the Excel workbook
   -> the workbook data comes back to the agent
   -> the agent writes the answer
```

A tool is a Python function the agent is allowed to call. The four tools in this lab are: search by employee ID, search by employee name, add a nomination, and get a nomination summary.

## Contents

- [Before you start](#before-you-start)
- [Step 1: Check the project files](#step-1-check-the-project-files)
- [Step 2: Check your Python](#step-2-check-your-python)
- [Step 3: Install the packages](#step-3-install-the-packages)
- [Step 4: Create your API key file](#step-4-create-your-api-key-file)
- [Step 5: Open the notebook and choose the interpreter](#step-5-open-the-notebook-and-choose-the-interpreter)
- [Step 6: Run Sections 1 to 10 (no API key needed)](#step-6-run-sections-1-to-10-no-api-key-needed)
- [Step 7: Look at the Excel workbook](#step-7-look-at-the-excel-workbook)
- [Step 8: Try the validation rules](#step-8-try-the-validation-rules)
- [Step 9: Try the search tools](#step-9-try-the-search-tools)
- [Step 10: Try the summary tool](#step-10-try-the-summary-tool)
- [Step 11: Build the agent (needs an API key)](#step-11-build-the-agent-needs-an-api-key)
- [Step 12: Run the four use cases](#step-12-run-the-four-use-cases)
- [Step 13: Chat with the agent yourself](#step-13-chat-with-the-agent-yourself)
- [Step 14: Check that the workbook was updated correctly](#step-14-check-that-the-workbook-was-updated-correctly)
- [Step 15: Reset the sample data](#step-15-reset-the-sample-data)
- [Step 16: Hands-on exercises and quiz](#step-16-hands-on-exercises-and-quiz)
- [Appendix A: Messages to try with the agent](#appendix-a-messages-to-try-with-the-agent)
- [Appendix B: Excel column reference](#appendix-b-excel-column-reference)
- [Appendix C: Troubleshooting](#appendix-c-troubleshooting)
- [Appendix D: Safety rules built into the lab](#appendix-d-safety-rules-built-into-the-lab)

## Before you start

Check that you have each item below. Steps 1 to 10 work without an API key. You need a key from Step 11 onward.

| You need | How to check it |
| --- | --- |
| A Windows computer with Python installed | Open a terminal in VS Code and type python --version (see Step 2). |
| VS Code with the Python and Jupyter extensions | Open the Extensions view (Ctrl+Shift+X) and confirm both are installed. |
| The six project files | See Step 1. |
| An OpenAI API key with access to gpt-4o-mini | Your trainer will tell you where to get one. Needed from Step 11. |
| Microsoft Excel (optional, for viewing the workbook) | Close the workbook in Excel before any step that saves a nomination. |

## Step 1: Check the project files

Open the Module8_Lab2_Nomination_Management folder. It should contain exactly these six files:

| File | What it is for |
| --- | --- |
| module8_lab2_nomination_management.ipynb | The lab notebook. You will run every step here. |
| employee_nominations.xlsx | The sample workbook with 14 fictional nominations. |
| requirements.txt | The list of Python packages the lab needs. |
| README.md | Setup and reference notes. |
| .env.example | A template for your API key file. Do not put a real key in it. |
| .gitignore | Tells git to ignore your .env file, backups and caches. |

Later in the lab, extra files appear: a backup named employee_nominations.xlsx.bak is created before the first save. Leave it in place.

## Step 2: Check your Python

1. In VS Code, choose Terminal > New Terminal. Make sure the terminal is in the project folder.
2. Type the first command and press Enter:

```bash
python --version
```

3. Type the second command and press Enter:

```bash
python -m pip --version
```

What you should see: a line such as Python 3.10.11 and a line that starts with pip. This lab was built and tested with Python 3.10.11.

> **Warning:** Do not install another Python. Do not create a new virtual environment or a Conda environment. Use the Python that is already set up in VS Code.

## Step 3: Install the packages

1. In the same terminal, type this command and press Enter:

```bash
python -m pip install -r requirements.txt
```

What you should see: lines that say Requirement already satisfied for each package. There should be no line that says Successfully installed.

If pip tries to install or upgrade the LangChain packages, stop. Check the interpreter you are using (Step 5) and ask your trainer. The LangChain versions in this lab must not change.

## Step 4: Create your API key file

The notebook reads your OpenAI key from a file called .env. You create that file from the template.

1. In the project folder, copy the file .env.example. Name the copy .env. The name starts with a dot and has no .txt at the end.
2. Open .env in VS Code.
3. Replace your_openai_api_key_here with your own key. Keep OPENAI_API_KEY= at the start of the line.
4. Save the file.

```text
OPENAI_API_KEY=<your key goes here>
```

> **Warning:** Never share your .env file. Never paste your key into the notebook or into a chat. Never commit .env to git. Keep the placeholder in .env.example, not your real key.

> **Tip:** If Windows will not let you create a file that starts with a dot, create it in VS Code: File > New File, then save it as .env in the project folder.

You can check the key status at any time. Section 2 of the notebook shows True or False. It never shows the key itself.

## Step 5: Open the notebook and choose the interpreter

1. In VS Code, choose File > Open Folder and select Module8_Lab2_Nomination_Management.
2. In the Explorer panel, click module8_lab2_nomination_management.ipynb.
3. At the top right of the notebook, click Select Kernel. Choose Python Environments, then choose the same Python you used in Step 3.
4. Check the bottom-right status bar. It should show the same Python version as in Step 2.

What you should see: the notebook opens with the title Module 8 – Lab 2 and a Learning objectives section.

> **Warning:** The notebook must use the same Python where the packages were installed. If you see ModuleNotFoundError later, this is the first thing to check.

## Step 6: Run Sections 1 to 10 (no API key needed)

To run one cell, click inside it and press Shift+Enter. Run the cells in order, from the top. Do not skip cells. Each code cell shows its output directly below it.

| Section | What the cells do | What you should see |
| --- | --- | --- |
| 2. Environment setup | Imports libraries, shows the Python and LangChain versions, checks for your key. | Version lines. OPENAI_API_KEY available: False is fine at this stage. |
| 3. Excel workbook | Finds the workbook, loads it, shows the first five records, the count and the columns. | 14 existing nominations and ten column names. |
| 4. Pydantic model | Runs one valid nomination and five invalid ones through the Nomination model. | One PASSED line and five REJECTED lines, each naming the field. |
| 5. Python functions | Tests the search and summary functions. Then adds one demonstration record. | Search results. Then: Saved NOM-0015 with status Pending. |
| 6 and 7. Search tools | Defines the search-by-ID and search-by-name tools and tests them. | Records for EMP1001, and the 'two different employees' message for Rahul Sharma. |
| 8. Add tool | Defines the add-nomination tool and tests its validation, preview and duplicate checks. | Errors, previews and duplicate messages. Nothing new is saved in these tests. |
| 9 and 10. Summary and registration | Defines the summary tool and lists the four tools for the agent. | Counts, then the tool names and their arguments. |

> **Important:** Section 5 adds one demonstration record (Ananya Rao, NOM-0015) to the workbook every time it runs. Step 15 shows how to reset the workbook.

If a cell shows a red error, stop and read the message. Check the troubleshooting table in Appendix C.

## Step 7: Look at the Excel workbook

1. In Excel, open employee_nominations.xlsx from the project folder. Only view it for now.
2. Find the sheet named Nominations. It has ten columns (see Appendix B).
3. Scroll to the bottom. The Section 5 demonstration added row 16: NOM-0015, Ananya Rao, Pending.
4. Close the workbook in Excel when you are done looking at it.

> **Warning:** While the workbook is open in Excel, the notebook cannot save. You will see SAVE FAILED. Close the workbook before you run any step that adds a nomination.

## Step 8: Try the validation rules

Before a nomination reaches Excel, the Nomination model checks every field. These are the rules:

| Field | Rule |
| --- | --- |
| employee_id | Not blank. Format EMP followed by four digits, for example EMP1001. Stored in capital letters. |
| employee_name | Not blank. Two to 100 characters. |
| department, designation, award_category | Not blank. |
| nomination_reason | Not blank. At least 10 characters. |
| nominated_by | Not blank. |
| nomination_date | A real calendar date, for example 2026-04-30. Defaults to today if left out. |

1. Find the Section 4 cell with the test_cases dictionary.
2. Read the REJECTED lines. Each one names the field and the problem.
3. Change one value in valid_example, for example set nomination_reason to Good, and run the cell again. The record is now rejected. Change the value back before you continue.

Why this matters: if a record is invalid, the agent asks the user to correct it. Nothing invalid is ever written to Excel.

## Step 9: Try the search tools

Run the Section 6 and 7 cells. Then try these examples in a new cell, using the tool's invoke method:

```python
search_nomination_by_employee_id.invoke({"employee_id": "emp1001"})
search_nomination_by_employee_name.invoke({"employee_name": "rahul"})
search_nomination_by_employee_name.invoke({"employee_name": "Zara Quinn"})
```

| What you type | What you should get | Why |
| --- | --- | --- |
| employee ID emp1001 | Two records for EMP1001 | ID search ignores capital letters and spaces. |
| name rahul | Records for two different employees: EMP1001 and EMP1008 | Two people are called Rahul Sharma. The agent must not guess which one is meant. |
| name Zara Quinn | No nomination records found | No record matches, so the agent says so. |

> **Tip:** When the agent finds two people with the same name, it lists both and asks for the employee ID. This is by design.

## Step 10: Try the summary tool

1. Run the Section 9 cell. It shows the overview and the department counts.
2. Note the total and the number of Pending nominations.
3. Find the department with the most nominations. The list is sorted from highest to lowest, so the first line is the answer. At the start of the lab, IT Operations has 3.

The summary tool counts rows in Excel. It does not estimate or guess. You can ask the same questions in the agent (Step 12, Use Case 4).

## Step 11: Build the agent (needs an API key)

This is the first step that calls the OpenAI service. You need the key from Step 4.

1. Make sure .env exists in the project folder and holds your key (Step 4).
2. Re-run the Section 2 cell. It loads the .env file again. If the message still says False, choose Kernel > Restart Kernel, then run the notebook again from the top to Section 2.
3. Run the Section 11 cell, which builds the agent.

What you should see: Agent ready. Model: gpt-4o-mini | max steps: 8.

If you have no key yet, this cell stops with the message OPENAI_API_KEY is missing. That is expected. Sections 1 to 10 still work, so you can keep learning while you wait for a key.

> **Note:** Section 11 explains the agent, its prompt and its rules. Read it before the use cases. The agent is given four tools and chooses between them based on what you ask.

## Step 12: Run the four use cases

Section 13 runs scripted conversations through the same agent. Each message is sent to the agent in order, so every run is the same. After each reply, read the line TOOLS USED. It shows which tools the agent called.

| Use case | What to look for |
| --- | --- |
| 1. New nomination (Rahul Sharma, Star Performer Award) | The agent asks for the missing details, shows a summary, and saves only after you reply Yes, confirm. The first run saves NOM-0016. |
| 1b. Declined nomination (Priya Nair) | The agent shows a summary, the user says no, and the record count stays the same. |
| 2. Search by employee ID (EMP1001) | The agent calls the ID search tool and summarises the records. |
| 3. Search by name (Rahul Sharma) | The agent lists both Rahul Sharmas and asks which one is meant. The follow-up message is answered from the conversation. |
| 4. Summary (pending count and top department) | The agent calls the summary tool and answers from the counts. |

Expected output after the run: the record count before and after Use Case 1 goes up by one. Before and after Use Case 1b are the same.

> **Important:** The agent output is long because verbose mode prints every step. Scroll to the TOOLS USED and AGENT RESPONSE lines for each turn.

> **Warning:** Run the notebook once on a fresh workbook. On a second run, Use Case 1 finds the Rahul Sharma nomination that was already saved. The agent then reports a POTENTIAL DUPLICATE and does not save. Reset the workbook first (Step 15) if you want to repeat the demonstration.

## Step 13: Chat with the agent yourself

Section 12 contains a chat loop. You type messages, read the replies and type exit to finish.

1. Find the Section 12 cell that contains INTERACTIVE_CHAT = False.
2. Change it to INTERACTIVE_CHAT = True and run the cell.
3. A box labelled You: appears at the top of VS Code. Type a message and press Enter.
4. Type exit and press Enter when you are finished.
5. Change INTERACTIVE_CHAT back to False before you use Run All, so the notebook does not wait for input.

Try a full nomination. Here is an example:

```text
You: I want to nominate Priya Nair for the Innovation Award.
You: Priya Nair is EMP1002. Department Finance, designation Financial Analyst.
You: Reason: she built a forecasting template that saves the team time every month.
You: Nominated by Suresh Menon, Finance Director.
You: Yes, confirm.
```

> **Important:** The agent saves only when your message starts with a clear yes or confirm and has no no or change in it. Reply Yes, confirm. If you reply Please save it, the agent will ask you again. This is deliberate: a wrong save is worse than an extra question.

## Step 14: Check that the workbook was updated correctly

1. Close the workbook in Excel if it is open.
2. Run the Section 14 cell. It reloads the workbook from disk, not from memory.
3. Read the last five records. The new record should be at the bottom with status Pending.
4. Read the five integrity checks. Each should say PASS.

| Check | Meaning |
| --- | --- |
| New Nomination_ID exists exactly once | The saved record can be found and is not duplicated. |
| Initial status is Pending | The agent cannot approve a nomination. |
| All required fields are filled | No field was left empty when the record was saved. |
| Columns are unchanged | The worksheet layout has not been altered. |
| Original records are preserved, in order | No existing record was removed or changed. |

If the cell says No SAVED result in this session yet, no save has happened since the notebook was started. Run Use Case 1 (Step 12) or save a nomination in chat (Step 13) first, then run this cell again.

## Step 15: Reset the sample data

Use this step when you want to start again from the 14 original records, for example after a second run.

1. Close employee_nominations.xlsx in Excel.
2. Scroll to the bottom of the notebook. Click + Code to add a new cell.
3. Type restore_sample_workbook() and run the cell.

What you should see: Workbook restored to the original sample records. The workbook has 14 data rows again.

> **Warning:** The reset removes every record added after the backup, including records you saved in chat. Do not use it if you want to keep your changes. Do not delete employee_nominations.xlsx.bak, because the reset uses it.

## Step 16: Hands-on exercises and quiz

Section 15 of the notebook has five exercises and a five-question quiz. Try each exercise on your own before you check the answers with your trainer.

1. **Search by employee ID.** Find the records for EMP1011. Note their status.
2. **Search by name.** Ask the agent for Michael, then for Rahul. Explain why one needed no clarification and the other did.
3. **Conversational nomination.** Use chat to nominate EMP1013 Thomas Mathew for the Team Collaboration Award. Answer no at the confirmation step, then check that the workbook did not change.
4. **Add an optional field.** Add employee_location with a default of None to the Nomination model. Explain why the workbook would also need a new column before the value could be saved.
5. **Statistics by department and award category.** Ask the agent and compare its answer with the summary functions.

Quiz: five multiple-choice questions cover custom tools, Pydantic validation, employee lookup, tool calling and conversational data collection. The answers are in the Instructor Section at the end of the notebook.

## Appendix A: Messages to try with the agent

Use these in chat (Step 13) or as the user messages in a scripted conversation. Results depend on the workbook's current contents.

| Message | What to expect |
| --- | --- |
| I want to nominate Rahul Sharma for the Star Performer Award. | The agent asks which Rahul Sharma is meant, or asks for the employee ID. |
| Find all nominations for employee EMP1001. | The records for EMP1001, with status and date for each. |
| Has Rahul Sharma been nominated before? | Both Rahul Sharmas, and a request to say which one. |
| How many nominations are pending? | The current count of Pending nominations. |
| Which department has the most nominations? | IT Operations, with its count (3 at the start). |
| Nominate Priya Nair for the Innovation Award. | A request for the missing details. No save. |
| Yes, confirm. | Saves only if a preview has just been shown. Otherwise the agent asks for details first. |
| No, cancel. | The agent confirms that nothing was saved. |

## Appendix B: Excel column reference

| Column | What it holds |
| --- | --- |
| Nomination_ID | A unique record ID, for example NOM-0001. The application creates it. |
| Employee_ID | An employee ID, for example EMP1001. |
| Employee_Name | The employee's full name. |
| Department | The employee's department. |
| Designation | The employee's job title. |
| Award_Category | The award being nominated for. |
| Nomination_Reason | Why the employee is nominated. |
| Nominated_By | The nominating manager. |
| Nomination_Date | The date of the nomination, stored as a real Excel date. |
| Status | Pending, Approved or Rejected. New records are always Pending. |

## Appendix C: Troubleshooting

| Problem | Likely cause | What to do |
| --- | --- | --- |
| Workbook not found | The notebook was opened from another folder. | Open the project folder in VS Code, then open the notebook again. |
| ModuleNotFoundError (for example langchain or pandas) | The notebook is using a different Python. | Choose the interpreter from Step 3 (Step 5), then restart the kernel. |
| OPENAI_API_KEY is missing | No .env file, or the key was not saved. | Check Step 4. Re-run Section 2, or restart the kernel and run from the top. |
| 401 error, expired or invalid key | The key is wrong, or it has expired. | Create a new key in your OpenAI account, update .env, then re-run from Section 2. |
| SAVE FAILED ... open in another application | The workbook is open in Excel. | Close the workbook in Excel. Confirm the nomination again. Nothing was saved. |
| POTENTIAL DUPLICATE | A similar nomination already exists for the same employee, award and reason. | This is expected on a second run. Reset the workbook (Step 15), or tell the agent you want to add it anyway. |
| The agent says saved, but no new row appears | Unclear. Check the tool output. | A save is real only if the tool returns SAVED. Run Section 14 and report the output to your trainer. |
| The agent does not save after you reply | Your reply did not start with a clear yes or confirm. | Reply Yes, confirm. |
| Run All stops at Section 11 | No API key yet. | Expected. Add the key (Step 4), then run from Section 11. |
| The Mermaid diagram shows as text | Your editor does not draw Mermaid diagrams. | Ignore it. The flow is the same. |
| Output is very long | Verbose mode prints every agent step. | Expected. Scroll to TOOLS USED and AGENT RESPONSE. |
| Two different people named Rahul Sharma | The workbook has two employees with this name. | Expected. Reply with the employee ID you mean. |

## Appendix D: Safety rules built into the lab

- **No save without confirmation.** The agent previews every nomination first. A save also needs a code check on your latest message.
- **New nominations are always Pending.** The lab never approves a nomination automatically.
- **Invalid details are rejected.** The Pydantic model checks every field before anything is written.
- **Existing records are not changed.** Saves only add a new row at the end of the Nominations sheet.
- **A backup is made first.** employee_nominations.xlsx.bak is created before the first save.
- **Save failures are reported honestly.** The agent says SAVED only when the file was written and checked.
- **Your key stays private.** The notebook never prints the key, and .env is ignored by git.
