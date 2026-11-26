# Module 9 – Lab 1 User Guide

GenAI Application Evaluation using MLflow and LLM-as-a-Judge

This guide takes you through the lab one step at a time. You will set up the project, run the notebook from top to bottom, and learn how to read the results. **You do not need to write any code.** Each step tells you what to do and what you should see.

> **How to use this guide**
>
> Work through the parts in order. Tick off each step in the checklist at the end.
>
> Each step says **Expected** when you should see something specific on screen.

## Contents

- Part A – Before you start
- Part B – Set up the lab (one time)
- Part C – Run the notebook
- Part D – Understand the results
- Part E – Troubleshooting
- Part F – Good practice and cost
- Checklist

## Part A – Before you start

### What you need

| You need | Why | How to check |
| --- | --- | --- |
| Python 3.10 | Runs the lab's code. | Type `python --version` in a terminal. You should see `Python 3.10.x`. |
| An OpenAI account with an API key and billing turned on | The lab sends requests to OpenAI to generate and judge answers. | Log in at platform.openai.com and check that you can create an API key. |
| VS Code with the Jupyter extension, or JupyterLab | Opens and runs the notebook. | VS Code: open the Extensions panel and check that Jupyter is installed. |
| The lab folder | Contains the notebook and the setup files. | You should see the five files listed below. |

### Key words

You will see these words in the notebook. Come back to this table whenever a term is unclear.

| Word | Plain-English meaning |
| --- | --- |
| **GenAI application** | A program that writes answers using a language model. In this lab it is a single function. |
| **LLM** | Large language model. The AI that writes text, such as the OpenAI model used here. |
| **LLM-as-a-Judge** | A language model that grades another model's answer against a rule. |
| **Evaluation dataset** | The fixed list of test questions the application answers. |
| **Scorer** (or judge) | A ready-made MLflow check that grades an answer for one quality, such as relevance. |
| **Verdict** | The result of a check: `yes` or `no`. |
| **Rationale** | The short reason the judge gives for its verdict. |
| **MLflow** | A tool that records each evaluation so you can look at it later. |
| **Experiment** and **run** | An experiment is a folder in MLflow. Each evaluation you run is one run inside it. |
| **Kernel** | The engine that runs the notebook's code. Restart it after you change the `.env` file. |
| **Cell** | One block in the notebook. Text cells explain. Code cells do the work when you run them. |
| **API key** | A secret password that lets the lab use your OpenAI account. Keep it private. |
| **Terminal** | A window where you type commands. In VS Code: Terminal → New Terminal. |

### What is in the lab folder

| File | What it does | Do you edit it? |
| --- | --- | --- |
| `module9_lab1_genai_evaluation.ipynb` | The notebook. You run its cells in order. | No. You only run it. |
| `requirements.txt` | Lists the software packages the lab needs. | No. |
| `README.md` | A short written reference for the lab. | No. |
| `.env.example` | A template for your settings file. | Copy it to `.env`. Do not put your key in this file. |
| `.gitignore` | Tells Git which files to keep private. | No. |

> **Do the setup once**
>
> Part B is done once per computer. After that, go straight to Part C each time you run the lab.

## Part B – Set up the lab (one time)

### Step 1 – Check your Python version

- Open a terminal. In VS Code, choose **Terminal → New Terminal**. On Windows without VS Code, press the Windows key, type `cmd` and open **Command Prompt**.
- Type the command below and press Enter.

```text
python --version
```

**Expected:** a line such as `Python 3.10.11`. If you see a different version, install Python 3.10 from python.org before you continue.

### Step 2 – Open a terminal inside the lab folder

- **In VS Code:** choose **File → Open Folder**, select the folder **Module 9 - Lab 1**, then choose **Terminal → New Terminal**. The terminal starts in that folder.
- **Without VS Code (Windows):** open the lab folder in File Explorer, click the address bar, type `cmd` and press Enter.

**Expected:** the terminal is inside the lab folder. Type `dir` (Windows) or `ls -A` (Mac/Linux) and you should see the five files listed in Part A.

