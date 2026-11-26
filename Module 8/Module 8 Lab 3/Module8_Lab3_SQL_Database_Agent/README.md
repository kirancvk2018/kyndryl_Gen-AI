# Module 8 - Lab 3: Build a SQL Database Agent using LangChain

**Module:** 8 - Advanced LLM Systems &nbsp;|&nbsp; **Scenario:** IT Operations Management &nbsp;|&nbsp; **Database:** Supabase (PostgreSQL) &nbsp;|&nbsp; **Main artifact:** `module8_lab3_sql_database_agent.ipynb`

---

## 1. Lab overview

You build an **AI database agent** for an IT operations team. You type a request in plain English, for example *"Show me all critical incidents"*. The agent chooses one of five **authorized Python tools**. Each tool checks its input with **Pydantic**, then runs a **parameterized SQL** statement against a **cloud PostgreSQL database** hosted on Supabase. The agent then explains the result in business language.

The lab uses one table, `incidents`, with 15 fictional IT incidents. The agent can:

| Tool | Purpose | Changes data? |
|---|---|---|
| `get_all_incidents` | List up to 50 incidents | No |
| `search_incidents` | Search by one severity or one status | No |
| `get_incident_summary` | Counts by severity and status, plus unresolved Critical incidents | No |
| `create_incident` | Insert a new incident (status Open) | Yes, only after confirmation |
| `update_incident_status` | Change the status of one incident | Yes, only after confirmation |

The lab is about **how an LLM agent is connected to a database safely**. It is not a SQL course. The agent never writes SQL and cannot run arbitrary SQL.

## 2. Learning objectives

By the end of the lab you can:

1. Explain what a SQL database agent is and how it differs from a normal SQL application.
2. Connect Python to a cloud PostgreSQL database with authenticated, encrypted credentials stored in `.env`.
3. Create a table, insert sample data only when the table is empty, and run basic parameterized queries.
4. Validate tool inputs with Pydantic schemas, and explain why validation is not the same as database security.
5. Wrap database functions as LangChain custom tools with clear descriptions and input schemas.
6. Connect the tools to a LangChain agent and observe the tool trace.
7. Demonstrate read and write operations through natural language, including a confirmation step before every write.
8. Apply least-privilege access and explain why an LLM should never be given unrestricted SQL.

## 3. Prerequisites

- Windows with **Python already installed**. The lab uses that interpreter (Python 3.10.11 on the training workstation).
- **VS Code** with the Python and Jupyter extensions.
- **Module 8 Lab 1** completed (or Module 7 Labs 1 and 2). This lab reuses the same LangChain versions.
- A **free Supabase account**. Sign up at supabase.com.
- An **OpenAI API key** with available credit. Only Sections 8 to 11 need it. Sections 1 to 7 need only the database.
- Internet access for Supabase and OpenAI.

## 4. Supabase account and database setup

Follow these steps once. Supabase screens change from time to time, so follow the wording you see.

1. **Create a free Supabase account** at supabase.com.
2. **Create a new project.** Name it (for example `it-ops-lab`), choose a region near you, and set a **strong database password**. Store the password in a password manager. You can reset it later under **Project Settings > Database**.
3. **Find the PostgreSQL connection details.** Open the project, click **Connect** near the top of the dashboard, and find the PostgreSQL connection details. You need the **host**, **port**, **database name**, **user** and **password**.
4. **Choose a reachable connection type.** The direct connection can fail on networks without IPv6. If you cannot connect, use the **Session pooler** details from the same dialog. Copy the user name exactly as it appears, because pooler user names can include the project reference (for example `postgres.<project-ref>`).
5. **Create your `.env` file** (see Section 8).
6. **Check the connection** by running Section 3 of the notebook. You should see `CONNECTION OK`.

**Two different credentials:**
- **Supabase project URL and API keys** authenticate Supabase's web and app APIs. This lab does **not** use them.
- **PostgreSQL database credentials** (host, port, database name, user, password) authenticate a direct SQL connection. This lab uses these.

**SSL:** the notebook connects with `sslmode=require`. This encrypts the connection. Do not turn it off.

