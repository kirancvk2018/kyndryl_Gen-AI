# Module 8 – Lab 1: Build an Agentic IT Operations Assistant

User guide: step-by-step instructions to run the lab on Windows

| **Item** | **Details** |
|---|---|
| Audience | Module 8 participants who have set up the Module 7 Python environment (Labs 1 and 2) |
| Time needed | About 90 to 120 minutes. Each agent request can take several seconds to a minute. |
| Lab folder | `Module8_Lab1_Agentic_Operations` |
| Main file | `module8_lab1_agentic_operations.ipynb` (the notebook you will run) |
| Python | The Python already installed on your computer (verified with Python 3.10.11). Do not install another Python. |
| LangChain | langchain 1.3.14, the same version as Module 7. Installed in Part 2. |
| What you need | VS Code with the Python and Jupyter extensions, an OpenAI API key for Parts 6 to 10, and internet access |

## About this lab

In this lab you build an **AI agent** for an IT Operations team. You type a request in plain English, for example “Analyze the application logs and count the critical errors”. The agent decides which tools to use, runs them, reads what they return, and then writes an answer based on those results.

The agent has three tool categories:

- **File Management**: list, search and read the files in `operations_workspace`, and write new report files there.
- **Python REPL**: run small calculations, such as averages, maxima and counts.
- **Web/Search**: look up general public technical information. It does not need an API key.

You will watch the agent choose tools in its verbose trace. You will then run four operations use cases: log analysis, capacity planning, incident investigation and operational reporting.

**What is in this guide**

- Part 1: Before you start
- Part 2: Set up Python and the packages
- Part 3: Add your OpenAI API key
- Part 4: Open the notebook in VS Code
- Part 5: Run the notebook sections that do not need a key
- Part 6: Build the agent (needs the key)
- Part 7: Watch the agent choose tools
- Part 8: Run the four use cases
- Part 9: Read how the agent executes a request
- Part 10: Exercises and quiz
- Part 11: Finish and reset
- Part 12: Troubleshooting
- Appendices: safety rules, quick reference and glossary

## Part 1 – Before you start

Check each item before you begin. Tick the box when it is ready.

| **Requirement** | **How to check** | **Ready** |
|---|---|---|
| Python 3.10 is installed | Open PowerShell and type `python --version` | ☐ |
| The lab folder is complete | The folder contains `module8_lab1_agentic_operations.ipynb`, `operations_workspace` (with three files), `requirements.txt`, `README.md`, `.env.example` and `.gitignore` | ☐ |
| VS Code has the Python and Jupyter extensions | Open VS Code, press Ctrl+Shift+X and search for “Python” and “Jupyter” | ☐ |
| You have an OpenAI API key with credit | Your facilitator gives you a key. You need it only from Part 6 onwards. | ☐ |
| You have an internet connection | The agent calls the OpenAI API and the DuckDuckGo search service while it runs | ☐ |

> **Important**
>
> Do not create a virtual environment, do not install another Python, and do not install Anaconda. Use the Python that is already on your computer.
>
> Never paste your API key into the notebook, a chat or a screenshot, and never share the `.env` file.
>
> The lab can read and write only the `operations_workspace` folder. The agent cannot delete files.

## Part 2 – Set up Python and the packages

### Step 1 – Open PowerShell in the lab folder

1. Open File Explorer and go to the `Module8_Lab1_Agentic_Operations` folder.
2. Click in the address bar, type `powershell` and press Enter.

> **Expected result**
>
> A PowerShell window opens and its prompt ends with `Module8_Lab1_Agentic_Operations>`.

### Step 2 – Check the Python interpreter

Type these two commands, pressing Enter after each one:

```text
python --version
python -m pip --version
```

> **Expected result**
>
> `Python 3.10.11` (or another 3.10 version). The pip line shows the same Python installation. If PowerShell says that `python` is not recognized, stop and ask your facilitator. Do not install Python yourself.

### Step 3 – Install the required packages

From the lab folder, run:

```text
python -m pip install -r requirements.txt
```