### Step 3 – Install the packages

- In the terminal, type the command below and press Enter.

```text
pip install -r requirements.txt
```

Wait until the command finishes. This can take a few minutes. **Expected:** a final line that starts with `Successfully installed`. If the packages are already on your computer, you will see `Requirement already satisfied` lines instead. Both are fine.

### Step 4 – Create your settings file (.env)

The notebook reads your key from a file called `.env`. You make it by copying the template.

- **Windows (File Explorer):** right-click `.env.example`, choose **Copy**. Right-click an empty space in the folder and choose **Paste**. Right-click the new copy, choose **Rename** and type `.env`.
- **Mac or Linux (terminal):** type `cp .env.example .env` and press Enter.

**Expected:** a file named exactly `.env` appears in the lab folder. Make sure it is not called `.env.txt`.

### Step 5 – Add your OpenAI API key

- Open `.env` in VS Code, or in Notepad on Windows.
- Find the line that starts with `OPENAI_API_KEY=`. Replace everything after the equals sign with **your own key**. Do not add spaces or quotation marks.
- Leave the line `OPENAI_MODEL=gpt-4.1-mini` as it is. It is a low-cost model.
- Save the file (Ctrl + S).

> **Warning – keep your key private**
>
> Never paste your key into the notebook, into an email or into `.env.example`.
>
> The `.gitignore` file stops `.env` from being saved to Git.
>
> If you think someone else has seen your key, delete it on the OpenAI website and create a new one.

## Part C – Run the notebook

### Step 6 – Open the notebook and select the kernel

- Click `module9_lab1_genai_evaluation.ipynb` to open it.
- In VS Code, click **Select Kernel** in the top-right corner and choose the **Python 3.10** environment you used in Step 3. In JupyterLab, check that the kernel shown at the top right is a Python 3.10 kernel.

**Expected:** the notebook opens with the title **Module 9 – Lab 1: GenAI Application Evaluation using MLflow and LLM-as-a-Judge** at the top.

### Step 7 – Read the first section before you run anything

Read the introduction and the **How to run this notebook** note. The most important rules are: run the cells **in order**, do not skip cells, and restart the kernel (**Kernel → Restart**) if you change `.env`.

> **How to run a cell**
>
> Click anywhere inside a code cell (the grey box with code in it). Press **Shift + Enter** to run it. The cell's result appears just below it. While a cell is still working, it is marked as busy until it finishes.

### Step 8 – Run the setup cell (Section 3)

Find the code cell under the heading **Section 3 – Environment setup** and run it.

**Expected:** three lines: `Setup complete.`, `Model: gpt-4.1-mini` and `MLflow experiment: Module9_GenAI_Evaluation`.

> **If you see an error**
>
> If the cell stops with `AssertionError: SETUP NEEDED`, your `.env` file is missing or still has the placeholder key. Go back to Steps 4 and 5, save `.env`, restart the kernel and run the notebook again from the first cell.

### Step 9 – Try the GenAI application (Section 4)

Run the code cell under **Section 4 – A simple GenAI application**.

**Expected:** two short answers, one about machine learning and one about load balancers. Your wording will differ from the examples and from run to run. That is normal.

### Step 10 – Generate answers for the test questions (Sections 5 and 6)

Run the code cell under **Section 6 – Generate responses for the dataset**. It asks the model six IT Operations questions, one at a time, so it takes a short while.

**Expected:** a table with two columns, **question** and **response**, and six rows. The questions are about server CPU use, database backups, network latency, incident management, monitoring and server outages.

### Step 11 – Create the three judges (Section 7)

Run the code cell under **Section 7 – MLflow built-in scorers and LLM judges**. This cell only sets things up. It does not call the API.

**Expected:** `Judges ready: relevance_to_query | coherence | safety`.

### Step 12 – Test relevance (Section 8)

Run the code cell under **Section 8 – Evaluate relevance**. It judges two answers to the question “What is machine learning?”: one on topic and one about pizza.

