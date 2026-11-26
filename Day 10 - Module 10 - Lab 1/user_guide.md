# Module 10 – Lab 1 User Guide

Observability and Tracing for a RAG Application, using OpenTelemetry and Jaeger

| Item | Details |
| --- | --- |
| Time needed | About 60 minutes |
| Level | Beginner. No coding experience is needed. |
| Project folder | Module10_Lab1_Observability |
| Notebook | module10_lab1_observability.ipynb |
| Tools used | VS Code with Jupyter, Python 3.10, Docker Desktop, Jaeger, OpenAI API |

This guide explains how to set up and run the lab one step at a time. Follow the steps in order. Each step says what to do and what you should see when it works. If something goes wrong, check the **Troubleshooting** section near the end of this guide.

## What you will do

- Start **Jaeger**, a trace viewer, with one Docker command.
- Run a small **RAG** assistant that answers IT questions from a knowledge base.
- Record every step of the assistant with **OpenTelemetry**.
- Read the traces in the Jaeger web page and find the slow steps.
- Trigger a controlled error and find the step that caused it.

## Before you start

Check that you have each item below before you begin.

| What you need | Why you need it | How to check |
| --- | --- | --- |
| Windows 10 or 11 computer | The lab is set up for Windows. | Open Settings > System > About. |
| VS Code with the Jupyter extension | Opens and runs the notebook. | Press Ctrl+Shift+X. The Extensions list shows Jupyter. |
| Python 3.10 | Runs the code in the lab. | Run `python --version`. It should show 3.10.x. |
| Docker Desktop | Runs Jaeger. | Open Docker Desktop. It shows Engine running. |
| OpenAI API key | Lets the AI model answer questions. | Have your key ready. Never share it with anyone. |
| Project folder Module10_Lab1_Observability | Contains the lab files. | The folder holds 6 files (see the Project files table at the end). |

## Part 1 – Set up the project

### Step 1 – Open a terminal in the project folder

A terminal is the window where you type commands. It must be opened inside the project folder.

1. Open File Explorer and go to the folder **Module10_Lab1_Observability**.
2. Click the address bar at the top, type `cmd`, and press Enter. A black terminal window opens in this folder.

You can also use VS Code: choose **Terminal > New Terminal** while the project folder is open.

> **What you should see**
>
> The text before the cursor ends with `Module10_Lab1_Observability>`.

### Step 2 – Check your Python version

1. In the terminal, type `python --version` and press Enter.

> **What you should see**
>
> `Python 3.10.x`, for example `Python 3.10.11`.

> **Important**
>
> Do not install another Python version and do not create a virtual environment. Use the Python 3.10 you already have.

### Step 3 – Install the required packages

1. In the terminal, type `python -m pip install -r requirements.txt` and press Enter.
2. Wait until the prompt returns. This can take a few minutes.

> **What you should see**
>
> Lines that end with `Successfully installed ...` or `Requirement already satisfied`.
>
> No red error lines at the end.

> **Important**
>
> If pip says it will change packages that you use for other courses, press Ctrl+C to stop and ask your instructor before continuing.

### Step 4 – Create your private .env file

The `.env` file stores your OpenAI API key. The notebook reads the key from this file, so you never type it into the notebook.

1. In File Explorer, open the project folder and find the file **.env.example**.
2. Copy it (Ctrl+C, then Ctrl+V). Rename the copy to exactly **.env**. The name must have no `.txt` or `.example` ending.
3. Tip: In File Explorer, open **View > Show > File name extensions** so you can see file endings.
4. Open **.env** in VS Code. Replace `your_openai_api_key_here` with your key, so the line reads `OPENAI_API_KEY=` followed by your key. Do not add quotes or spaces around the `=` sign.
5. Save the file with Ctrl+S.

> **Important**
>
> Keep the .env file private. Do not email it, upload it, or paste your key into the notebook.
>
> The notebook never displays your key.

## Part 2 – Start Jaeger

### Step 5 – Start Docker Desktop and Jaeger

1. Open **Docker Desktop**. Wait until it shows **Engine running**.
2. In the terminal from Step 1, type `docker compose up -d` and press Enter.
3. Open **http://localhost:16686** in your web browser.

The first time, Docker downloads the Jaeger image, which can take a few minutes. The `-d` option runs Jaeger in the background, so your terminal is free again.

> **What you should see**
>
> The terminal shows that the `module10-jaeger` container started.
>
> The Jaeger page loads in the browser. It has no traces yet, which is normal at this point.

## Part 3 – Run the notebook

Open **module10_lab1_observability.ipynb** in VS Code and run the cells from top to bottom. A cell is one block of code or text. To run a code cell, click it and press **Shift+Enter**, or click its play button. Do not skip cells, because later cells depend on earlier ones.

### Step 6 – Open the notebook and choose the kernel

1. In VS Code, open **module10_lab1_observability.ipynb** from the Explorer panel.
2. Click **Select Kernel** at the top right of the notebook and choose **Python 3.10**.

> **What you should see**
>
> The kernel name at the top right of the notebook shows Python 3.10.

