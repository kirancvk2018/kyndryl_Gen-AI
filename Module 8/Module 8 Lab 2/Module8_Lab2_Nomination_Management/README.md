# Module 8 Lab 2: Nomination Management Agent with Excel Integration (LangChain)

## 1. Overview

Build a conversational agent that manages employee nominations for recognition and award programmes. The agent reads an existing Excel workbook, collects nomination details through conversation, validates them with a small Pydantic model, searches records by employee name or ID, answers questions from the retrieved data, and adds new nominations to the workbook **only after explicit user confirmation**.

This is a training application, not a production HR system. All employees, IDs and records are fictional.

## 2. Learning objectives

Participants learn how to:

1. Create custom business tools in LangChain with `@tool`.
2. See how an agent selects and invokes those tools (tool calling).
3. Read and inspect an Excel workbook with Pandas.
4. Validate structured data with a Pydantic model.
5. Collect nomination details through conversation and validate them before saving.
6. Search nominations by employee ID and by employee name, including ambiguous names.
7. Add nominations to Excel safely, with backup, duplicate detection and confirmation.
8. Answer summary questions from the retrieved data.

## 3. Prerequisites

- Windows with Python already installed and selected in VS Code. This lab was verified with **Python 3.10.11**.
- VS Code with the Python and Jupyter extensions.
- An OpenAI API key with access to `gpt-4o-mini`.
- Module 7 Lab 1/2 or Module 8 Lab 1 completed (recommended, not required).

## 4. Technologies used

| Technology | Role in this lab |
|---|---|
| LangChain (`langchain==1.3.14`) | Core framework |
| langchain-core (`1.5.3`) | `@tool`, messages, prompt templates |
| langchain-openai (`1.4.2`) | `ChatOpenAI` model |
| langchain-classic (`1.0.8`) | `create_tool_calling_agent` and `AgentExecutor` (LangChain 1.x location) |
| Pydantic (`2.12.3`) | `Nomination` model and validation |
| Pandas (`2.3.3`) and OpenPyXL (`3.1.5`) | Reading and writing `employee_nominations.xlsx` |
| python-dotenv (`1.0.1`) | Loads `OPENAI_API_KEY` from `.env` |

### Versions detected in the training interpreter

Inspected before the build. The same LangChain versions were reused from Module 7 Lab 1, Module 7 Lab 2 and Module 8 Lab 1.

| Package | Version |
|---|---|
| Python | 3.10.11 |
| langchain | 1.3.14 |
| langchain-core | 1.5.3 |
| langchain-openai | 1.4.2 |
| langchain-classic | 1.0.8 |
| langchain-community | 0.4.2 (installed, but not needed by this lab) |

Do not upgrade these packages. The lab was built to work with these exact versions.

## 5. Agent architecture

```
User Conversation -> LangChain Agent -> Custom Tools -> Excel Workbook -> Retrieved Data -> Agent Response
```

The agent is one `AgentExecutor` with four custom tools:

| Tool | Purpose | Writes? |
|---|---|---|
| `search_nomination_by_employee_id` | All records for one exact employee ID | No |
| `search_nomination_by_employee_name` | Records whose name matches (partial, case-insensitive); lists every employee if several match | No |
| `add_employee_nomination` | Validates, checks duplicates, previews, and saves as **Pending** after confirmation | Yes (only after confirmation) |
| `get_nomination_summary` | Counts: overview, status, department or award category | No |

The LLM chooses tools from the user's intent and the tool descriptions. The prompt does not hard-code a tool per request.

## 6. Project structure

```text
Module8_Lab2_Nomination_Management/
├── module8_lab2_nomination_management.ipynb   # the lab notebook (run it top to bottom)
├── employee_nominations.xlsx                  # sample workbook: 14 fictional nominations
├── requirements.txt                           # pinned LangChain stack and light dependencies
├── README.md                                  # this file
├── .env.example                               # placeholder for your OpenAI key
└── .gitignore                                 # keeps .env, backups and caches out of git
```

When you run the notebook, two files appear next to the workbook: `employee_nominations.xlsx.bak` (the original, created before the first write) and a temporary file that is removed automatically. Both are ignored by `.gitignore`.

## 7. Existing Python environment

Use the Python interpreter that is already configured in VS Code. Do **not** create a new virtual environment, install another Python, install Anaconda, or change the default interpreter. Check the interpreter from a terminal:

```bash
python --version
python -m pip --version
```

## 8. Dependency installation

From the project folder, install into the same interpreter:

```bash
python -m pip install -r requirements.txt
```

The pins match the versions already installed in the training interpreter, so this should report that the requirements are already satisfied. If it wants to change LangChain versions, stop and check that VS Code is using the right interpreter.

The notebook **must** run on the same Python interpreter where the dependencies were installed. In VS Code, check the interpreter shown in the status bar (bottom right) and the kernel shown at the top right of the notebook.

## 9. API-key configuration

1. Copy `.env.example` to a new file named `.env` in the same folder.
2. Replace the placeholder with your key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Never commit `.env`. It is listed in `.gitignore`.

The notebook reads the key with `python-dotenv` and prints only whether a key was found. It never displays the key. Sections 1 to 10 run without a key. The agent (Section 11 onward) needs one. The model is set in one place: `CHAT_MODEL` in Section 2.

## 10. How to open the notebook in VS Code

1. Open the `Module8_Lab2_Nomination_Management` folder in VS Code (File > Open Folder).
2. Open `module8_lab2_nomination_management.ipynb`.
3. Select the kernel: **Select Kernel > Python Environments**, then choose the same interpreter where you ran `python -m pip install -r requirements.txt`.

## 11. How to run the notebook