- Wait until the prompt (`PS ...>`) returns. The first install can take a few minutes.
- “Requirement already satisfied” lines are normal when the packages are already installed.
- You may see `Successfully installed httpx-0.28.1`. The search package needs this newer version, so it is expected.
- Do not run `pip install --upgrade`. The lab depends on the pinned versions.

### Step 4 – Confirm the LangChain version

```text
python -m pip show langchain
```

> **Expected result**
>
> A line that reads `Version: 1.3.14`. If it shows a different version, ask your facilitator before you continue.

Optionally, run the consistency check:

```text
python -m pip check
```

> **Tip**
>
> If `pip check` lists packages that are not in `requirements.txt`, they probably come from another project on the same computer. They do not stop this lab. Tell your facilitator if you are unsure.

## Part 3 – Add your OpenAI API key

Sections 1 to 6 of the notebook run without a key. Sections 7 to 10 call the OpenAI API, so you need the key before you reach Part 6.

### Step 5 – Create your .env file

The lab reads your key from a file called `.env`. Create it by copying the template:

```text
Copy-Item .env.example .env
dir .env
```

> **Expected result**
>
> No message appears after `Copy-Item`. The `dir .env` line shows a file named `.env`.

### Step 6 – Add your API key

1. Open the file in Notepad: `notepad .env`
2. Replace `your_openai_api_key_here` with your key. Keep it on one line, in this form:

```text
OPENAI_API_KEY=sk-...your key...
```

3. Save the file (Ctrl+S) and close Notepad.

> **Tip**
>
> If you cannot see file extensions, open File Explorer and choose **View > Show > File name extensions**. The file must be named `.env`, not `.env.txt`.

> **Important**
>
> Do not add quotes, spaces or a second line. Do not paste the key anywhere else.

## Part 4 – Open the notebook in VS Code

### Step 7 – Open the lab folder in VS Code

In the PowerShell window from Step 1, type:

```text
code .
```

If PowerShell says that `code` is not recognized, open VS Code, choose **File > Open Folder** and select the `Module8_Lab1_Agentic_Operations` folder.

Opening the lab folder matters. The notebook looks for `operations_workspace` in the folder it runs from.

### Step 8 – Open the notebook

In the Explorer panel (Ctrl+Shift+E), click `module8_lab1_agentic_operations.ipynb`. The notebook opens with Markdown explanations and grey code cells.

### Step 9 – Select the Python interpreter

1. Press Ctrl+Shift+P.
2. Type `Python: Select Interpreter` and press Enter.
3. Choose the Python 3.10 entry that matches the version you checked in Step 2.

### Step 10 – Select the kernel

1. At the top right of the notebook, click **Select Kernel**.
2. Choose **Python Environments** and pick the same Python 3.10 installation.

> **Expected result**
>
> The kernel name at the top right shows a Python 3.10 installation.

## Part 5 – Run the notebook sections that do not need a key

**How to run a cell**

- Click inside a code cell, then press **Shift+Enter**. The cell runs and the cursor moves to the next cell.
- Press **Ctrl+Enter** to run a cell and keep the cursor in it.
- The number in square brackets, such as `[3]`, shows the order in which cells ran. A `*` means the cell is still running.
- Run the cells **from top to bottom**. Each section uses variables created above it.
- If something looks wrong, click **Restart** in the notebook toolbar, then run again from the top.

> **Important**
>
> Do not skip cells in Section 7. The build cell creates the `run_agent` function that every later agent cell uses.

### Step 11 – Read Sections 1 and 2, then run the environment check

1. Read the Markdown cells for Section 1 (introduction to AI agents) and Section 2 (the lab environment).
2. Run the code cell that imports the libraries and prints the Python and LangChain versions.
3. Run the next code cell. It checks that a key is present without printing it, and it sets the workspace folder and the model name.

> **Expected result**
>
> The versions print without errors. The key line reads `OPENAI_API_KEY available: True` once you add a key in Part 3. Without a key it shows a warning, and Sections 1 to 6 still run. The workspace line ends with `operations_workspace`, and the model is `gpt-4o-mini`.

### Step 12 – Inspect the sample files (Section 3)

