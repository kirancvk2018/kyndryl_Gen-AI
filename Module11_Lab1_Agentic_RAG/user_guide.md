# Module 11 Lab 1: Agentic RAG for IT Infrastructure Operations

User guide: how to run this project step by step on Windows

Project folder: Module11_Lab1_Agentic_RAG. Prepared 26 November 2026.

## About this lab

This lab builds an IT Infrastructure Operations AI Assistant. It answers operations questions by combining three sources:

- A **vector knowledge base** of 12 IT procedures, searched by meaning.
- Four **read-only Excel tools** that read servers, incidents and services from `it_infrastructure_data.xlsx`.
- An **LLM judge** that scores the assistant's answers.

The assistant also records OpenTelemetry traces, which you can view in Jaeger. All data in the lab is fictional. The notebook `module11_lab1_agentic_rag_infrastructure.ipynb` contains the complete lab: the code and the instructions.

## 1. Before you start

Check each item below before you begin Step 1.

| Item | Why you need it | How to check |
| --- | --- | --- |
| Windows PC with Visual Studio Code and the Jupyter extension | Runs the notebook | Open VS Code and check that the Jupyter extension is installed |
| Python 3.10 | The lab is built for Python 3.10. Do not install another Python version for this lab. | Run `python --version` in a terminal. It should show Python 3.10.x |
| OpenAI API key with billing enabled | Powers the chat model and the embeddings | Your key starts with `sk-`, and your OpenAI account has billing or credit |
| Internet access | Calls the OpenAI API and downloads the Jaeger image | Open any website |
| Docker Desktop (optional) | Runs Jaeger, the trace viewer, for Section 10 | Run `docker --version` in a terminal |
| Free disk space | pip needs space to install the packages | If pip reports `No space left on device`, free space on the drive where Python is installed |

## 2. Run the project, step by step

### Step 1: Open the project folder

1. Start Visual Studio Code.
2. Choose **File > Open Folder** and select the folder `Module11_Lab1_Agentic_RAG`.
3. Check that the folder contains these files: `module11_lab1_agentic_rag_infrastructure.ipynb`, `it_infrastructure_data.xlsx`, `requirements.txt`, `README.md`, `.env.example`, `.gitignore` and `docker-compose.yml`.

> **Important:** open the project folder itself, not a folder above it. The notebook reads the `.env` file and the Excel workbook from the folder it runs in.

### Step 2: Select the Python 3.10 interpreter

1. Press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and pick the existing **Python 3.10** interpreter.
2. Open a terminal with **Terminal > New Terminal**. It opens in the project folder.
3. Run the command below. The output should start with `Python 3.10`.

```text
python --version
```

Do not create a virtual environment or a new Conda environment for this lab. Use the existing Python 3.10 installation.

### Step 3: Install the packages

1. In the terminal, run the command below.
2. Wait until the command finishes without errors.

```text
python -m pip install -r requirements.txt
```

The packages are pinned to these versions in `requirements.txt`:

- langchain 1.3.14, langchain-core 1.5.3, langchain-openai 1.4.2, langchain-community 0.4.2
- openai 2.54.0, faiss-cpu 1.14.3
- pandas 2.3.3, openpyxl 3.1.5, python-dotenv 1.2.4
- opentelemetry-api, opentelemetry-sdk and the OTLP HTTP exporter 1.44.0
- ipykernel 7.3.0 (lets VS Code run the notebook)

pip checks nothing beyond the installation. The first code cell of the notebook prints the installed version of each package, so you can confirm the installation there.

### Step 4: Add your OpenAI API key

1. In the terminal, make a private copy of the template. This creates the file `.env`:

```text
Copy-Item .env.example .env
```

> **Check first:** if a `.env` file already exists, do not run this command, because it replaces the file and any key in it. Open the existing `.env` instead.