### Step 7 – Set up the environment (Section 2)

Run the first code cell, under **Section 2 – Environment Setup**. It imports the libraries, reads your API key, and prepares tracing.

> **What you should see**
>
> `OpenAI API key found (the value is hidden for safety).`
>
> `OpenTelemetry is ready. Traces will be sent to http://localhost:4317`

> **Important**
>
> If you see `OPENAI_API_KEY was not found`, go to the Troubleshooting section. Run this cell once per session. Running it again shows a harmless warning.

### Step 8 – Check that Jaeger is running (Section 3)

Run the cell under **Section 3 – Start and Verify Jaeger**.

> **What you should see**
>
> A line that says the Jaeger UI is running at http://localhost:16686.
>
> A line that says OTLP port 4317 is open.

If either line says the service is not reachable or the port is closed, go back to Step 5.

### Step 9 – Create the knowledge base (Section 4)

Run the cell. It creates seven short, fictional IT documents inside the notebook.

> **What you should see**
>
> `Knowledge base created with 7 fictional documents`
>
> A list from KB-001 (Password Reset Procedure) to KB-007 (IT Service Desk Procedures).

### Step 10 – Test the simple RAG assistant (Section 5)

Run the cell. It finds the matching documents for a sample question and asks the AI model for an answer.

> **What you should see**
>
> The question: `How do I reset my password if I am locked out?`
>
> Retrieved document IDs: `['KB-001', 'KB-004', 'KB-007']`.
>
> An answer based on those documents. Its wording can differ from run to run.

This run does not create traces yet. Tracing starts in Step 12.

### Step 11 – Learn how a trace is built (Section 6)

Run the demo cell. It creates one parent span with two child spans and prints their IDs and durations.

> **What you should see**
>
> The parent span's Trace ID and Span ID.
>
> Both child spans show the same Trace ID as the parent.
>
> Child A takes about 200 ms, Child B about 500 ms, and the parent about 700 ms.
>
> Child A's parent span ID equals the parent's Span ID. This link is what Jaeger shows as indentation.

### Step 12 – Load the traced RAG application (Section 7)

Run the cell under **Section 7 – Instrument the RAG Application**.

> **What you should see**
>
> No output. The cell only defines the `answer_question` function, which records each step as a span.

Read the explanation below the cell. The indentation of the code matches the parent-child structure you will see in Jaeger.

### Step 13 – Ask three questions (Section 8)

Run the cell under **Section 8 – Execute the RAG Application**. It asks three IT questions.

> **What you should see**
>
> For each question, a line `Trace ID for this question:` followed by a 32-character code.
>
> The question, the number of documents retrieved, the execution time, and the response.
>
> In the test run the documents retrieved were 3, 3 and 1. Your execution times will differ.

> **Important**
>
> Write down the three Trace IDs. You will search for them in Jaeger.

## Part 4 – Explore the traces

### Step 14 – Find your traces in Jaeger (Section 9)

1. Refresh the Jaeger page at **http://localhost:16686**.
2. Under **Service**, choose **module10-rag-app**.
3. Under **Operation**, choose **RAG Application**.
4. Under **Lookback**, choose a period that includes the last hour. If you see no results, choose a longer period.
5. Click **Find Traces**. Each row is one question.
6. To open one specific question, paste its Trace ID into **Lookup by Trace ID** at the top of the page.
7. Click the trace to open it. The spans appear as a timeline. Child spans are indented under their parent: **RAG Application**, then **User Query**, then the four steps **Document Retrieval**, **Prompt Construction**, **LLM Invocation** and **Response Generation**.
8. Read the bars. A longer bar means a longer step. **LLM Invocation** is usually the longest.
9. Click a span to see its **Tags**. Look for `retrieval.documents_found`, `gen_ai.request.model` and `gen_ai.usage.input_tokens`. Token counts appear only when OpenAI returns them.

> **Think about this**
>
> Which step takes the most time? What would you change first to make the application faster?
>
> Why is it useful that **User Query** groups the four steps under one parent?
>
> The Section 6 demo also appears in Jaeger, under the Operation **Demo: Parent Operation**.

The trace stores only safe details, such as IDs, counts, timings and model names. It does not store the question text, the prompt or the answer. This is deliberate, because trace data is often viewed by many people.

### Step 15 – Create and find an error (Section 10)

1. Run the cell under **Section 10 – Error Handling and Debugging Demonstration**.
2. In Jaeger, set **Service** to **module10-rag-app**, type `error=true` in the **Tags** box, and click **Find Traces**.
3. Open the trace. Three spans are marked as errors: **Document Retrieval**, **User Query** and **RAG Application**.
4. Click **Document Retrieval** to read the error message.
5. Notice that **LLM Invocation** is missing. The failure came first, so no AI model call was made.

> **What you should see**
>
> In the notebook: `The application stopped with this error: Simulated failure: the knowledge base index is unavailable`.
>
> This error is intentional. It shows what a failure looks like in a trace.

