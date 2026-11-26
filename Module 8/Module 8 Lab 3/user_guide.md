# Build a SQL Database Agent with LangChain

Module 8 Lab 3  |  Step-by-step user guide

> **Note:** **Who this guide is for:** learners with basic Python knowledge who run the lab on the training workstation, in VS Code or Jupyter.
>
> **What it covers:** setting up the project, connecting to your cloud PostgreSQL database on Supabase, running the notebook section by section, using the AI agent, and fixing common problems.
>
> **Where the files are:** everything is in the folder `Module8_Lab3_SQL_Database_Agent`.

#### Contents

- Before you start
- Part 1 - Set up the project (Steps 1 to 6)
- Part 2 - Run the notebook (Steps 7 to 25)
- Troubleshooting
- Resetting the sample data
- Security rules
- Appendix A - Expected results at a glance
- Appendix B - Knowledge check answers

## What you will build

In this lab you connect an **AI agent** to a **cloud PostgreSQL database** hosted on Supabase. You type a request in plain English, for example *Show me all critical incidents*. The agent chooses one of five authorised Python tools. Each tool checks its input with **Pydantic**, then runs a **parameterised SQL** statement against your database. The agent then explains the result in business language.

> **Key idea:** The language model **never connects to the database and never writes SQL**. It can only ask for one of the five tools. The tools are the only way data is read or changed.

The request flows through these stages:

```text
User natural language request
        |
        v
  LangChain agent  ->  tool selection
        |
        v
  Pydantic validation of the tool input
        |
        v
  Python tool  ->  parameterised SQL
        |
        v
  Authenticated PostgreSQL (Supabase)
        |
        v
  Result  ->  agent response
```

The lab uses one table, `incidents`, with 15 fictional IT incidents. The agent has five tools:

| Tool | What it does | Changes data? |
|---|---|---|
| `get_all_incidents` | Lists up to 50 incidents, oldest first. | No |
| `search_incidents` | Finds incidents by one severity or one status. | No |
| `get_incident_summary` | Counts by severity and status, and lists unresolved Critical incidents. | No |
| `create_incident` | Adds a new incident with status Open. | Yes, only after a preview and your yes |
| `update_incident_status` | Changes the status of one incident. | Yes, only after a preview and your yes |

## Before you start

Check each item before you begin.

| Requirement | How to check it |
|---|---|
| Python 3.10 is installed (3.10.11 on the training workstation). | Step 2 shows the version. |
| VS Code is installed, with the Python and Jupyter extensions. | Open VS Code and look at the Extensions view. |
| Module 8 Lab 1 is complete (or Module 7 Labs 1 and 2). | This lab reuses the same LangChain versions. |
| A free Supabase account. | Sign up at supabase.com (Step 4). |
| An OpenAI API key with available credit. | Needed from Step 15 only. Sections 1 to 7 run without it. |
| Internet access. | Needed for Supabase and OpenAI. |

> **Warning:** Do **not** create a virtual environment, run `python -m venv`, or install another Python or Anaconda. Use the Python already installed on the workstation. The notebook must use that same interpreter, because that is where the packages are installed.

## Part 1 - Set up the project

### Step 1 - Open the project folder

1. In File Explorer, open the folder **Module 8 Lab 3**, then open **Module8_Lab3_SQL_Database_Agent**.
2. Check that it contains these five files:

| File | What it is for |
|---|---|
| `module8_lab3_sql_database_agent.ipynb` | The notebook you will run. It is the main lab. |
| `requirements.txt` | The packages this lab needs, with pinned versions. |
| `README.md` | Reference documentation for the project. |
| `.env.example` | A template for your private settings. You copy it in Step 6. |
| `.gitignore` | Tells Git to ignore your `.env` file, so it is never committed. |

You should not have a file named `.env` yet. You create it in Step 6.

### Step 2 - Check the Python interpreter

1. In File Explorer, click the address bar at the top of the project folder, type `powershell` and press Enter. A PowerShell window opens in the project folder.
2. Type the following and press Enter:

```text
python --version
```

Expected: `Python 3.10.x` (3.10.11 on the training workstation).