1. Run the first code cell. It lists the three files and shows the first 12 lines of `application.log`.
2. Run the second code cell. It reads `server_metrics.csv` and prints the incident notes.

> **Expected result**
>
> Three files are listed with their sizes. The log lines begin with a date, a time and a level such as INFO, WARN, ERROR or CRITICAL.

> **Tip**
>
> Look at the metric rows and the log lines yourself before you use the agent. You will be able to judge its answers better when you know the data.

### Step 13 – Try the File Management tools (Section 4)

1. Run the cell that builds the file tools. It lists the four tools the agent may use: `list_directory`, `read_file`, `file_search` and `write_file`. Copy, move and delete are not registered.
2. Run the cell that tests the read tools. It lists the workspace, searches for `*.log` files, and reads the log and the incident notes.
3. Run the cell that tests writing. It creates `lab_test_report.txt`, then tries two actions that must fail.

> **Expected result**
>
> The write test prints `File written successfully` for the new report. It prints an error when it tries to overwrite `application.log`, and an access-denied error when it tries to read `../../secret.txt`. The last lines read `unchanged: True` for all three original files.

### Step 14 – See the Python REPL restrictions (Section 5)

1. Run the cell that creates the REPL tool. It runs three blocked examples: an `import`, a call to `open`, and a double-underscore name.
2. Wait a few seconds for the fourth example, an endless loop. It is stopped after 5 seconds.
3. Run the calculation cell. It prints a basic calculation, the average CPU, the highest disk value and a capacity example.

> **Expected result**
>
> The import and the double-underscore name print readable `Error:` messages. The `open` call shows a NameError. The endless loop prints `Execution timed out`. The calculation cell prints numbers computed from `server_metrics.csv`.

> **Tip**
>
> Each REPL call takes about half a second, because it starts a helper process. That is normal.
>
> The REPL is a teaching guardrail, not a security sandbox. Read Appendix A for the rules.

### Step 15 – Run a web search (Section 6)

1. Run the search cell. It searches DuckDuckGo for a generic question about high CPU utilization.

> **Expected result**
>
> The query line, the number of characters returned, and the first 500 characters of the results. These results come from the public internet. Treat them as reference material, not facts about your systems.

## Part 6 – Build the agent (needs the API key)

### Step 16 – Register the three tool categories (Section 7)

1. Run the cell that defines the system prompt and registers the tools.

> **Expected result**
>
> `Registered tools (3 categories):` followed by six names: `list_directory`, `read_file`, `file_search`, `write_file`, `Python_REPL` and `duckduckgo_search`.

The system prompt is the instruction text given to the LLM. It tells the agent its role, the tools it may use, and the rules it must follow, such as “never invent log entries”. Read it. It is the main way to influence the agent's behaviour.

### Step 17 – Build the LangChain agent

1. Run the cell that creates the LLM, the prompt, the agent and the executor, and defines `run_agent`.

> **Expected result**
>
> `Agent ready. Model: gpt-4o-mini | max steps: 8`.

If you see `OPENAI_API_KEY is missing`, go back to Part 3, save `.env`, click **Restart** and run again from the top.

## Part 7 – Watch the agent choose tools (Section 8)

In Section 8 you do not tell the agent which tool to use. You only give the request. Each request makes the agent reason and call tools, and the trace shows what it did.

### Step 18 – Read the trace for Examples 1 and 2

1. Run the first example cell. It sends two requests: list the workspace, then calculate the average CPU.
2. For each request, read the trace from top to bottom. Note four things: the `Entering new AgentExecutor chain` line, each `Invoking:` line (the tool and the input it wrote), the output the tool returned, and the final answer.
3. Find the `TOOLS USED (in order)` line after each request. It lists the tools the agent called.

> **Why the tool order matters**
>
> The average CPU example usually reads the CSV file first, then calculates in the Python REPL. The REPL cannot read files itself, so the agent has to pass it the values.

### Step 19 – Read the trace for Examples 3 and 4

1. Run the second example cell. It sends a web search request and a log summary request.
2. Compare the tools used with the table below.