> **Debugging rule**
>
> Start with the deepest span that is marked as an error. That is where the fault is.

## Part 5 – Finish the lab

### Step 16 – Read the summary and answer the knowledge check (Sections 11 and 12)

1. Read **Section 11 – Key Learning Outcomes**.
2. Answer the five questions in **Section 12 – Knowledge Check**.
3. Check your answers against the **Answer Key** in the last cell of the notebook.

### Step 17 – Stop Jaeger

1. In the terminal, type `docker compose down` and press Enter.

> **What you should see**
>
> The Jaeger container stops and is removed.

> **Important**
>
> Jaeger keeps traces only in memory. They disappear when Jaeger stops. Write down anything you need, such as Trace IDs and timings, before you stop it.

### Optional: use a different AI model

If your OpenAI account does not offer the model named in the notebook, change it:

1. In the Section 5 code cell, find the line `MODEL_NAME = "gpt-6-luna"`.
2. Replace the name with a chat model that your account offers.
3. Run the Section 5 cell again, then run the Section 8 cell again.

## Troubleshooting

Find your problem in the first column. Try the fix in the last column.

| Problem | Likely cause | What to do |
| --- | --- | --- |
| `OPENAI_API_KEY was not found` | The .env file is missing, has the wrong name (for example `.env.txt`), or still has the placeholder. | Rename the file to exactly `.env` in the project folder. Put your key after `OPENAI_API_KEY=`. Save it, then run **Restart Kernel** and run the Section 2 cell again. |
| `401` or `Incorrect API key provided` | The key is wrong or has been revoked. | Create a new key on the OpenAI API keys page. Update `.env`, then **Restart Kernel** and run Section 2 again. |
| Jaeger UI is not reachable | Docker Desktop is closed, or the Jaeger container is not running. | Open Docker Desktop, wait for Engine running, then run `docker compose up -d`. |
| `Failed to export traces` warnings | Jaeger is not running, so traces cannot be sent. | Start Jaeger (Step 5) and run the Section 8 cell again. Each question takes a few extra seconds while Jaeger is down. |
| Jaeger shows no `module10-rag-app` service | Section 8 has not run yet, or the Lookback period is too short. | Run the Section 8 cell, then set Lookback to a longer period and click Find Traces. |
| `Overriding of current TracerProvider is not allowed` | The Section 2 cell was run twice in the same session. | This warning is harmless. Use **Restart Kernel** for a clean start. |
| `docker: command not found` or `Cannot connect to the Docker daemon` | Docker Desktop is not installed or not running. | Install Docker Desktop or start it, then open a new terminal. |
| Port 16686 or 4317 is already in use | Another program uses the same port. | Close that program, restart Docker Desktop, and run `docker compose up -d` again. |
| Model error such as `model not found` | Your account does not offer the model named in the notebook. | Follow **Optional: use a different AI model** above. |
| pip says it will change other packages | Packages from another course may conflict with this lab. | Press Ctrl+C and ask your instructor before continuing. |
| The notebook does not run | The notebook uses a different Python version. | Click **Select Kernel** and choose Python 3.10. |

## Glossary

| Term | Plain-English meaning |
| --- | --- |
| Trace | The complete record of one request. In this lab, one trace is one question and its answer. |
| Span | One step inside a trace. Each span has a name, a start time, an end time and details. |
| Parent and child span | A parent is a bigger step. Its children are the smaller steps inside it. |
| Trace ID | A 32-character code that identifies one trace. Use it to find a trace in Jaeger. |
| Span ID | A 16-character code that identifies one span inside a trace. |
| Tag (attribute) | A detail attached to a span, such as the number of documents found. |
| Span status | Shows whether a span finished normally or ended with an error. |
| OpenTelemetry | A free, open-standard toolkit that creates spans and sends them to a tracing tool. |
| OTLP | The standard format and port that OpenTelemetry uses to send traces to Jaeger. |
| Jaeger | A free, open-source tool that stores traces and shows them as timelines in a web browser. |
| RAG | Retrieval-Augmented Generation. The assistant first finds relevant documents, then answers using them. |
| LLM | Large Language Model. The AI model that writes the answer. |
| Token | A small piece of text that the AI model reads or writes. Usage is often measured in tokens. |
| Docker Compose | A tool that starts one or more programs, such as Jaeger, from a configuration file. |
| Kernel | The Python engine that runs the notebook cells in VS Code. |
| .env file | A private file that stores settings such as your API key. |

## Project files

| File | What it is for |
| --- | --- |
| module10_lab1_observability.ipynb | The lab notebook. Run its cells in order. |
| requirements.txt | The exact package versions to install with pip. |
| docker-compose.yml | Starts Jaeger with the `docker compose up -d` command. |
| .env.example | A template. Copy it to `.env` and add your API key. |
| .gitignore | Keeps the `.env` file out of version control. |
| README.md | A short setup guide for the project folder. |

### Safety reminders

- Keep your `.env` file and API key private.
- Use only the fictional data in this lab.
- Trace data stores IDs, counts, timings and model names. It does not store questions, prompts or answers.