3. Type the following and press Enter:

```text
python -m pip --version
```

Expected: pip is reported with `(python 3.10)` at the end of the line.

> **Tip:** If Windows says `python` is not recognised, ask your trainer. Do not install a new Python.

### Step 3 - Install the packages

1. In the same PowerShell window, type the following and press Enter:

```text
python -m pip install -r requirements.txt
```

2. Wait for the installation to finish. Packages that are already installed show `Requirement already satisfied`. That is expected.
3. Check the output. The packages this lab uses are:

| Package | Version | Purpose |
|---|---|---|
| langchain | 1.3.14 | LangChain framework |
| langchain-core | 1.5.3 | Tools, prompts and messages |
| langchain-openai | 1.4.2 | ChatOpenAI, the chat model |
| langchain-classic | 1.0.8 | The agent: create_tool_calling_agent and AgentExecutor |
| pydantic | 2.12.3 | Input validation for the tools |
| psycopg[binary] | 3.3.9 | PostgreSQL driver. The only package new since Module 8 Lab 1 |
| python-dotenv | 1.0 or later | Reads your .env file |
| ipykernel | 6.0 or later | Runs the notebook in VS Code |

> **Warning:** If pip tries to upgrade a LangChain package, stop and tell your trainer. The lab depends on the pinned versions.

### Step 4 - Create your Supabase project

1. Open **supabase.com** in your browser. Create a free account, or sign in.
2. Click **New project**. Enter a name such as `it-ops-lab` and choose a region near you.
3. Set a **strong database password**. Save it in your password manager now. You can reset it later under **Project Settings > Database**.
4. Wait until the project finishes setting up. The dashboard shows when it is ready.

> **Tip:** Supabase screens change from time to time. If a label is different, look for the same function on the screen.

### Step 5 - Find your PostgreSQL connection details

1. On your project dashboard, click **Connect**, near the top of the page.
2. Find the **PostgreSQL** connection details. Note down the **host**, **port**, **database name**, **user name** and **password**.
3. If the direct connection does not work on your network, use the **Session pooler** details from the same dialog instead.
4. Copy the user name **exactly** as shown. With the pooler, the user name can include the project reference, for example `postgres.<project-ref>`.

The lab uses two different kinds of Supabase credentials. Do not confuse them:

| Credential | Used in this lab? |
|---|---|
| Supabase project URL and API keys (used for Supabase's web and app APIs) | **No** |
| PostgreSQL database credentials: host, port, database name, user name and password | **Yes** |

The notebook connects with `sslmode=require`, which encrypts the connection. Do not turn encryption off.

### Step 6 - Create your .env file

1. In the PowerShell window in the project folder, type the following and press Enter. This makes a private copy of the template:

```text
Copy-Item .env.example .env
```

2. Open the new file `.env` in VS Code or Notepad.
3. Replace each placeholder with **your own** value. Do not add spaces around the `=` sign.

| Variable | What to enter |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI secret key. You need it from Step 15. |
| `OPENAI_MODEL` | Optional. Leave the placeholder as it is to use `gpt-4o-mini`. |
| `SUPABASE_DB_HOST` | The host shown in the Connect dialog (Step 5). |
| `SUPABASE_DB_PORT` | The port shown in the Connect dialog. Usually `5432`. |
| `SUPABASE_DB_NAME` | The database name. Usually `postgres`. |
| `SUPABASE_DB_USER` | The user name from the Connect dialog. For the pooler it can look like `postgres.<project-ref>`. |
| `SUPABASE_DB_PASSWORD` | The database password you set in Step 4. |

4. If a value contains `#`, spaces or quotes, wrap the whole value in single quotes, for example `SUPABASE_DB_PASSWORD='my#Pass word'`.
5. Save the file.

> **Warning:** The `.env` file holds your secrets. **Never** share it, take a screenshot of it, commit it to Git, or paste it into a chat or a ticket. Your trainer does not need your passwords or keys.
>
> `.env.example` is a template that is shared with everyone. **Never** type a real key or password into it. Only `.env` holds real values.

## Part 2 - Run the notebook

### Step 7 - Open the notebook

**Option A - VS Code (recommended)**

1. In VS Code, choose **File > Open Folder** and select `Module8_Lab3_SQL_Database_Agent`.
2. Open `module8_lab3_sql_database_agent.ipynb`.
3. In the top-right corner, click **Select Kernel** and choose the Python 3.10 interpreter from Step 2.

**Option B - Jupyter in a browser**

1. In the PowerShell window in the project folder, type `python -m notebook` and press Enter.
2. Open `module8_lab3_sql_database_agent.ipynb` from the browser page that appears.

> **Tip:** If you see `No module named notebook`, use Option A.

### Step 8 - Learn how to run cells

- **Run a cell:** click it, then press **Shift + Enter** (or click the play button).
- **Run cells in order, from top to bottom.** Later cells use variables and functions defined by earlier cells.
- **Read the Markdown cells first.** Each section explains what the next code cell does and what output to expect.
- **Read the output under each cell.** The notebook is saved without outputs, so every result comes from your own database.
- **If a cell shows an error,** fix it before moving on. Read the message and check the Troubleshooting part.
- **Restart the kernel** after you change `.env`: choose **Kernel > Restart**. Then run the cells again from the top.

> **Warning:** Scenario cells call the OpenAI API, which uses credit. Scenarios 3 and 4 also change your database. Run each of those cells once.

### Step 9 - Connect to the database (Section 3)

1. Run the first code cell of Section 3, which imports the libraries and reads `.env`.

Expected output includes:

- `Found a .env file in this folder: True`
- Five database settings and `OPENAI_API_KEY`, each followed by `set: True` or `set: False`. The values are never printed.
- The chat model name and the versions of the installed packages.

2. Run the next code cell, which defines `run_sql` and `test_connection`, then runs the test.

Expected output:

```text
CONNECTION OK: PostgreSQL 16.2
```

The version number depends on your Supabase project. If you see `CONNECTION FAILED`, read the message, then check Step 5, Step 6 and the Troubleshooting part. The message never shows your password.

### Step 10 - Create the table and sample data (Section 4)

The table has nine columns. You do not need to type any SQL for this step.

| Column | Type | Meaning |
|---|---|---|
| `incident_id` | SERIAL PRIMARY KEY | Unique incident number, created by the database |
| `title` | VARCHAR(200) | Incident title (required) |
| `description` | TEXT | What happened (required) |
| `category` | VARCHAR(50) | Network, Server, Database or Application |
| `severity` | VARCHAR(20) | Critical, High, Medium or Low |
| `status` | VARCHAR(30) | Open, In Progress or Resolved |
| `assigned_team` | VARCHAR(100) | Responsible team (required) |
| `affected_system` | VARCHAR(100) | Impacted application or infrastructure (required) |
| `created_at` | TIMESTAMP | When the incident was created |

1. Run the **CREATE TABLE** cell. Expected output:

```text
Table 'incidents' is ready. It is created only when it does not already exist.
```

2. Run the cell that defines the 15 sample incidents. Expected output:

```text
15 sample incidents defined (not inserted yet).
```

3. Run the **seed** cell. Expected output:

```text
Inserted 15 sample incidents.
```

4. Run the seed cell **again**. Expected output:

```text
Skipped: the table already has 15 incidents. No sample data was inserted.
```

The insert runs only when the table is empty, so running it again is safe.

### Step 11 - Run basic SQL queries (Section 4, continued)

1. Run the cell that prints the four queries. Expected results:

| Query | Expected result |
|---|---|
| 1) All incidents | All 15 rows, IDs 1 to 15, in order |
| 2) Critical incidents | 4 rows: IDs 2, 3, 5 and 13 |
| 3) Open incidents | 8 rows: IDs 2, 3, 4, 6, 8, 9, 14 and 15 |
| 4) Total incidents | Total incidents: 15 |

Each query uses a `%s` placeholder. The value is sent separately from the SQL text, which is how the lab prevents SQL injection. Section 5 explains this in more detail.

### Step 12 - Check the database functions (Section 5)

1. Run the cell that calls the read functions. Expected output:

```text
get_all_incidents(): 15 rows
search_incidents_by_severity('Critical'): 4 rows
search_incidents_by_status('Open'): 8 rows
get_incident_summary(): {...}
```

2. Run the cell that defines `add_incident` and `update_incident_status`. It only **defines** them. Nothing is written. The agent runs these functions later, and only after you confirm (Steps 17 and 18).

### Step 13 - Check Pydantic validation (Section 6)

1. Run the cell that defines the three Pydantic schemas. Expected output:

```text
Pydantic schemas defined: IncidentSearchInput, IncidentCreateInput, IncidentUpdateInput
```

2. Run the demonstration cell. It builds five inputs and prints what happened to each one:

| Demonstration | Expected result |
|---|---|
| 1) Valid create request | ACCEPTED, with the values listed |
| 2) Severity `Urgent` | REJECTED: severity: Input should be 'Critical', 'High', 'Medium' or 'Low' |
| 3) Status `Done` for an update | REJECTED: status: Input should be 'Open', 'In Progress' or 'Resolved' |
| 4) `affected_system` left out | REJECTED: affected_system: Field required |
| 5) `incident_id` set to 0 | REJECTED: incident_id: Input should be greater than 0 |

A rejected input never reaches the database. Pydantic checks the **input**. It does not replace database permissions. Section 10 explains the difference.

### Step 14 - Inspect the custom tools (Section 7)

1. Run the cell that builds the five tools. Expected output starts with `5 custom tools registered:` and lists each tool with its inputs and purpose.
2. Run the safety-check cell. Expected output:

```text
Check passed: no tool accepts raw SQL or can drop, truncate or delete data.
```

| Tool | Inputs | Confirmation needed? |
|---|---|---|
| `get_all_incidents` | none | No |
| `search_incidents` | exactly one of `severity` or `status` | No |
| `get_incident_summary` | none | No |
| `create_incident` | title, description, category, severity, assigned_team, affected_system, confirmed | Yes: preview first, then your yes |
| `update_incident_status` | incident_id (above 0), status, confirmed | Yes: preview first, then your yes |

### Step 15 - Add your OpenAI key and start the agent (Section 8)

1. Open `.env` and make sure `OPENAI_API_KEY` holds your OpenAI key. Save the file.
2. In VS Code, choose **Kernel > Restart**. The kernel must restart to read the new value.
3. Run all the code cells again from the top, in order, up to and including the agent cell in Section 8. The agent cell depends on the database and tool cells above it.
4. Check the outputs. The imports cell should show `OPENAI_API_KEY set: True`. The agent cell should show:

```text
Agent ready. Model: gpt-4o-mini | max steps: 8
```

> **Warning:** If you see `Agent NOT created: OPENAI_API_KEY is missing in .env`, the key was not loaded. Check the spelling in `.env`, save the file, restart the kernel and run the cells again from the top.

### Step 16 - Run the read scenarios (Section 9: Scenarios 1 and 2)

1. Run the cell for Scenarios 1 and 2. It sends two requests to the agent:

- **Scenario 1:** *Show me all open IT incidents.* Expected tool: `search_incidents` with status Open. The agent lists **8** incidents.
- **Scenario 2:** *Show me all critical incidents.* Expected tool: `search_incidents` with severity Critical. The agent lists **4** incidents.

2. Read the trace. Lines starting with `>` come from the agent. The line `TOOLS CALLED:` shows which tool the agent chose. This is how you see the agent choose a tool.

Scenarios 1 and 2 only read data. They never change anything.

### Step 17 - Run the create scenario with confirmation (Scenario 3)

1. Run the Scenario 3 cell. It sends three messages to the agent, one after another. The messages are already written in the cell.
2. Check each reply:

| Message | What you should see |
|---|---|
| 1. A high-severity database incident for payment timeouts, assigned to the Database Support Team | The agent asks for the **affected system**. It does not guess. `TOOLS CALLED: none`. |
| 2. The affected system is the Payments Database. | The agent calls `create_incident` with `confirmed=false`. It shows a **preview** and asks *Shall I save this?*. Nothing has been saved yet. |
| 3. Yes, please save it. | The agent calls `create_incident` with `confirmed=true`. It reports **SAVED** with the new incident ID, which is **#16** on a fresh setup. |

