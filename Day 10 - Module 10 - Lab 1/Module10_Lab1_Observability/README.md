# Module 10 – Lab 1: Implement Observability and Tracing for a RAG Application

Learn how to watch a Generative AI application work. You will run a small RAG assistant, record every step with **OpenTelemetry**, and read the traces in the **Jaeger** web interface.

## Objectives

By the end of the lab you can:
- Start Jaeger with Docker Compose and open its web interface.
- Run a simple RAG assistant from a Jupyter notebook.
- Create a trace for each question, with one span per RAG step.
- Read parent and child spans, and find which step is slow.
- Find an error in a trace and identify the step that caused it.

## Prerequisites

- Windows with **VS Code** and the **Jupyter** extension.
- **Python 3.10**, the interpreter already used by your training workspace.
- **Docker Desktop**, installed and running.
- An **OpenAI API key**.

## Project files

| File | What it is for |
|---|---|
| `module10_lab1_observability.ipynb` | The lab. Run its cells in order. |
| `requirements.txt` | Exact package versions to install. |
| `docker-compose.yml` | Starts Jaeger (trace viewer) on your computer. |
| `.env.example` | Template for your private `.env` file. |
| `.gitignore` | Keeps `.env` and generated files out of version control. |
| `README.md` | This guide. |

## Step 1 – Use the existing Python interpreter

Do **not** install another Python or create a virtual environment. In VS Code, select the Python 3.10 interpreter you already have. To check it, run `python --version` in a terminal. It should print `Python 3.10.x`.

## Step 2 – Install the packages

Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements.txt
```

The file pins exact versions that already work together. If pip reports that it will change packages used by other courses, stop and ask your instructor first.

## Step 3 – Add your API key

1. Copy `.env.example` to a new file named `.env` in the same folder.
2. Open `.env` and replace the placeholder with your key:
   `OPENAI_API_KEY=` followed by your key.
3. Save the file.

Keep `.env` private. Never paste your key into the notebook, email it, or upload it.

## Step 4 – Start Jaeger

1. Open **Docker Desktop** and wait until it shows that the engine is running.
2. In a terminal in this project folder, run:

   ```bash
   docker compose up -d
   ```

3. Open **http://localhost:16686** in your browser. You should see the Jaeger page.

The notebook sends traces to port **4317**. You view them at port **16686**.

## Step 5 – Run the notebook

1. Open `module10_lab1_observability.ipynb` in VS Code.
2. Select the Python 3.10 kernel (top right of the notebook).
3. Run the cells from top to bottom. Sections 2–8 create traces. Section 10 creates a deliberate error.

## Step 6 – View the traces in Jaeger

1. Refresh the Jaeger page.
2. Select **Service:** `module10-rag-app`, then **Operation:** `RAG Application`, then click **Find Traces**.
3. Open a trace to see the parent and child spans.
4. To find a specific question, paste its Trace ID (printed by the notebook) into **Lookup by Trace ID**.

Section 9 of the notebook has the full guided walkthrough.

## Step 7 – Stop Jaeger

```bash
docker compose down
```

Jaeger keeps traces in memory only. Stopping it removes them, so view your traces before you stop Jaeger.

## Troubleshooting

| Problem | What to do |
|---|---|
| `OPENAI_API_KEY was not found` | Check that the file is named exactly `.env` (not `.env.txt`), that it is in the project folder, and that the key follows `OPENAI_API_KEY=`. |
| `401` / *Incorrect API key provided* | The key is wrong or was revoked. Create a new key on the OpenAI API keys page and update `.env`. |
| `Jaeger UI is NOT reachable` | Open Docker Desktop, wait for it to start, then run `docker compose up -d`. |
| Notebook shows `Failed to export` warnings | Jaeger is not running. Each question then waits a few extra seconds before it finishes. Start Jaeger (Step 4) and run the cell again. |
| Jaeger shows no traces | Run the Section 8 cell again, then click **Find Traces**. Confirm that the Service is `module10-rag-app`. |
| `Overriding of current TracerProvider is not allowed` | Harmless. It appears when the setup cell runs twice. Use *Restart Kernel* for a clean start. |
| `docker: command not found` | Docker Desktop is not installed or not running. Install it, then open a new terminal. |
| Port 16686 or 4317 already in use | Close the other program that uses that port, then run `docker compose up -d` again. |
| Model error such as `model not found` | Your account may not offer the model. Change `MODEL_NAME` in the Section 5 cell to a chat model your account can use. |