**Expected:** the on-topic answer gets `yes` and the pizza answer gets `no`. Each line is followed by a reason.

### Step 13 – Test coherence (Section 9)

Run the code cell under **Section 9 – Evaluate coherence**. It judges a clear answer and a deliberately contradictory answer.

**Expected:** the clear answer gets `yes` and the contradictory answer gets `no`.

### Step 14 – Test safety (Section 10)

Run the code cell under **Section 10 – Evaluate safety**. It judges a normal answer and an insulting answer.

**Expected:** the normal answer gets `yes` and the insulting answer gets `no`.

### Step 15 – Run the full evaluation (Section 11)

Run the code cell under **Section 11 – Combined evaluation with LLM-as-a-Judge**. It sends all six test answers to all three judges. That is 18 judge checks, so wait until the cell finishes. A progress bar labelled **Evaluating** appears while it works.

**Expected:** a line that says `Evaluation finished. MLflow run ID:` followed by a long code made of letters and numbers.

### Step 16 – Read the results tables (Section 12)

Run the code cell under **Section 12 – Review the evaluation results**.

**Expected:** two tables. The first shows the verdicts (`yes` or `no`) for each question. The second shows the reason behind each verdict. Part D explains how to read them.

### Step 17 – Optional – open the MLflow web page (Section 13)

- In a terminal inside the lab folder, type the command below and press Enter.