1. Open `.env` in VS Code.
2. Replace the placeholder `your_openai_api_key_here` with your own key. Leave the other lines unchanged: `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `OTEL_SERVICE_NAME` and `OTEL_EXPORTER_OTLP_ENDPOINT`.
3. Save the file.

> **Keep your key private.** Put the key in `.env` only. Do not put it in `.env.example`, the notebook, a chat or a document. `.env` is listed in `.gitignore`, so Git does not track it. `.env.example` is only a template and must keep the placeholder.

When the Section 2 cell runs correctly, it prints `OpenAI key found (value hidden)`.

### Step 5: Start Jaeger (optional)

Jaeger is needed only for Section 10. You can skip this step if you only want to run the agent. The notebook still runs without Jaeger, but the trace export messages will appear.

1. Start **Docker Desktop** and wait until it reports that it is running.
2. In the project folder, run the command below.

```text
docker compose up -d
```

- Jaeger web interface: http://localhost:16686
- Trace receiver used by the notebook (OTLP over HTTP): http://localhost:4318

### Step 6: Open the notebook and select the kernel

1. In VS Code, open `module11_lab1_agentic_rag_infrastructure.ipynb`.
2. At the top right of the notebook, choose **Select Kernel** and pick the **Python 3.10** interpreter from Step 2.
3. If you change `.env` after the kernel has started, restart the kernel with **Restart** in the notebook toolbar. The kernel keeps the values it loaded the first time, so a restart is needed before the new key is used.

### Step 7: Run the notebook cells in order

Use **Run All**, or click each cell and press **Shift+Enter**, from top to bottom. Do not skip cells, because later cells use variables created by earlier cells. Compare each section with the expected result below.

| Section | What the cells do | What you should see |
| --- | --- | --- |
| 2. Environment setup | Checks the packages, loads the key from `.env`, and creates the chat model and the embedding model. No API call is made yet. | The installed version of each package, then `OpenAI key found (value hidden)` and the model names |
| 3. Excel dataset | Creates `it_infrastructure_data.xlsx` if it is missing, then loads it and checks the columns. | `All required columns were found in all three worksheets`. The workbook has 14 infrastructure rows, 14 incidents and 9 services |
| 4. Vector knowledge base | Sends the 12 procedures to the OpenAI embedding model and builds the FAISS index. Then tests retrieval with a memory question. | `Vectors stored in the FAISS index: 12`. For the memory question, the "High Memory Utilization Troubleshooting" procedure should rank first |
| 5. Excel tools | Defines and tests the four read-only tools. | The four tool names. SRV-102 returns one Production server. SRV-999 returns `No server found` |
| 6. RAG tool | Wraps the vector search as the `search_knowledge_base` tool. | Three numbered matches, each with a distance |
| 7. Agent | Builds the agent and asks one test question about server SRV-104. | One call to `search_server_details` with SRV-104. The status is Running |
| 8. Five scenarios | Runs five questions: knowledge only, Excel only, both sources, incident investigation, and summary. | A summary table of the tools called in order. Expected paths: scenario 1 knowledge base only; scenario 2 server details only; scenarios 3 to 5 Excel tool first, then the knowledge base. Wording varies between runs |
| 9. OpenTelemetry | Sets up trace export to http://localhost:4318. | `Tracing configured. Service name: it-infrastructure-agent` |
| 10. Jaeger traces | Checks the Jaeger web interface, then runs scenario 3 again and exports its trace. | With Jaeger running: `Jaeger UI is reachable. HTTP status: 200`, then `Spans sent`. Without Jaeger: `Jaeger UI is not reachable yet`, which is expected |
| 11. Evaluation | Asks six questions. The LLM judge scores Relevance, Groundedness and Completeness; a code rule scores Tool Usage. | A score table with values from 1 to 5 and a table of the judge's reasons |
| 12. Summary | Text only. It recaps the architecture and has a five-question knowledge check. | No output. Answer the knowledge check questions yourself |

### Step 8: View the traces in Jaeger (optional)

1. Confirm that the Section 10 check printed `Jaeger UI is reachable`.
2. Open http://localhost:16686 in a browser.
3. On the **Search** page, set **Service** to `it-infrastructure-agent` and select **Find Traces**.
4. Open the trace named **IT Infrastructure Operations Assistant**.

In the trace view, each row is a **span**, one timed step. Indentation shows parent and child relationships. Click a span to see its duration, its tags (for example `tool.matches`) and its status. A failed span is shown in red with the error message.

The expected shape of the trace is:

```text
IT Infrastructure Operations Assistant      whole question
|-- User Query                               question received and checked
`-- Agent Execution                          the LLM and tools loop
    |-- LLM Tool Decision       step 1        model asks for a tool
    |-- Excel Server Lookup                   tool runs, reports matches
    |-- LLM Tool Decision       step 2        model asks for another tool
    |-- RAG Knowledge Retrieval               vector search, documents retrieved
    `-- LLM Response Generation               final answer, no more tool calls