| **Request** | **Tool(s) you should expect to see** | **Why** |
|---|---|---|
| List the files available in the Operations workspace | `list_directory` | The request is about files |
| Calculate the average CPU utilization of all servers | `read_file`, then `Python_REPL` | The data is in a file, and the calculation needs Python |
| Search for common causes of high server CPU utilization | `duckduckgo_search` | General public knowledge, not in the workspace |
| Read the application logs, identify critical errors and prepare a summary | `read_file`, plus `Python_REPL` for counting | Read the logs first, then count |

> **Note**
>
> The agent may choose a different but sensible path. What matters is whether it used a tool to get the facts, instead of answering from memory. The wording of answers will differ from run to run.

## Part 8 – Run the four use cases (Section 9)

Each use case is one request. The agent has to combine tools to answer it. Compare the `TOOLS USED` list with the expected workflow in the table in Section 9 of the notebook.

The sample thresholds used in this lab are **training values, not production policies**:

- CPU above 85%: high utilization.
- Memory above 85%: high utilization.
- Disk above 90%: critical utilization.
- Network latency above 100 ms: elevated (an extra threshold for this lab).

### Step 20 – Use case 1: log analysis

1. Run the first use case cell. The agent reads `application.log`, counts the critical errors and prepares an incident summary.
2. Check one or two of its counts against `application.log` yourself.

> **Expected result**
>
> A summary that separates what the log shows from any assumptions. The tools used include `read_file` and `Python_REPL`.

### Step 21 – Use case 2: capacity planning

1. Run the second use case cell. The request states the thresholds above, so the agent uses the same rules.
2. Check any server it says is over a threshold against `server_metrics.csv`.

> **Expected result**
>
> A list of threshold breaches, a ranking by concern and recommendations. The tools used include `read_file`.

### Step 22 – Use case 3: incident investigation

1. Run the third use case cell. The agent reads `incident_notes.txt` and `application.log`, then investigates.
2. Check that the answer separates **evidence** (observed facts with timestamps) from **assumptions**.

> **Expected result**
>
> A report that does not claim a root cause. The incident notes say the root cause is still open, and a good answer keeps that position.

### Step 23 – Use case 4: operational report

1. Run the fourth use case cell. The agent saves a new file named `daily_operations_report.txt` in `operations_workspace`.
2. Run the verification cell directly below it.

> **Expected result**
>
> `Report saved: True`, the five required section headings found, and `OK` for each of the three original files. If the report was not saved, the agent's answer should say so. Do not accept an answer that claims success without a file.

1. Open the report in Notepad to read it: `notepad operations_workspace\daily_operations_report.txt`

## Part 9 – Read how the agent executes a request (Section 10)

### Step 24 – Match the steps to your trace

Read the Section 10 explanation. It describes seven steps: the user request, the agent's interpretation, the tool selection, the tool execution, the tool observation, further tool selection, and the final response.

1. Find these steps in the trace of Use case 4 (Step 23).
2. Note that an agent may call one tool or several, and that it does not call every tool for every request.

## Part 10 – Exercises and quiz (Section 11)

### Step 25 – Complete the five exercises

Add a new code cell below Section 11 for each exercise. Type `run_agent("...")` with the request in quotation marks, then press Shift+Enter. Record the `TOOLS USED` list each time.

| **No.** | **Request to type** |
|---|---|
| 1 | List all files in the Operations workspace. |
| 2 | Identify the server with the highest CPU utilization. |
| 3 | Identify and count the critical application errors in application.log. |
| 4 | Investigate incident INC-20261119-001 using incident_notes.txt and application.log. |
| 5 | Prepare an operational report covering application errors, server capacity and risks. Save it as my_report.txt in the workspace. |

> **Tip**
>
> Do not ask the agent to search the web for the contents of your logs, server names or incident IDs. Search is for generic public questions only.
>
> Exercise 5 creates `my_report.txt`. Delete it in File Explorer when you finish (see Step 27).

### Step 26 – Answer the quiz

Section 11 has five multiple-choice questions on AI agents, tool selection, File Management, the Python REPL, and tool observations. Choose one answer for each question and write it down.