- Run the cells **in order**, from top to bottom. Use **Run All** or run each cell with Shift+Enter.
- The notebook is designed to run from start to finish. Each cell depends on the one before it.
- The agent cell (Section 11) stops with a clear message if no key is found. Add the key to `.env`, then run that cell again.
- Interactive chat is off by default (`INTERACTIVE_CHAT = False`). To chat yourself, set it to `True` in the Section 12 cell, run that cell, type your messages, and type `exit` to finish.
- Each write adds a record to the workbook. The notebook is safe to re-run, but see Troubleshooting for what a second run shows.

## 12. Excel workbook structure

The workbook `employee_nominations.xlsx` has one worksheet, `Nominations`, with these columns:

| Column | Meaning |
|---|---|
| Nomination_ID | Unique record ID, for example NOM-0001 (generated by the application) |
| Employee_ID | Employee ID, for example EMP1001 |
| Employee_Name | Employee's full name |
| Department | Employee's department |
| Designation | Employee's job title |
| Award_Category | Award being nominated for |
| Nomination_Reason | Why the employee is nominated |
| Nominated_By | Nominating manager |
| Nomination_Date | Date of the nomination (a real Excel date) |
| Status | Pending, Approved or Rejected (new records are always Pending) |

The workbook is the source of truth. The notebook reads it every time it needs data, and it never keeps a separate database.

## 13. Pydantic model explanation

The `Nomination` model in Section 4 checks each field before anything is written:

- **employee_id**: not blank; format `EMP` + 4 digits; stored in upper case.
- **employee_name**: not blank; 2 to 100 characters.
- **department, designation, award_category, nominated_by**: not blank.
- **nomination_reason**: not blank; at least 10 characters.
- **nomination_date**: a real calendar date. Defaults to today.

Invalid input raises a `ValidationError`. The tool returns the failing fields to the agent, which asks the user to correct them. No invalid record reaches Excel.

## 14. Custom tool explanations

- **`@tool`** turns a Python function into a LangChain tool. The function name is the tool name, the docstring is the description the LLM reads, and `Annotated[..., Field(description=...)]` explains each argument.
- **Outputs are text.** Each tool returns a readable string, which the agent uses to write its answer.
- **Search tools** call the same Pandas functions used in Section 5, so business logic is not repeated.
- **The add tool** has the confirmation and duplicate checks described below.

## 15. Conversational nomination workflow

1. The user says they want to nominate someone.
2. The agent asks only for the fields still missing. It keeps the conversation context, so details already given are not asked for again.
3. When all fields are present, the agent calls the add tool with `user_confirmed=False`. The tool validates the details and returns a **preview**. Nothing is written.
4. The agent shows the preview and asks the user to confirm.
5. The user must reply with a clear "yes" to save. A code check also requires that the latest message is a confirmation.
6. If a similar nomination already exists for the same employee, award category and reason, the tool shows that record and asks whether to add the new one anyway.
7. Only when the tool returns `SAVED` does the agent report success.

Employees can have several nominations, so an existing employee ID is not rejected. Two different people with the same name are never assumed to be one person: the agent lists both and asks which one is meant.

## 16. Employee search functionality

- **By employee ID**: exact match, case-insensitive (`emp1001` finds `EMP1001`).
- **By employee name**: partial, case-insensitive match (`rahul` finds both Rahul Sharmas). When more than one employee matches, the tool lists every employee with their ID.
- **No match**: a clear message is returned. The agent says the information is not in the workbook and does not invent an answer.

## 17. Excel update functionality

The write is handled by one controlled function, `save_workbook_safely()`:

1. Create a backup (`employee_nominations.xlsx.bak`) once, before the first write.
2. Append the new row with OpenPyXL. Other sheets and formatting are kept.
3. Save to a temporary file and reload it.
4. Check that exactly one row was added, the columns are unchanged, and every existing Nomination_ID is still in place.
5. Replace the original file only if all checks pass.

If the workbook is open in Excel, the write stops and the tool reports `SAVE FAILED`. The agent never claims a save that did not happen.

## 18. Hands-on exercises

The notebook's Section 15 has five exercises and a five-question quiz:

1. Search an employee's nominations by employee ID.
2. Search nominations by employee name and handle a name shared by two employees.
3. Submit a new nomination through conversation and decline the confirmation.
4. Add an optional field (for example `employee_location`) to the `Nomination` model.
5. Ask for nomination statistics by department and award category.

## 19. Troubleshooting

| Problem | What to do |
|---|---|
| `Workbook not found` | Open the notebook from the project folder. The workbook must be in the same folder. |
| `ModuleNotFoundError` for LangChain, pandas, openpyxl or pydantic | The notebook is using a different interpreter. Select the interpreter where you ran `python -m pip install -r requirements.txt`, then restart the kernel. |
| `OPENAI_API_KEY is missing` | Create `.env` from `.env.example` and add your key. Restart the kernel, then run the cell again. |
| `SAVE FAILED ... open in another application` | Close `employee_nominations.xlsx` in Excel, then ask the agent to confirm again. Nothing was saved. |
| The Rahul Sharma nomination says "potential duplicate" | You have already run Use Case 1. The record exists, so the agent asks before adding another. To start again, run `restore_sample_workbook()` in a new cell. This restores the 14 original records from the backup and removes records added since. |
| Mermaid diagram shows as text | Your editor does not render Mermaid. The flow is still the same. |
| The agent claims a save but the row is missing | Run the verification cell in Section 14 and report the output. A claimed save is only real if the tool returned `SAVED`. |
| Agent is slow or hits the step limit | Increase `MAX_ITERATIONS` in Section 2 slightly, or simplify the request. |
| Results differ slightly between runs | LLM wording can vary, even at `temperature=0`. Check the tool names and the data, not the exact wording. |