> **Key idea:** The write is blocked until **your own message** says yes. The agent cannot approve its own change. The code checks the words you typed. The preview and the confirmed call must also match exactly.

> **Warning:** Run this cell **once**. Running it again creates another incident.

### Step 18 - Run the update scenario (Scenario 4)

1. Run the Scenario 4 cell. It sends two messages:

- *Update incident 3 to In Progress.* The agent checks incident 3, which is currently Open, and shows a preview.
- *Yes, go ahead.* The agent calls `update_incident_status` with `confirmed=true`. It reports the status the **database** now shows.

2. Confirm that the reply says the database shows incident 3 as In Progress.

> **Warning:** Run this cell once. Each run performs another write.

### Step 19 - Run the summary scenario (Scenario 5)

1. Run the Scenario 5 cell. It asks for a summary of the current incident situation.
2. The agent calls `get_incident_summary` and reports the totals. The numbers depend on which scenarios you have already run:

| Measure | Before Scenarios 3 and 4 | After Scenarios 3 and 4 |
|---|---|---|
| Total incidents | 15 | 16 |
| By severity (Critical / High / Medium / Low) | 4 / 4 / 5 / 2 | 4 / 5 / 5 / 2 |
| By status (Open / In Progress / Resolved) | 8 / 4 / 3 | 8 / 5 / 3 |
| Unresolved Critical incidents | #2, #3 and #13 | #2, #3 and #13 |

### Step 20 - Ask your own question (optional)

1. Click below the last cell and insert a new code cell.
2. Type one of the lines below, and press Shift + Enter:

```text
chat_with_agent("Show me all High-severity incidents.", [])
```

Try these questions. Each one teaches a different point:

- *Show me all High-severity incidents.* The agent uses `search_incidents`.
- *Show me the incidents assigned to the Network Operations team.* The search tool filters only by severity or status, so the agent should explain its limits, or use another tool and filter the results.
- *Delete incident 2.* There is no delete tool, so the agent should refuse.

To continue a conversation, create a list first, for example `my_history = []`, and pass the same list to each call: `chat_with_agent("...", my_history)`.

### Step 21 - Run the security self-check (Section 10)

1. Run the self-check cell. Expected output:

- `Tools available to the agent:` followed by the five tool names.
- `Database password appears in the agent prompt: False`. The agent's instructions never contain the password.
- `CHECK constraints on the incidents table:` followed by three names, one each for category, severity and status. The database itself rejects any value outside the allowed lists.
- `Incidents in the database now:` followed by the current total.

### Step 22 - Practise least privilege (recommended)

In production, the agent should use an account that can do only what the tools need. This step creates that account and tests it.

1. In the Supabase dashboard, open **SQL Editor** and choose **New query**.
2. Paste the SQL below. Replace `REPLACE_WITH_A_STRONG_PASSWORD` with a strong password, then click **Run**.

```text
CREATE ROLE it_agent_app LOGIN PASSWORD 'REPLACE_WITH_A_STRONG_PASSWORD';
GRANT CONNECT ON DATABASE postgres TO it_agent_app;
GRANT USAGE ON SCHEMA public TO it_agent_app;
GRANT SELECT, INSERT, UPDATE ON TABLE incidents TO it_agent_app;
GRANT USAGE, SELECT ON SEQUENCE incidents_incident_id_seq TO it_agent_app;
```

3. Save the new password in your password manager.
4. In `.env`, set `SUPABASE_DB_USER` to `it_agent_app` and `SUPABASE_DB_PASSWORD` to the new password. With the pooler, the user name may need the project reference, for example `it_agent_app.<project-ref>`. Use the format that works for your connection.
5. Save `.env`, restart the kernel, and run the connection test and Scenario 1 again. Both should work.
6. Note what this account can do: read incidents, add incidents and update statuses. The database refuses DELETE, TRUNCATE, ALTER, CREATE TABLE and DROP TABLE for this account. A refused request shows `Permission denied ... (error code 42501)`.
7. **Switch back to the owner account** before you run the table setup cells again. Set `.env` back to your original user name and password, then restart the kernel.

