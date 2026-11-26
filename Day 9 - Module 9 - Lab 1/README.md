# Module 9 – Lab 1: GenAI Application Evaluation using MLflow and LLM-as-a-Judge

## Purpose

Learn how to check the quality of GenAI answers. You will generate answers from a small GenAI application, then use MLflow and an LLM judge to test three things: **relevance**, **coherence** and **safety**.

## Learning objectives

By the end of the lab you should be able to:

1. Explain why GenAI applications need evaluation.
2. Explain what LLM-as-a-Judge means.
3. Generate responses from a simple GenAI application.
4. Evaluate relevance, coherence and safety.
5. Use MLflow built-in evaluation scorers.
6. Review evaluation verdicts and reasons.
7. Explain how evaluation results help improve a GenAI application.

## Prerequisites

- Python 3.10 (the lab was checked with Python 3.10.11).
- An OpenAI account with an API key and billing set up.
- VS Code with the Jupyter extension, or JupyterLab.

> **Cost note:** the lab calls the OpenAI API. Running it may incur small charges.

## Files in this folder

| File | Purpose |
|---|---|
| `module9_lab1_genai_evaluation.ipynb` | The lab notebook. This is the only file you run. |
| `requirements.txt` | The Python packages the lab needs. |
| `.env.example` | Template for your settings file. |
| `.gitignore` | Stops secrets and MLflow data from being committed to Git. |

## 1. Install the packages

Open a terminal in this folder and run:

```
pip install -r requirements.txt
```

## 2. Add your OpenAI API key

1. Copy `.env.example` and rename the copy to `.env`.
   - Windows: copy the file in File Explorer, then rename the copy to `.env`.
   - Mac or Linux: `cp .env.example .env`
2. Open `.env` and replace `your_openai_api_key` with your key.
3. Keep `OPENAI_MODEL=gpt-4.1-mini`, a low-cost model. You can change it to another OpenAI chat model your account can use.

Never share your `.env` file or paste your key into the notebook.

## 3. Open the notebook

- **VS Code:** open this folder, then open `module9_lab1_genai_evaluation.ipynb`. Select the Python 3.10 interpreter as the kernel.
- **Jupyter:** run `jupyter notebook` in this folder, then open the notebook.

## 4. Run the notebook from top to bottom

Run the cells in order (use **Run All**, or click a cell and press **Shift + Enter**). The notebook creates a local MLflow database file, `mlflow.db`, in this folder. You do not need to start any server.

## 5. How to read the results

| Dimension | Verdict you will see | What it means |
|---|---|---|
| Relevance | `yes` / `no` | `yes`: the answer addresses the question. |
| Coherence | `yes` / `no` | `yes`: the answer is clear, logical and consistent. |
| Safety | `yes` / `no` | `yes`: the answer is free from harmful or abusive content. |

Each verdict has a **rationale**, which is the judge's short reason. Read it before deciding what to improve. A `no` shows which dimension needs work.

## 6. Open the MLflow UI (optional)

In a terminal in this folder, run:

```
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open http://127.0.0.1:5000 in your browser. Press **Ctrl + C** in the terminal to stop it.

## 7. Basic troubleshooting

| Problem | What to do |
|---|---|
| The cell shows `SETUP NEEDED` | `.env` is missing, or the key is still the placeholder. Fix `.env`, restart the kernel (**Kernel → Restart**) and run again. |
| `401` or `AuthenticationError` | The API key is wrong or has been revoked. Check the key in `.env`. |
| `model_not_found` or similar | Your account cannot use the model in `OPENAI_MODEL`. Change it to a model you can use, then restart the kernel. |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` using the same Python that the notebook kernel uses. |
| The notebook cannot find your key | Keep `.env` in the same folder as the notebook, and open the notebook from that folder. |
| A cell is slow | Evaluation makes many API calls. Wait for the cell to finish before running the next one. |

Built with MLflow 3.15.1 and the OpenAI Python package 2.54.0.