**Free-tier note:** free Supabase projects can be paused after a period of inactivity. If the connection suddenly fails, open the Supabase dashboard and restore the project.

## 5. Project structure

```text
Module8_Lab3_SQL_Database_Agent/
│
├── module8_lab3_sql_database_agent.ipynb   # the hands-on notebook (start here)
├── requirements.txt                        # packages for this lab (pinned)
├── README.md                               # this file
├── .env.example                            # template for your settings (copy to .env)
└── .gitignore                              # keeps .env and generated files out of git
```

The `.env` file is not part of the project. You create it yourself, and it must stay private.

## 6. Existing Python interpreter requirements

This lab uses the **Python interpreter already installed** on your computer. Do **not** create a virtual environment, do not run `python -m venv`, and do not install another Python version or Anaconda.

Open PowerShell in the `Module8_Lab3_SQL_Database_Agent` folder and check:

```powershell
python --version
python -m pip --version
```

Both commands must use the **same** Python installation (Python 3.10.11 on the training workstation). The notebook kernel must be that same interpreter, because that is where the packages are installed. In VS Code, choose it with **Python: Select Interpreter** (the status bar at the bottom right).

**Versions verified for this lab** (in the training interpreter):

| Package | Version | Purpose |
|---|---|---|
| `langchain` | 1.3.14 | LangChain framework (same as Module 7 and Module 8 Lab 1) |
| `langchain-core` | 1.5.3 | Tools, prompts, messages (same as Module 8 Lab 1) |
| `langchain-openai` | 1.4.2 | `ChatOpenAI` chat model (same as Module 8 Lab 1) |
| `langchain-classic` | 1.0.8 | `create_tool_calling_agent` and `AgentExecutor` (same as Module 8 Lab 1) |
| `pydantic` | 2.12.3 | Input validation for the tools |
| `psycopg` (binary) | 3.3.9 | PostgreSQL driver. **New for this lab** |
| `python-dotenv` | 1.x (`>=1.0.0`) | Reads the `.env` file. Lab 1 used the same floor. |
| `ipykernel` | 7.x | Runs the notebook in VS Code |
| OpenAI model | `gpt-4o-mini` (default) | Chat model that drives the agent |

Only `psycopg` is new compared with Module 8 Lab 1. Nothing else was upgraded.

## 7. Package installation

From the `Module8_Lab3_SQL_Database_Agent` folder:

```powershell
python -m pip install -r requirements.txt
```

Packages that are already installed are reported as `Requirement already satisfied`. That is expected. If pip tries to upgrade a LangChain package, stop and ask your trainer, because the lab depends on the pinned versions.

## 8. `.env` configuration

1. In the lab folder, copy `.env.example` and rename the copy to `.env`. In PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Open `.env` in a text editor and replace each placeholder with **your own** values:

   | Variable | Where to get it |
   |---|---|
   | `OPENAI_API_KEY` | Your OpenAI account (API keys page) |
   | `OPENAI_MODEL` | Optional. Leave the placeholder to use `gpt-4o-mini`. |
   | `SUPABASE_DB_HOST` | Supabase **Connect** dialog |
   | `SUPABASE_DB_PORT` | Usually `5432`. Use the port shown in the dialog. |
   | `SUPABASE_DB_NAME` | Usually `postgres` |
   | `SUPABASE_DB_USER` | The user from the Connect dialog (see Section 4, step 4) |
   | `SUPABASE_DB_PASSWORD` | The database password you set. Reset it in Project Settings > Database if needed. |

3. Save the file. Values with special characters, such as `#` or spaces, should be wrapped in single quotes, for example `SUPABASE_DB_PASSWORD='my#Pass word'`.

**Keep `.env` private.** Do not email it, paste it into a chat, put it in a screenshot, or commit it to git. `.gitignore` already excludes it. The notebook never prints the password, and it prints only `True` or `False` for each setting.

**Do not share your credentials with your trainer.** If you need help, describe the error message instead.

## 9. How to launch Jupyter Notebook

Choose one of these ways:

**Option A - VS Code (recommended).** Open the `Module8_Lab3_SQL_Database_Agent` folder in VS Code (**File > Open Folder**), then open `module8_lab3_sql_database_agent.ipynb`. Select the Python interpreter from Section 6 when VS Code asks for a kernel.

