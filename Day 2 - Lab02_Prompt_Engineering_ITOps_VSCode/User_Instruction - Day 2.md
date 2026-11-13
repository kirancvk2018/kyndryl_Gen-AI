# Day 2 Lab: Prompt Engineering for Everyday Operations

*Step-by-step instructions for participants*

Written for: workshop participants with no IT infrastructure background. Follow the steps in order. Each step tells you what to do and what you should see.

## What you need before you start

| Item | Details |
| --- | --- |
| Computer | Windows 10 or 11 with an internet connection |
| Lab folder | Folder named Lab02_Prompt_Engineering_ITOps_VSCode, provided by the trainer |
| API key | An OpenAI API key from your trainer. Keep it private. |
| Software | Python 3.10 or newer, and VS Code (Visual Studio Code) |
| Time | About 90 minutes for the full lab |

## Section 1: Install or reinstall Python

Why: Python runs the lab code. Your Python was reinstalled, so check it first and reinstall if needed.

### Step 1.1: Check whether Python is installed

1. Click Start, type PowerShell, and press Enter.
2. Type the following command and press Enter:

   ```
   python --version
   ```

3. Check the result. If it shows Python 3.10 or higher, skip to Step 1.5 (pip check).
4. If it says 'python' is not recognized, go to Step 1.2.

### Step 1.2: Download Python

1. Open a web browser and go to https://www.python.org/downloads/
2. Click the yellow 'Download Python' button. The file is a Windows installer.

### Step 1.3: Install Python (important setting)

1. Double-click the downloaded installer.
2. On the first screen, tick the box 'Add python.exe to PATH' at the bottom. Do not skip this.
3. Click 'Install Now' and wait for it to finish.
4. Click 'Close' when the installer says setup was successful.

### Step 1.4: Restart PowerShell and confirm the version

1. Close any open PowerShell or VS Code windows, then open PowerShell again.
2. Type `python --version` and press Enter. You should see Python 3.10 or higher.

### Step 1.5: Confirm pip is available

What is pip? pip is the tool that installs Python libraries. It comes with Python.

1. In PowerShell, type the following and press Enter:

   ```
   python -m pip --version
   ```

2. You should see a line that starts with 'pip'. If you see an error, repeat Step 1.3 and tick 'Add python.exe to PATH'.

## Section 2: Open the lab folder in VS Code

### Step 2.1: Open the folder

1. Open VS Code.
2. Click File, then Open Folder.
3. Select the folder Lab02_Prompt_Engineering_ITOps_VSCode and click Select Folder.

### Step 2.2: Check the files are there

1. In the left panel (Explorer), confirm you can see these items:

| File or folder | What it is |
| --- | --- |
| .env.example | Template for your private key file (Section 3) |
| requirements.txt | List of Python libraries to install (Section 4) |
| prompt_engineering_lab.py | Short test script (Section 5) |
| Day 2 - Lab2_PromptEngineering_GeneralOperations.ipynb | Main lab notebook (Section 6) |
| Lab02_Prompt_Engineering_ITOps_Detailed.ipynb | Optional: nine prompt styles (Section 7) |
| Day 2 - Lab 1 (folder) | Optional: batch incident summarizer (Section 7) |
| data (folder) | Sample CSV files used by the lab |

If files are missing: Ask your trainer for a fresh copy of the lab folder.

## Section 3: Create your private .env file

Why: The lab reads your API key from a file called .env. The key stays on your computer and is never typed into a notebook.

### Step 3.1: Make a copy of the template

1. In VS Code's Explorer, right-click .env.example and choose Copy, then Paste.
2. Rename the copy to exactly:

   ```
   .env
   ```

3. If Windows will not let you name a file starting with a dot, use File Explorer, then View, then tick 'File name extensions', and try again.

### Step 3.2: Paste your key

1. Open the .env file in VS Code.
2. Replace the text your_api_key_here with the key your trainer gave you. The line should look like this:

   ```
   OPENAI_API_KEY=sk-...your key...
   ```

3. Check there are no spaces around the = sign and no quote marks.
4. Save the file with Ctrl+S.

### Step 3.3: Keep the key private

- Do not paste the key into any notebook, chat, email or screenshot.
- Do not share the .env file with anyone.
- If you think the key was shared, tell your trainer straight away so the key can be replaced.

## Section 4: Install the Python libraries

### Step 4.1: Open PowerShell in the lab folder

1. In VS Code, click Terminal, then New Terminal. A terminal opens at the bottom.
2. Check the terminal's location ends with Lab02_Prompt_Engineering_ITOps_VSCode. If not, type the following, replacing the path with the one on your computer:

   ```
   cd "C:\path\to\Lab02_Prompt_Engineering_ITOps_VSCode"
   ```

### Step 4.2: Install the libraries

1. Type the following and press Enter:

   ```
   python -m pip install -r requirements.txt
   ```

2. Wait until the text stops scrolling. You should see 'Successfully installed' near the end.

Libraries installed: openai (connects to the AI model), python-dotenv (reads your .env file), pandas (reads the CSV data).

### Step 4.3: Install Jupyter (only if you will run notebooks in a browser)

Skip this step if you run the notebook inside VS Code with the Python and Jupyter extensions installed.

1. Type the following and press Enter:

   ```
   python -m pip install jupyter
   ```

## Section 5: Test your setup

### Step 5.1: Run the test script

1. In the terminal, type the following and press Enter:

   ```
   python prompt_engineering_lab.py
   ```