> **Tip**
>
> The answer key is in the last section of the notebook. It is for the facilitator. Check your answers with your facilitator instead of reading ahead.

## Part 11 – Finish and reset

### Step 27 – Clean up the generated files (optional)

The notebook writes three generated files into `operations_workspace`: `lab_test_report.txt`, `daily_operations_report.txt`, and any `my_report.txt` you created in the exercises. The agent cannot delete files, so you remove them yourself in File Explorer.

> **Important**
>
> Delete only the generated report files. Never delete, rename or edit `application.log`, `server_metrics.csv` or `incident_notes.txt`. If one of them changes, get a fresh copy of the lab folder from your facilitator.

### Step 28 – Save and close

1. Press Ctrl+S to save the notebook.
2. Close the notebook and VS Code when you finish.
3. Never commit the `.env` file to git. The `.gitignore` file already excludes it.

## Part 12 – Troubleshooting

Find the message you see in the first column. Then follow the action in the last column.

| **What you see** | **Likely cause** | **What to do** |
|---|---|---|
| `python` is not recognized | Python is not on the PATH | Ask your facilitator to check the computer. Do not install Python. |
| `ModuleNotFoundError` for `langchain_classic`, `langchain_experimental`, `ddgs` or `dotenv` | The notebook uses an interpreter that does not have the packages | Check Steps 9 and 10, then run Step 3 in that same interpreter. |
| `OPENAI_API_KEY is missing` | `.env` is missing, misnamed or empty | Check Parts 3 and 4. Click Restart and run from the top. |
| `NameError: name 'run_agent' is not defined` | The build cell in Section 7 was skipped or failed | Restart the kernel and run every cell from the top, in order. |
| `401` with “API key has expired” or “Incorrect API key” | The key is expired, mistyped or revoked | Ask your facilitator for a new key. Update `.env`, check for extra spaces, and restart the kernel. |
| `429` or a quota or rate-limit message | Too many requests, or no credit left | Wait a minute and run again. Ask your facilitator about credit. |
| `404` or “model does not exist” | The model name is not available to your account | Ask your facilitator which model to use. Change `CHAT_MODEL` in the settings cell. |
| `operations_workspace not found` | The notebook was opened from another folder | Open the `Module8_Lab1_Agentic_Operations` folder in VS Code (Step 7), then restart the kernel. |
| `Error: imports are not allowed in the lab REPL`, or a `NameError` for `open` | Expected: the REPL blocks this on purpose | Not a fault. Rewrite the code without imports or file access. |
| `Execution timed out` | The REPL code ran for more than 5 seconds | Expected for endless loops. Simplify the code. |
| `Error: ... is an original source file and cannot be modified` | The guard protects the sample data | Expected. Write a new report file instead. |
| `Agent stopped due to max iterations.` | The agent kept calling tools without reaching an answer | Ask a narrower question. Check the trace for a repeated tool call. |
| The search returns an error or no results | DuckDuckGo is rate-limiting, or the network is blocked | Wait, then run the cell again. The agent should say that the search failed. |
| The agent answered without calling any tool | The model chose to answer from memory | Repeat the request and say “use the files”. Check the `TOOLS USED` list. |
| `Python REPL can execute arbitrary code. Use with caution.` | A normal warning from the REPL library | No action needed. |
| Your answers differ from a classmate's | The wording and tool path vary between runs | Compare the numbers and timestamps, not the wording. |
| `pip check` lists packages you did not install | Another project on the same computer | Not a blocker for this lab. Tell your facilitator if unsure. |

## Appendix A – Safety rules

The lab limits what each tool may do. These limits are part of the lesson, so do not try to bypass them.

