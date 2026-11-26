# Module 11 Lab: End-to-End Agentic RAG for IT Infrastructure Operations

You will build an **IT Infrastructure Operations AI Assistant**. It answers operations questions by combining a vector knowledge base (IT procedures) with Excel tools (servers, incidents, services). It also records OpenTelemetry traces and scores its own answers.

All data in this lab is fictional.

---

## 1. Learning objectives

By the end of the lab you can:

1. Explain the difference between traditional RAG and agentic RAG.
2. Build a small vector knowledge base with embeddings and FAISS.
3. Create LangChain custom tools that read and search Excel data.
4. Explain how an LLM selects and calls a tool.
5. Run an agent that uses RAG and Excel tools in one multi-step answer.
6. Read the trace of one question in Jaeger, including parent and child spans.
7. Evaluate answers for relevance, groundedness, completeness and tool usage.

---

## 2. Prerequisites

| Item | Why you need it |
|---|---|
| Windows PC with **VS Code** and the **Jupyter** extension | Runs the notebook |
| The **existing Python 3.10** interpreter used for your training | Runs the code. Do not install another Python. |
| An **OpenAI API key** with billing enabled | Powers the LLM and the embeddings |
| **Docker Desktop** (optional for the notebook, required for Jaeger) | Runs Jaeger, the trace viewer |
| Internet access | Calls the OpenAI API and pulls the Jaeger image |

---

## 3. Project files

```
Module11_Lab1_Agentic_RAG/
├── module11_lab1_agentic_rag_infrastructure.ipynb   the complete lab (code and instructions)
├── it_infrastructure_data.xlsx                      Excel data (created by the notebook if missing)
├── requirements.txt                                 Python packages
├── README.md                                        this file
├── .env.example                                     template for your API key
├── .gitignore                                       files that must not be shared
└── docker-compose.yml                               starts Jaeger
```

---

## 4. Python interpreter

1. Open the `Module11_Lab1_Agentic_RAG` folder in VS Code (**File > Open Folder**).
2. Press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and pick the **existing Python 3.10** interpreter.
3. Do **not** create a virtual environment or a new Conda environment for this lab.

---

## 5. Install the packages

Open a terminal in VS Code (**Terminal > New Terminal**) in the project folder and run:

```powershell
python -m pip install -r requirements.txt
```

If pip reports `No space left on device`, free space on the drive where Python is installed, then run the command again.

The command checks nothing else. The notebook's first code cell prints the installed version of each package, so you can confirm the install.

---

## 6. Configure your OpenAI key

1. Copy `.env.example` and name the copy `.env`. In PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Open `.env` in VS Code and replace `your_openai_api_key_here` with your key.
3. Keep `.env` private. It is listed in `.gitignore`, so Git does not track it. Never paste the key into a notebook, a chat or a document.

If the key is missing, the notebook's Section 2 cell stops with this message: `OPENAI_API_KEY is missing or still the placeholder`. Fix `.env`, restart the kernel (**Restart** in the notebook toolbar), and run the cell again.

---

## 7. Start Jaeger (Docker Desktop)

Jaeger is needed only for Section 10. Start Docker Desktop first, then run this in the project folder:

```powershell
docker compose up -d
```

- Jaeger web UI: **http://localhost:16686**
- Trace receiver (OTLP over HTTP): **http://localhost:4318** (the notebook sends traces here)

To stop Jaeger when you have finished:

```powershell
docker compose down
```

---

## 8. Open and run the notebook

1. In VS Code, open `module11_lab1_agentic_rag_infrastructure.ipynb`.
2. Select the **Python 3.10** interpreter as the kernel (top right of the notebook).
3. Run the cells **in order, from top to bottom**. Use **Run All** or run each cell with `Shift+Enter`.
4. Read the description and the expected output below each section.