> **Tip:** The table setup cells need the owner account. Running them with `it_agent_app` shows the permission message above. That is the control working as designed.

### Step 23 - Complete the exercises (Section 11)

Try each exercise yourself before you read the expected outcome in the table below.

1. **Exercise 1 - Incident search.** In the exercise cell, replace the `TODO` text in `exercise_1_turns` with your own request to find all High-severity incidents. Run the cell.
2. **Exercise 2 - Incident creation.** Replace the two `TODO` texts in `exercise_2_turns`. The first asks the agent to create a new Network incident. The second is your reply, or `yes` when the agent previews the incident. If the agent asks for more details, add another line to the list.
3. **Exercise 3 - Incident update.** Replace the two `TODO` texts in `exercise_3_turns`. Ask the agent to update an incident that is not yet Resolved, then confirm with `yes`.
4. Run the exercise cell. Any exercise whose first message still says `TODO` is skipped.

| Exercise | Expected outcome |
|---|---|
| 1. Incident search | The agent calls `search_incidents` with severity High. Before Scenario 3 there are **4** High incidents (IDs 1, 6, 8 and 12). After Scenario 3 there are **5**, because incident 16 is also High. |
| 2. Incident creation | The agent asks for any missing details and previews the incident with status Open. After your yes it reports the new ID that the database confirmed. |
| 3. Incident update | The agent previews the change and shows the current status. After your yes it updates the incident and reports the status the database now shows. |

### Step 24 - Take the knowledge check (Section 12)

1. Read the five multiple-choice questions in Section 12 of the notebook.
2. Choose your answers before you look at **Appendix B**.
3. Check your answers against Appendix B. Read the reason for any answer you missed.

### Step 25 - Review the summary (Section 13)

1. Read the ten-step workflow in Section 13 of the notebook.
2. Think of one enterprise system where the same pattern would work, such as service requests or asset management. Write down what the tools would be, and which of them would need confirmation.

## Troubleshooting

Find the message you see in the first column, then follow the fix.

| What you see | Likely cause | What to do |
|---|---|---|
| `CONNECTION FAILED: The database connection failed. Check the SUPABASE_DB_* values in .env` | Wrong host, port, user name or password. Or the network blocks the connection. Or the project is paused. | Copy the values again from the Connect dialog (Step 5). Check for typos, extra spaces or quotes. Restart the kernel. Restore a paused project in the dashboard. |
| The same message, but the host is correct | The direct connection is not reachable from your network. This often happens on IPv6-only routes. | Use the **Session pooler** details from the Connect dialog. |
| Connection works in the dashboard but fails in the notebook | The pooler user name is not in the format the dialog shows. | Use the user name exactly as shown, for example `postgres.<project-ref>`. |
| `Found a .env file in this folder: False` | The `.env` file is not in the notebook's folder. | Create `.env` in the same folder as the notebook (Step 6). Open the folder in VS Code. |
| `SUPABASE_DB_PASSWORD set: False` | The line is missing, empty, or still has the placeholder. | Edit `.env`, save it, restart the kernel and run the cells again from the top. |
| A value with `#`, spaces or quotes does not work | The value was not quoted in `.env`. | Wrap the value in single quotes, for example `SUPABASE_DB_PASSWORD='my#Pass word'`. |
| `Permission denied by the database (error code 42501)` | The account is not allowed to do this, for example creating the table with the restricted account. | Run the table setup with the owner account. Use the restricted account only for the agent (Step 22). |
| `The database rejected the request (error code ...)` | A statement was refused by a table rule, for example an invalid severity. | No change was made. Check the input against the rules in Section 4 and Section 6. |
| `Agent NOT created: OPENAI_API_KEY is missing in .env` | The key is missing, or the kernel was not restarted after you added it. | Add `OPENAI_API_KEY` to `.env`, save, restart the kernel and run the cells again from the top (Step 15). |
| OpenAI authentication or quota error | The key is wrong, or the account has no credit. | Check the key and the billing page in your OpenAI account. |
| `ModuleNotFoundError: No module named 'psycopg'` | The notebook kernel is a different Python from the one where pip installed the packages. | Select the interpreter from Step 2 in VS Code, then run `python -m pip install -r requirements.txt` again. |
| `INPUT REJECTED - nothing was run.` | The agent sent a value that is not allowed, for example a severity of `Urgent`. | Ask again with an allowed value. The agent should explain the allowed values. |
| `BLOCKED - nothing was saved.` | The agent tried to write without your yes, or the values differ from the preview. | Reply `yes` to the preview. If the agent cannot find it, ask it to show the preview again. |
| `Skipped: the table already has 15 incidents.` | The table already has data. This is expected. | Nothing to fix. |
| Two new incidents appear after you run Scenario 3 twice | Each run of Scenario 3 creates another incident. | This is expected. To start again, use **Resetting the sample data**. |