**Option B - Jupyter in the browser.** From the lab folder, in the same interpreter:

```powershell
python -m notebook
```

Open `module8_lab3_sql_database_agent.ipynb` from the browser page that opens. If you see `No module named notebook`, use Option A.

## 10. How to execute notebook cells

- Run a cell with **Shift + Enter** (or the play button). Run cells **in order, from top to bottom**.
- A Markdown cell explains what the next code cell does and what output to expect.
- Check the output after each cell. If a cell shows an error, fix it before going on, because later cells depend on earlier ones.
- **Run All** is fine after `.env` is ready. Stop and read the first error if one appears.
- Run each **write scenario** (Scenarios 3 and 4) **once**. Running it again creates another incident or repeats an update.
- The notebook is saved without outputs. Your results come from your own database.

| Section | Needs | Writes data? |
|---|---|---|
| 1 to 2 | Nothing (reading only) | No |
| 3 to 5 | Database | Creates table and sample data once (only when empty) |
| 6 to 7 | Nothing (validation and tool definitions) | No |
| 8 to 11 | Database and `OPENAI_API_KEY` | Only after your yes, for Scenarios 3 and 4 and Exercises 2 and 3 |
| 12 to 13 | Nothing | No |

## 11. How the custom tools work

Each tool has three parts:

1. **Name**: the name the LLM uses to call it.
2. **Description**: when to use the tool. The LLM reads this text to choose a tool.
3. **Input schema**: a Pydantic model that validates the arguments.

The notebook builds the tools with `StructuredTool.from_function`, which is the same tool class as the `@tool` decorator. It lets rejection reasons go back to the agent.

**Write confirmation (two locks).** `create_incident` and `update_incident_status` each use two steps:

1. The agent calls the tool with `confirmed=false`. The tool validates the input and returns a **preview**. Nothing is saved.
2. The agent shows the preview and asks you. Only after you reply yes does the agent call the tool with `confirmed=true`.

The code adds two checks the model cannot change:
- The confirmed call must match the previewed values exactly.
- Your **latest message** must be a clear yes (for example "yes", "yes, please save it", "go ahead").

If a lock is not satisfied, the tool returns a `BLOCKED` message and nothing is written. Section 15 explains what to do.

## 12. How Pydantic validation works

Each input schema in Section 6 of the notebook is a small class with rules:

| Rule | Example | Result when broken |
|---|---|---|
| Allowed values | `severity` must be Critical, High, Medium or Low | Rejected, with the allowed values listed |
| Required text | `title` cannot be empty or only spaces | Rejected |
| Length limits | `title` up to 200 characters, matching the table | Rejected |
| Positive ID | `incident_id` must be greater than 0 | Rejected |
| Exactly one filter | `search_incidents` needs severity **or** status | Rejected |
| Real boolean | `confirmed` must be `true` or `false`, not `"yes"` | Rejected |

A rejected input never reaches the database. The reason goes back to the agent as text, so the agent can ask you for the correct value.

**Pydantic validates inputs. It does not replace database permissions.** See Section 14.

## 13. How the agent interacts with PostgreSQL

```text
Your request (natural language)
   -> LangChain agent (ChatOpenAI chooses one tool)
   -> Pydantic validates the tool inputs
   -> Python tool function (checks the confirmation locks for writes)
   -> run_sql(): one parameterized statement on one authenticated connection
   -> PostgreSQL (Supabase) returns rows or confirms the change
   -> Tool result text (includes the database's confirmation)
   -> Agent writes the business-friendly answer
```

Important details:
- The **LLM never connects to the database**. It sees only the tool names, descriptions and results.
- Every SQL statement uses **placeholders** (`%s`), so values are sent separately from the SQL text.
- Each call opens one connection, runs the statement, commits on success or rolls back on error, and closes the connection.
- The agent says that a write succeeded only when the tool reads the row back and reports `SAVED` or `UPDATED`.

## 14. Security considerations