| Section | What you do |
|---|---|
| 1 | Read the introduction to Agentic RAG |
| 2 | Check packages, load your key, create the LLM and embeddings |
| 3 | Create (if missing) and inspect the Excel workbook |
| 4 | Build the FAISS vector knowledge base and test retrieval |
| 5 | Build and test the four Excel tools |
| 6 | Wrap the vector search as the `search_knowledge_base` tool |
| 7 | Build the agent and run a simple test |
| 8 | Run five scenarios and read the tool path of each one |
| 9 | Configure OpenTelemetry and OTLP export |
| 10 | Start Jaeger, run a trace, and explore it in the Jaeger UI |
| 11 | Run the six-question evaluation and read the scores |
| 12 | Review the summary and answer the knowledge check |

---

## 9. View traces in Jaeger

1. Confirm Jaeger is running (`docker compose up -d`). The check cell in Section 10 should print that the UI is reachable.
2. Run the Section 10 cells.
3. Open **http://localhost:16686**.
4. On the **Search** page, choose **Service** = `it-infrastructure-agent`, then select **Find Traces**.
5. Open the trace named **IT Infrastructure Operations Assistant**.

In the trace view:
- Each row is a **span**: one timed step.
- Indentation shows **parent and child** relationships. For example, `Excel Server Lookup` sits inside `Agent Execution`.
- Click a span to see its duration, its tags (such as `tool.matches`) and its status. A failed span is shown in red with the error message.

---

## 10. Run the response evaluation

Run the Section 11 cells. The notebook:

1. Asks the agent six questions from a fixed evaluation set.
2. Asks the LLM judge to score Relevance, Groundedness and Completeness from 1 to 5.
3. Scores Tool Usage with a code rule (no LLM).
4. Shows the scores and the judge's reasons in two tables.

Automated scores are not the same as human-verified correctness. Check at least two answers yourself against the workbook and the knowledge base, and fill in the *Human verified* column in your own copy of the results.

---

## 11. Stop Jaeger

```powershell
docker compose down
```

---

## 12. Common errors and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `OPENAI_API_KEY is missing or still the placeholder` | `.env` not created, or the key was not replaced | Complete Section 6, restart the kernel, run again |
| `ModuleNotFoundError` or `NOT INSTALLED` in the first cell | Packages not installed in this interpreter | Run `python -m pip install -r requirements.txt` in the project folder, then restart the kernel |
| No kernel, or the notebook does not run | `ipykernel` missing, or the wrong interpreter selected | Select the Python 3.10 interpreter; install `ipykernel` with the command in Section 5 |
| `AuthenticationError` or `insufficient_quota` | The key is wrong, or the OpenAI account has no billing or credit | Check the key and the billing page of your OpenAI account |
| `Workbook ... is missing columns` | An older workbook with different columns exists | Delete `it_infrastructure_data.xlsx`, then run the Section 3 cell again |
| Jaeger UI not reachable | Docker Desktop is not running, or Jaeger has not started | Start Docker Desktop, run `docker compose up -d`, check http://localhost:16686 |
| Traces do not appear in Jaeger | Section 9 not run in this kernel, or the spans were not flushed | Restart the kernel, run Sections 2 to 9 again, then run the Section 10 trace cell and search again |
| Export messages in the output, such as connection refused | Jaeger is not running | This does not stop the notebook. Start Jaeger and run the trace cell again |
| Evaluation scores differ from the expected output | The LLM is not perfectly repeatable | Small differences are normal. Look for big changes in the tool path or in the facts |
| The agent says the step limit was reached | The question needed more tool calls than `MAX_MODEL_STEPS` allows | Ask a narrower question, or raise `MAX_MODEL_STEPS` in the Section 7 cell |

---

## 13. Notes

- The Excel tools only read data. They cannot change the workbook, and they never run code or SQL written by the model.
- The agent uses one LLM instance for answering and for judging. The model is set by `OPENAI_MODEL` in `.env`.
- The vector index lives in memory. It is rebuilt each time Section 4 runs, so nothing extra is saved to disk.
- Do not record real credentials, real server names or confidential data in this lab.