```text
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

- If `mlflow` is not recognised, use this command instead: `python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000`.
- Open **http://127.0.0.1:5000** in your web browser.
- Click the experiment **Module9_GenAI_Evaluation**, then open the newest run. Open the **Traces** tab on the run page to see the verdict and reason for each question.
- When you have finished, go back to the terminal and press **Ctrl + C** to stop the MLflow page.

**Expected:** a web page listing the experiment and its runs. The page is optional, so you can skip this step.

### Step 18 – Do the practical exercise (Section 14)

- In the exercise cell, find the line that starts with `my_question =`. Change the question inside the quotation marks to an IT Operations question you care about.
- Run the cell.
- Read the answer and the three verdicts.
- Decide which verdict is weakest. If one of them is `no`, that dimension needs improvement.

**Expected:** the answer is printed, followed by a small table with three verdicts: relevance, coherence and safety. In our test run, the question about checking disk space got `yes` on all three.

> **Try an improvement**
>
> Scroll up to the cell under **Section 4**. Change the text of `SYSTEM_PROMPT`, for example to ask for plain words. Run that cell again, then run the exercise cell again and compare the verdicts. Each run calls the API, so keep the number of runs small.

### Step 19 – Check your understanding (Section 15)

Answer the five multiple-choice questions under **Section 15 – Knowledge check**. The answers are in the next section of the notebook, titled **Answers**. Compare your choices with them.

## Part D – Understand the results

### The three verdicts

| Dimension | Column in the results table | Verdict | What it means | If the verdict is no |
| --- | --- | --- | --- | --- |
| Relevance | relevance_to_query/value | `yes` or `no` | Yes: the answer addresses the question that was asked. | The answer is off-topic or does not answer the question. |
| Coherence | coherence/value | `yes` or `no` | Yes: the answer is clear, logically organised and consistent. | The answer is confusing, contradictory or hard to follow. |
| Safety | safety/value | `yes` or `no` | Yes: the answer is free from harmful, abusive or inappropriate content. | The answer contains content that could be harmful or abusive. |

### How to read the reason

- Each verdict has a **rationale**. It is the judge's short explanation in plain English.
- Read the reason before you decide what to change. It tells you **why** the answer passed or failed.
- Judges are usually right, but not always. If a reason does not make sense to you, check the answer yourself.

### A worked example

The notebook judges two answers to the question “What is machine learning?”.

| Answer | Relevance | What the reason says |
| --- | --- | --- |
| “Machine learning enables systems to learn patterns from data and make predictions.” | `yes` | The answer describes machine learning, so it addresses the question. |
| “Pizza is a popular food that is often topped with cheese and tomato sauce.” | `no` | The answer is about pizza, which has nothing to do with machine learning. |

**What to do with a no:** the answer has the wrong topic. Improve the instructions to the model, then evaluate again and compare the verdicts.

### What is normal

- The wording of answers changes from run to run, and judges can vary a little. Two runs may not give identical results.
- In our test run, all six sample answers in Section 11 got `yes` on all three checks. Your results may be a little different.
- Focus on the **reasons**. If a verdict is `no`, read the reason and decide whether it is right.

## Part E – Troubleshooting

Find what you see in the first column. Then try the fix in the second column.

| What you see | What to do |
| --- | --- |
| `AssertionError: SETUP NEEDED: copy .env.example to .env …` | The `.env` file is missing or still has the placeholder key. Make sure `.env` is in the same folder as the notebook. Replace the key (Step 5), save, restart the kernel and run from the first cell. |
| `AuthenticationError` or `Error code: 401` or `Incorrect API key provided` | The key is wrong, has been deleted, or has extra spaces or quotation marks. Copy a key again from the OpenAI website into `.env`, save, restart the kernel and run again. |
| `model_not_found`, or a message that the model does not exist | Your account cannot use the model in `OPENAI_MODEL`. Change the value to a model you can use, save, restart the kernel and run again. |
| `MlflowException: OPENAI_API_KEY environment variable must be set` | The notebook did not load your key. Save `.env`, restart the kernel (**Kernel → Restart**) and run from the first cell. |
| `NameError: name 'client' is not defined`, or other errors in cells after the setup cell | The setup cell failed, so later cells cannot run. Fix the setup problem above, restart the kernel and run from the first cell. |
| `ModuleNotFoundError: No module named …` | A package is missing. In the terminal, run `pip install -r requirements.txt` in the lab folder. Restart the kernel and run again. |
| `429` or a message about rate limits or quota | OpenAI is limiting requests or your account has no credit. Wait a minute and try again. If it continues, check billing on the OpenAI website. |
| The notebook says it cannot find the key, but `.env` exists | Make sure `.env` is in the **same folder** as the notebook. Open the notebook from that folder, then restart the kernel. |
| A cell keeps running for a long time | Evaluation makes many calls to the API. Wait for the cell to finish. Do not run the next cell until it has. |
| `mlflow` is not recognised, or the MLflow page does not open | Use `python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000` instead. If port 5000 is busy, use `--port 5001` and open http://127.0.0.1:5001. |

## Part F – Good practice and cost

- **Cost:** running the lab calls the OpenAI API, so it may cost a small amount each time. The lab uses only six test questions to keep costs low. The practical exercise and every full run add more calls.
- **Restart after changing settings:** if you change `.env`, restart the kernel before you run the notebook again. Otherwise the notebook keeps the old values.
- **Run from the top:** when you change a setting or a function, run the notebook again from the first cell so every later cell uses the new value.
- **Keep files together:** keep `.env` and the notebook in the same folder.
- **Keep your key private:** do not share `.env`, do not paste your key into the notebook, and do not send it to anyone.
- **MLflow records:** each run is saved in the file `mlflow.db` in the lab folder. Keep this file if you want to look at your runs later.

## Checklist

Tick each box when you have finished the step.

- [ ] Python 3.10 is installed (Step 1).
- [ ] The terminal is open inside the lab folder (Step 2).
- [ ] `pip install -r requirements.txt` finished without errors (Step 3).
- [ ] `.env` exists and contains my own key (Steps 4 and 5).
- [ ] The notebook is open and the kernel is set to Python 3.10 (Step 6).
- [ ] The setup cell shows `Setup complete.` (Step 8).
- [ ] The answers, relevance, coherence and safety cells all ran (Steps 9 to 14).
- [ ] The full evaluation finished and I read both results tables (Steps 15 and 16).
- [ ] I did the practical exercise and identified one dimension to improve (Step 18).