| Topic | What to know |
|---|---|
| Credentials | Keep the password in `.env` only. The notebook never prints it, and the agent's instructions do not contain it. |
| Encryption | `sslmode=require` encrypts the connection. Do not disable it. |
| Least privilege | Use a restricted account for the agent. The notebook's Section 10 has the SQL. The restricted account can read, insert and update, but the database refuses DELETE, TRUNCATE, ALTER, DROP and CREATE. |
| Owner account | Table setup (`CREATE TABLE`) needs the owner account. Use the owner account only for setup. |
| No arbitrary SQL | The agent has five named tools. None accepts SQL text. Do not add a general SQL tool to an LLM agent. |
| Human approval | Writes need a preview and your yes. This is a teaching guardrail. A production system adds approval outside the chat. |
| Errors | Driver errors are replaced by generic messages, so hosts, user names and passwords do not appear. |
| Prompt injection | Text inside the data could try to instruct the agent. The tools limit what any instruction can do. |
| Shared machines | Do not leave `.env` on a shared drive, and do not sign in to Supabase on a machine you do not control. |
| Trainer | Never send your password or your OpenAI key to your trainer or to anyone else. |

## 15. Troubleshooting common connection and authentication errors

The notebook shows safe messages. Use this table to match the message to a fix.

| What you see | Likely cause | What to do |
|---|---|---|
| `CONNECTION FAILED: The database connection failed. Check the SUPABASE_DB_* values in .env` | Wrong host, port, user or password. Or the network blocks the connection. Or the project is paused. | Copy the values again from the Connect dialog. Check for typos, extra spaces or quotes. Restore a paused project. |
| The same message, but the host is correct | The direct connection is not reachable from your network (often IPv6 only) | Use the **Session pooler** details from the Connect dialog. |
| Connection works in Supabase but fails here with the same values | Pooler user name is wrong | Use the user name exactly as the dialog shows it, for example `postgres.<project-ref>`. |
| `Found a .env file in this folder: False` | The `.env` file is not in the notebook's folder | Create `.env` in the same folder as the notebook. Open the folder in VS Code. |
| `SUPABASE_DB_PASSWORD set: False` | The password line is missing, empty or still the placeholder | Edit `.env`, save it, and restart the kernel (**Kernel > Restart**). |
| `Permission denied by the database (error code 42501)` | The account is not allowed to do this action (for example creating the table with the restricted account) | Run table setup with the owner account. Use the restricted account only for the agent. |
| `The database rejected the request (error code ...)` | A statement was refused, for example a rule in the table | No change was made. Read the code and the Section 4 table rules. |
| `Agent NOT created: OPENAI_API_KEY is missing in .env` | No OpenAI key | Add `OPENAI_API_KEY` to `.env`, restart the kernel, and run Section 3 again. |
| OpenAI authentication or quota error | Wrong key, or no credit | Check the key and the billing page in your OpenAI account. |
| `ModuleNotFoundError: No module named 'psycopg'` | The notebook kernel is a different Python from the one where pip installed the packages | Select the interpreter from Section 6 in VS Code, then run `python -m pip install -r requirements.txt` again. |
| `INPUT REJECTED - nothing was run. severity: Input should be ...` | The request used a value that is not allowed | Ask again with an allowed value. The agent explains the valid values. |
| `BLOCKED - nothing was saved` | The agent tried to write without your yes | Reply `yes` to the preview. If the agent cannot find the preview, ask it to show the preview again. |
| `No sample data was inserted` | The table already has data. This is expected. | Nothing to fix. |
| Re-running the `CREATE TABLE` cell gives no error | The table already exists | Expected. `IF NOT EXISTS` makes the statement safe to repeat. |

**Using Neon instead (fallback only).** If Supabase cannot be used at all, a free PostgreSQL project from Neon can provide the same five `SUPABASE_DB_*` values. Keep `sslmode=require`. Tell your trainer before you switch, because the setup steps in Section 4 are different. Turso is not a PostgreSQL service, so this notebook cannot connect to it.

---

**Lab summary:** cloud PostgreSQL, authenticated connection, a validated table, parameterized functions, Pydantic schemas, five custom tools with a write confirmation, a LangChain agent, and a least-privilege account. The model proposes, the validated tools execute, and the database permissions decide what is allowed.