```

> **Note:** traces are exported only from Section 9 onward. The test question in Section 7 and the scenarios in Section 8 run before tracing is configured, so they do not appear in Jaeger.

### Step 9: Read the evaluation results

1. Read the score table in Section 11. Relevance, Groundedness and Completeness come from the LLM judge and range from 1 (very poor) to 5 (excellent). Tool Usage comes from a code rule, not from the LLM.
2. Read the judge reasons table next to it.
3. For any score of 1 or 2, read the judge reason and the tool path. A Tool Usage score below 4 means the agent skipped an expected source or used an unexpected one.
4. Check at least two answers yourself against `it_infrastructure_data.xlsx` and the knowledge base. Record your verdict in the **Human verified** column of your own copy of the results.

Automated scores are not the same as human-verified correctness. Small score changes between runs are normal. Look for large changes in the tool path or in the facts.

### Step 10: Stop Jaeger and finish

1. When you have finished, stop Jaeger in the project folder:

```text
docker compose down
```

1. Optional: restart the kernel to clear its state.
2. Do not commit or share your `.env` file.

## 3. Troubleshooting

| Symptom | Cause | What to do |
| --- | --- | --- |
| `OPENAI_API_KEY is missing or still the placeholder` | `.env` is missing, the placeholder was not replaced, or the key was typed into `.env.example` | Complete Step 4 in `.env`, restart the kernel, then run the Section 2 cell again |
| `AuthenticationError` or `Error code: 401` with `invalid_api_key` | The key is wrong, cut off, or has extra spaces | Copy the key again into `.env`, restart the kernel, then run again |
| `insufficient_quota` | The OpenAI account has no billing or credit | Check the billing page of your OpenAI account |
| `ModuleNotFoundError` or `NOT INSTALLED` in the first cell | The packages were installed into a different interpreter | Select Python 3.10 (Step 2), run Step 3 again, then restart the kernel |
| No kernel, or the notebook does not run | The wrong interpreter is selected, or ipykernel is missing | Select the Python 3.10 kernel. Run Step 3 to install ipykernel |
| `No space left on device` during pip | The drive where Python is installed is full | Free disk space, then run Step 3 again |
| `Workbook ... is missing columns` | An older workbook with different columns exists | Delete `it_infrastructure_data.xlsx`, then run the Section 3 cell again |
| Jaeger UI is not reachable | Docker Desktop is not running, or Jaeger has not started | Start Docker Desktop, run `docker compose up -d`, then open http://localhost:16686 |
| `Failed to export span batch` or `connection refused` in the output | Jaeger is not running | The notebook keeps working. Start Jaeger, then run the Section 10 trace cell again |
| `Tracing is already configured in this kernel` | Section 9 already ran in this kernel | Restart the kernel, then run Sections 2 to 9 again |
| Traces do not appear in Jaeger | Section 9 did not run in this kernel, or the spans were not sent yet | Restart the kernel, run Sections 2 to 10, then run the trace cell and search again |
| The agent says the step limit was reached | The question needs more tool calls than MAX_MODEL_STEPS allows | Ask a narrower question, or raise MAX_MODEL_STEPS in the Section 7 cell |
| `Spans sent` is printed, but Jaeger shows nothing | The message is printed after the flush even when the export failed | Read the export messages above it, and check that Jaeger is running |
| Evaluation scores differ from earlier runs | The LLM is not perfectly repeatable | Small differences are normal. Look for large changes in the tool path or the facts |

## 4. Project files

| File | Purpose |
| --- | --- |
| `module11_lab1_agentic_rag_infrastructure.ipynb` | The complete lab: code and instructions |
| `it_infrastructure_data.xlsx` | Excel data with the Infrastructure, Incidents and Service_Inventory sheets. Section 3 creates it if it is missing |
| `requirements.txt` | The Python packages, with pinned versions |
| `README.md` | The lab instructions and notes |
| `.env.example` | Template for your settings. Keep the placeholder in it |
| `.env` | Your private settings, created in Step 4. Never share it |
| `.gitignore` | Lists files that must not be shared, including `.env` |
| `docker-compose.yml` | Starts Jaeger with `docker compose up -d` |

## 5. Notes and limits

- The Excel tools only read data. They cannot change the workbook, and they never run code or SQL written by the model.
- The agent uses one LLM instance for answering and for judging. The model is set by `OPENAI_MODEL` in `.env`.
- The vector index lives in memory. It is rebuilt each time Section 4 runs.
- The agent allows at most six model turns per question (`MAX_MODEL_STEPS`).
- A full run makes several OpenAI calls (embeddings, agent steps and the judge). The cost is small, but it is not zero. Check your OpenAI usage page.
- Do not record real credentials, real server names or confidential data in this lab.

## 6. About this guide

The steps were checked on Windows 11 with Python 3.10.11 and the package versions in `requirements.txt`. With a valid OpenAI key, the notebook ran from the first cell to the last without errors. Trace export was checked by receiving the trace data locally on port 4318. The Jaeger web pages were not checked, because Docker Desktop was not installed on that machine.