| **Tool** | **Allowed** | **Blocked** |
|---|---|---|
| File Management | List the workspace folder, search file names, read files, and write new `.txt` or `.md` reports inside `operations_workspace` | Paths outside the workspace (for example `../`), absolute paths, copy, move and delete tools, overwriting the three original files in any letter case, and other file types |
| Python REPL | Arithmetic, lists, loops, functions and `print` | `import`, `open`, `exec`, `eval`, double-underscore names, and code that runs longer than 5 seconds |
| Web/Search | Generic public technical questions | Log lines, server names, IP addresses and incident IDs. Never send internal data to a search provider. |
| Agent execution | Up to 8 tool steps per request. Tool errors are returned as text. | Destructive actions. There is no delete tool. The agent must report a failure instead of claiming success. |
| API key | Read from `.env` by `python-dotenv` | Printing, pasting into the notebook, or committing `.env` to git |

The Python REPL check and the timeout are teaching controls. They are not a security sandbox. A determined person could still find a way around them, and memory use is not capped. In production, untrusted code must run in an isolated container or service with no file or network access.

## Appendix B – Quick reference

**Commands** (type in PowerShell in the lab folder)

| **Task** | **Command** |
|---|---|
| Check Python | `python --version` |
| Check pip | `python -m pip --version` |
| Install the packages | `python -m pip install -r requirements.txt` |
| Check the LangChain version | `python -m pip show langchain` |
| Create the .env file | `Copy-Item .env.example .env` |
| Edit the .env file | `notepad .env` |
| Open the lab folder in VS Code | `code .` |
| Open the sample report | `notepad operations_workspace\daily_operations_report.txt` |

**Notebook keys**

| **Action** | **Key** |
|---|---|
| Run the current cell and move on | Shift+Enter |
| Run the current cell and stay in it | Ctrl+Enter |
| Save the notebook | Ctrl+S |
| Open the VS Code command palette | Ctrl+Shift+P |
| Open the Explorer panel | Ctrl+Shift+E |

**Notebook map**

| **Section** | **What it teaches** | **Needs the API key?** |
|---|---|---|
| 1. Introduction to AI agents | Agents, tools, tool calling, the execution loop | No |
| 2. Understanding the lab environment | Imports, versions, key check, settings | No (the check only) |
| 3. Inspect the operations workspace | The three sample files | No |
| 4. File Management tools | The four tools and the write guard | No |
| 5. Python REPL tool | Restricted calculations and blocked code | No |
| 6. Web/Search tool | A generic DuckDuckGo search | No (internet needed) |
| 7. Build the LangChain agent | Tools, prompt, LLM and executor | Yes |
| 8. Observe agent tool selection | Four requests and their traces | Yes |
| 9. Practical IT Operations use cases | Four use cases and the report | Yes |
| 10. Understanding agent execution | The execution steps (reading only) | No |
| 11. Exercises and quiz | Five exercises and five questions | Yes, for the exercises |

## Appendix C – Glossary

| **Term** | **Meaning in this lab** |
|---|---|
| Agent | A program that uses an LLM to decide what to do next, call tools, and answer from their results |
| LLM | Large language model. This lab uses `gpt-4o-mini` through the OpenAI API. |
| Tool | A function with a name and a description. The LLM reads the description to decide when to use it. |
| Tool calling | The LLM asks for a tool to run with specific inputs. The program runs the tool and returns the result. |
| Tool observation | The output a tool returned. The agent reads it before its next step or final answer. |
| AgentExecutor | The loop that runs the agent: call the LLM, run the tool it chose, return the result, and repeat. |
| Verbose trace | The printed steps for each request: the chain start, each `Invoking:` line, the output and the final answer. |
| Iteration limit | The maximum number of tool steps per request (8 in this lab). It stops runaway loops. |
| REPL | Read-Eval-Print Loop. Here, a restricted Python tool the agent uses for calculations. |
| Kernel | The background Python process that runs the notebook cells. |
| Interpreter | The Python program that runs the code. The notebook must use the same one the packages were installed into. |
| .env file | A private text file that holds your API key. It is never shared or committed. |
| Workspace | The `operations_workspace` folder, the only folder the agent may read or write. |
| Threshold | A limit used to flag a value, such as CPU above 85%. The lab's thresholds are training values. |
| Latency | The time a network request takes, measured here in milliseconds (ms). |
| Incident | An unplanned interruption of a service. Here, incident INC-20261119-001 in the sample files. |