2. Wait about 10 to 20 seconds.

### Step 5.2: Check the result

1. You should see a short report with three parts: Incident Summary, Probable Root Cause, and Recommended Next Actions.
2. If you see this, your key and libraries work. Go to Section 6.
3. If you see an error, go to Section 8 and find the matching problem.

## Section 6: Run the main lab notebook

About the notebook: Day 2 - Lab2_PromptEngineering_GeneralOperations.ipynb contains text, code cells and exercises. You run one cell at a time, from top to bottom.

### Step 6.1: Open the notebook and choose a Python kernel

1. In VS Code, click the file Day 2 - Lab2_PromptEngineering_GeneralOperations.ipynb.
2. At the top-right, click Select Kernel. Choose the Python version you installed in Section 1.
3. A kernel is the engine that runs the code in the notebook.

### Step 6.2: Install the notebook's package (first cell)

1. Click the first code cell, then click the play button (triangle) at the left of the cell.
2. Wait until the cell shows a number in square brackets, for example [1], and no error.

### Step 6.3: Run the setup cell

1. Click the setup cell (it imports libraries and defines the ask function) and press the play button.
2. You should see the message: Ready. Use ask("your prompt") to send a prompt.

Tip: If you see 'OPENAI_API_KEY is not set', go back to Section 3, save .env, then restart the kernel (Kernel, then Restart) and run the setup cell again.

### Step 6.4: Section 2, What makes a good prompt

1. Run the cell that defines the complaint. Read the customer complaint printed below it.

### Step 6.5: Section 3, Basic vs. improved prompt

1. Run the basic prompt cell. Read the answer.
2. Run the improved prompt cell. Read the answer.
3. Write one sentence: which answer would you act on, and why?

### Step 6.6: Section 4, Role

1. Run the role prompt cell.
2. Change the first line to a different role, for example: 'a delivery operations manager at a regional warehouse'. Run the cell again.
3. Compare the two answers.

### Step 6.7: Section 5, Asking for a table

1. Run the table prompt cell. Check the answer is a table with Owner, Action and Due date columns.

### Step 6.8: Section 6, Learning from examples

1. Run the few-shot cell. The model should choose a category and priority for the new request.
2. Change the new_request text to a different request, such as a delivery that arrived damaged. Run the cell again.

### Step 6.9: Section 7, Exercises 1 to 3

1. Exercise 1: find the line that says TODO, write your prompt, and run the cell. Use a role, a task and a five-line format.
2. Exercise 2: add two examples where the TODO is, then run the cell.
3. Exercise 3: write a basic prompt and an improved prompt for a task from your own work. Run both and write one sentence about what changed.

If a cell still says TODO: the exercise is not finished. The model will reply asking what TODO means. Replace TODO with your text.

### Step 6.10: Section 8, Quick check and save

1. Answer the four questions in your own words. The instructor section below each question shows the answers.
2. Save the notebook with Ctrl+S.

## Section 7: Optional notebooks

Note: These are kept from the original lab. Your trainer will say whether to run them.

### Step 7.1: Prompt style tour (Lab02_Prompt_Engineering_ITOps_Detailed.ipynb)

- Runs nine prompt styles on the same incident: basic, role, goal, context, structured, executive tone, zero-shot, few-shot and JSON.
- Uses the model gpt-4.1-mini. Run the setup cell first, as in Section 6.

### Step 7.2: Batch incident summarizer (folder Day 2 - Lab 1)

- Open Lab02_GenAI_Incident_Summarization_COMPLETE.ipynb. It reads your .env file automatically.
- It loads the file sample_incidents_10000.csv from the folder you run it from. Either run it from the data folder, or copy the CSV next to the notebook.
- It writes incident_summaries_output.csv and incident_summaries_output.json next to the notebook.
- The examples are IT-focused, so the trainer may skip this step.

### Step 7.3: Do not use the archived notebook

- Old_Day 2 - Lab2_PromptEngineering_ITOperations.ipynb is archived. It uses a model that the current API key cannot access. Do not run it.

## Section 8: Troubleshooting

| What you see | What to do |
| --- | --- |
| 'python' is not recognized | Reinstall Python (Section 1) and tick 'Add python.exe to PATH'. Then close and reopen VS Code and the terminal. |
| pip install fails with a permission error | Run: `python -m pip install --user -r requirements.txt` |
| WARNING: OPENAI_API_KEY is not set | Check the file is named exactly .env, is in the lab folder, and the line reads OPENAI_API_KEY=... Save it, then restart the kernel and run the cell again. |
| 401 error or 'Incorrect API key' | The key is wrong or was copied with extra characters. Copy the key again from your trainer. |
| 404 error: model does not exist | Tell your trainer. The model name may be unavailable for your key. |
| 429 error: rate limit | Wait one minute and run the cell again. |
| FileNotFoundError for a data file | Run the script from the lab folder. For the Lab 1 notebook, see Step 7.2. |
| Notebook shows 'TODO' replies | The exercise is not finished. Replace TODO with your own text (Step 6.9). |
| Notebook cell is stuck or will not run | Kernel, then Restart, then run the setup cell again from the top. |

## Flow chart: the whole lab at a glance

Follow the boxes from START to END. If the test in Step 5 fails, fix the problem in Section 8 and run Step 5 again.

![Flow chart: the whole lab at a glance](User_Instruction%20-%20Day%202_files/image1.png)