## Resetting the sample data

> **Warning:** This deletes **all** incidents in your Supabase project, including any you created. Use it only in your own lab project, and only with the owner account.

1. In the Supabase **SQL Editor**, run:

```text
DROP TABLE incidents;
```

2. In the notebook, run the Section 4 setup cells again: the CREATE TABLE cell, the sample data cell and the seed cell. The 15 sample incidents come back with IDs 1 to 15.
3. Run the later cells again as needed. Scenarios 3 and 4 can then be run once more.

## Security rules

#### Do

- Keep `.env` private. Store passwords in a password manager.
- Use the least-privilege account for the agent when you practise Step 22.
- Read each preview before you say yes. Check the values carefully.
- Ask your trainer before you change shared data, and before you reset anything.

#### Do not

- Share `.env`, or post a screenshot that shows a password or key.
- Commit `.env` to Git, or copy it to a shared drive.
- Type a real key or password into `.env.example`.
- Turn off SSL (`sslmode=require`).
- Add a general SQL tool to the agent. The lab's point is that the agent only has five safe tools.

## Appendix A - Expected results at a glance

| Check | Expected result | Step |
|---|---|---|
| Python version | 3.10.x (3.10.11 on the training workstation) | 2 |
| Connection test | `CONNECTION OK: PostgreSQL <version>` | 9 |
| Table creation | `Table 'incidents' is ready...` | 10 |
| First seed | `Inserted 15 sample incidents.` | 10 |
| Second seed | `Skipped: the table already has 15 incidents.` | 10 |
| Total incidents | 15 | 11 |
| Critical incidents | 4 (IDs 2, 3, 5, 13) | 11 |
| Open incidents | 8 (IDs 2, 3, 4, 6, 8, 9, 14, 15) | 11 |
| Pydantic demonstrations | 1 accepted, 4 rejected with the reasons shown in Step 13 | 13 |
| Tools registered | `5 custom tools registered` | 14 |
| Agent ready | `Agent ready. Model: gpt-4o-mini \| max steps: 8` | 15 |
| Scenario 1 | Tool `search_incidents`, 8 open incidents | 16 |
| Scenario 2 | Tool `search_incidents`, 4 critical incidents | 16 |
| Scenario 3 | Preview, then `SAVED` with ID #16 (on a fresh setup) | 17 |
| Scenario 4 | Preview, then `UPDATED` for incident 3 | 18 |
| Scenario 5 | Summary with totals and unresolved Critical incidents | 19 |
| Security self-check | Password not in the prompt: `False`. Three CHECK constraints. | 21 |

## Appendix B - Knowledge check answers

The questions are in Section 12 of the notebook. Answer them before you read this table.

| Question | Answer | Why |
|---|---|---|
| 1. Purpose of a SQL database agent | B | The agent chooses authorised tools that run validated database operations, then reports the results. |
| 2. Role of Pydantic schemas | B | Pydantic validates tool inputs (allowed values, required fields, lengths) before any database work happens. |
| 3. Purpose of authenticated connections | B | Only identified, authorised credentials can connect, and the agent works only through them. |
| 4. Why parameterised queries | B | Values are sent separately from the SQL text, so user input cannot change the structure of the query. |
| 5. Why no arbitrary SQL tool | B | It could run destructive or unauthorised SQL, which validation cannot fully control. |
