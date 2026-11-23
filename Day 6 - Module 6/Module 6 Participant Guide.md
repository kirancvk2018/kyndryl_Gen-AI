# Module 6 Participant Guide: LangChain Labs

This guide walks you through every part of Module 6\. You will set up each lab on your computer, run the notebooks, and try the scripts. You do not need any programming experience. Follow the steps in order.

---

## Part 1: Before You Start

### What you need

- A Windows computer connected to the internet.  
- The project folder **Day 6 \- Module 6**, with all its lab folders inside it.  
- An **OpenAI API key**. This is a private password that lets the labs talk to the AI model. Your facilitator will tell you whether to create your own key or use one provided for the session (see Part 2).  
- Microsoft Word, to open this guide and the Word version of it.

### Important rules

- **Do not move, rename or delete** the lab folders or the files inside them. The labs depend on the exact file names.  
- **Keep your API key private.** Do not paste it into emails, chats, screenshots or shared documents.  
- **Use sample data only.** Do not type real names of customers, employees or real financial records into the labs.  
- Each lab uses about a few cents of AI usage. Running a notebook more times costs a little more.

### Words you will see

| Word | What it means |
| :---- | :---- |
| **Folder** | A container for files, like a drawer. |
| **Terminal** | A window where you type short commands. This guide uses **PowerShell**, which is built into Windows. |
| **Virtual environment** | A private toolbox for one lab. It is a folder named `.venv` that sits inside the lab folder. It keeps the lab's tools separate from everything else on your computer. |
| **Notebook** | A web page where you run code in small blocks called **cells**. The file name ends in `.ipynb`. |
| **Cell** | One block of code or text inside a notebook. |
| **.env file** | A small settings file that holds your API key and a few settings. |
| **API key** | The private password that connects the labs to the AI model. |

---

## Part 2: Get Your API Key

Skip this part if your facilitator has given you a key for the session.

1. Open a web browser and go to **platform.openai.com**.  
2. Sign in or create an account.  
3. Click your profile picture, then choose **API keys**.  
4. Click **Create new secret key**. Give it a name such as "Module 6".  
5. **Copy the key right away** and save it somewhere safe. OpenAI only shows the full key once.  
6. Make sure your account has credit or billing set up. Without it, the labs will fail with an error about quota or payment.

---

## Part 3: Open a Terminal in a Lab Folder

You will do this at the start of every lab. The steps are the same for each lab. Only the folder changes.

1. Open **File Explorer** and go to the lab folder, for example **Module 6 \- Lab 1**.  
2. Click once in the **address bar** at the top of the window. The folder path becomes highlighted.  
3. Type **powershell** and press **Enter**.  
4. A blue or black window opens. Its title shows the lab folder path. Check that the path ends with the lab folder name, for example `...\Module 6 - Lab 1`.

**Tip:** Always create the virtual environment **inside the lab folder you are working in**, so the `.venv` folder sits next to the lab's files. Each lab gets its own `.venv`.

**Copy and paste:** To paste a command into PowerShell, right-click inside the window. Do not press Ctrl+V in PowerShell.

---

## Part 4: Lab 1, LangChain Basics

**What you will do:** Use AI to summarize a night-shift handover, sort helpdesk tickets into teams, and turn meeting notes into a status email. You will learn prompt templates, chains that pass one answer to the next step, and checking JSON output.

**Lab folder:** `Module 6 - Lab 1`

### Step 1: Remove the old toolbox (if one exists)

1. In the **Module 6 \- Lab 1** folder, look for a folder named **.venv**.  
2. If it exists, right-click it and choose **Delete**. Then empty the Recycle Bin.  
3. This is needed because an older toolbox in this folder was built for a different computer and will not work.

### Step 2: Open a terminal in the lab folder

Follow Part 3 and open PowerShell in **Module 6 \- Lab 1**.

### Step 3: Create the virtual environment

Type this command and press **Enter**:

```
python -m venv .venv
```

Wait about one minute. When the line you typed appears again, the toolbox is ready. A new folder named **.venv** will appear inside **Module 6 \- Lab 1**.

### Step 4: Install the lab tools

Type this command and press **Enter**. It can take several minutes. Wait until you see the cursor again:

```
.\.venv\Scripts\python.exe -m pip install -r lab1_m6_requirements.txt
```

Then install the notebook viewer:

```
.\.venv\Scripts\python.exe -m pip install jupyter
```

### Step 5: Add your API key

1. In the **Module 6 \- Lab 1** folder, right-click the file named **.env** and choose **Open with \> Notepad**.

2. Find the line that starts with `OPENAI_API_KEY=`.

3. Replace the placeholder text after the equals sign with your key. Keep it on the same line, with no spaces and no quotation marks. It should look like this:

```
OPENAI_API_KEY=sk-your-key-goes-here
```

4. Leave the other lines as they are. The line `OPENAI_MODEL=gpt-4o-mini` chooses the AI model for this lab.

5. Save the file (**Ctrl+S**) and close Notepad.

**Note:** If you cannot see the file name **.env**, open File Explorer, click **View**, and tick **File name extensions** and **Hidden items**.

### Step 6: Open the notebook

In the PowerShell window, type this and press **Enter**:

```
.\.venv\Scripts\jupyter.exe notebook module6_lab1_langchain_basics.ipynb
```

A web browser opens with the notebook. If it does not open, copy the link that appears in PowerShell (it starts with `http://localhost`) and paste it into your browser.

### Step 7: Run the notebook

1. Click inside the first cell.  
2. Press **Shift+Enter** to run it. The cell's output appears below it.  
3. Continue to the next cell and press **Shift+Enter** again.  
4. Run every cell from top to bottom. Do not skip cells.  
5. Section 3 makes your first AI call. Expect a short answer. Your answer may be different from the one shown in the notebook, because AI replies vary.  
6. Section 8 is your exercise. Change the instructions in the cell so the status email also has 3 bullet points and an owners-and-due-dates line. Then run the cell again.  
7. Section 11 creates a new folder named **output** and saves the ticket results to `output\ticket_triage.json`.

### Step 8: Stop the notebook

1. Return to the PowerShell window.  
2. Press **Ctrl+C**, then type **y** and press **Enter** when asked to confirm.

---

## Part 5: Lab 2, Sequential Chains

**What you will do:** Run a four-step chain where each step uses the result of the step before it. The steps are: summary, cause and blockers, business impact, and action plan. The lab uses five routine office requests, such as a supply restock, a building badge and a printer repair.

**Lab folder:** `Module 6 - Lab 2`

### Step 1: Open a terminal in the lab folder

Open **Module 6 \- Lab 2** and open PowerShell there, as in Part 3\.

### Step 2: Create the virtual environment

```
python -m venv .venv
```

### Step 3: Install the lab tools

```
.\.venv\Scripts\python.exe -m pip install -r requirements_module6_lab2.txt
```

This list includes Jupyter, so you do not need a separate install step.

### Step 4: Add your API key

1. Open the **.env** file in **Module 6 \- Lab 2** with Notepad.  
2. Replace the placeholder after `OPENAI_API_KEY=` with your key, on the same line.  
3. Save and close.

### Step 5: Run the corporate operations notebook

```
.\.venv\Scripts\jupyter.exe notebook module6_lab2_sequential_chain.ipynb
```

Run the cells from top to bottom with **Shift+Enter**. This notebook processes five routine office requests. Each request goes through four steps: summary, cause and blockers, business impact, and action plan. The results are saved to a file named **ops\_analysis\_results.json** in the same folder.

### Step 6: Run the other Lab 2 notebook (optional)

In the same PowerShell window, stop the first notebook (Ctrl+C, then **y**). Then run:

```
.\.venv\Scripts\jupyter.exe notebook module6_lab2_corporate_ops.ipynb
```

This notebook does the same four-step job in a shorter form, using the functions in `ops_workflow.py`. It also saves **ops\_analysis\_results.json**.

### Step 7: Run the script (optional)

Scripts run without a notebook. Type this in PowerShell and press **Enter**:

```
.\.venv\Scripts\python.exe ops_workflow.py
```

**Warning:** This replaces the results file **ops\_analysis\_results.json** with the new results.

---

---

## Part 8: Troubleshooting

Find the error message you see in the first column.

| What you see | What to do |
| :---- | :---- |
| `python` is not recognized | Ask your facilitator for help with this computer. |
| `OPENAI_API_KEY not found` or an empty key | Open the `.env` file again. Check that the line starts with `OPENAI_API_KEY=`, that the key is on the same line, and that you saved the file. |
| `401` or `Incorrect API key` | The key was copied wrongly or is no longer valid. Copy it again, with no extra spaces. If it still fails, create a new key (Part 2\) or ask your facilitator for one. |
| `429`, `quota` or `billing` | Your OpenAI account has no credit or has hit its limit. Ask your facilitator. |
| `404`, `model does not exist` or a model name error | The model name is out of date. Lab 1 sets the model in `.env` (`OPENAI_MODEL=gpt-4o-mini`). Labs 2 and 3 set it in the notebook or script; change it to `gpt-4o-mini`. If your account still cannot use that model, ask your facilitator. |
| `No module named ...` (for example `langchain`) | The install step was skipped or failed. Go back to the install step for that lab and run it again. Make sure you are in the correct lab folder. |
| The notebook opens but a cell fails with a missing package | Stop the notebook, close the browser tab, and start again using the `jupyter.exe` command from that lab's guide. Then run the cells from the top. |
| `path too long` during installation | Ask your facilitator. This is a Windows setting that needs changing on the computer. |
| The `.venv` folder causes errors | Delete the `.venv` folder, then create it again with Step 2 or Step 3 of the lab. |
| The browser does not open | Copy the link in PowerShell that starts with `http://localhost` and paste it into your browser. |
| A cell is taking a long time | Wait up to a minute. AI calls can be slow. If nothing happens, press **Ctrl+C** in PowerShell and run the notebook again. |
| The notebook shows old results | Click **Kernel \> Restart & Run All** from the notebook menu, then check the results again. |

---

## Part 9: Quick Reference

### Commands for every lab

Replace the folder in each step with the lab you are working on. Always run the commands from inside that lab folder.

| Task | Command |
| :---- | :---- |
| Create the toolbox | `python -m venv .venv` |
| Install lab tools | `.\.venv\Scripts\python.exe -m pip install -r <requirements file>` |
| Open a notebook | `.\.venv\Scripts\jupyter.exe notebook <notebook file>` |
| Run a script | `.\.venv\Scripts\python.exe <script file>` |
| Stop a notebook | Press **Ctrl+C** in PowerShell, then type **y** |
| Run a notebook cell | Click the cell, then press **Shift+Enter** |

### Requirements files by lab

| Lab folder | Install this file |
| :---- | :---- |
| Module 6 \- Lab 1 | `lab1_m6_requirements.txt`, then `jupyter` |
| Module 6 \- Lab 2 | `requirements_module6_lab2.txt` |

Settings files by lab

| Lab folder | Settings file | Setting to fill in |
| :---- | :---- | :---- |
| Module 6 \- Lab 1 | `.env` | `OPENAI_API_KEY=` (and `OPENAI_MODEL=gpt-4o-mini`) |
| Module 6 \- Lab 2 | `.env` | `OPENAI_API_KEY=` |

---

## Part 10: Safety Checklist

Before you finish, check these points:

- [ ] I used sample data only and did not enter real customer, employee or financial records.  
- [ ] I did not share my API key with anyone, and I did not paste it into a chat, email or document.  
- [ ] I did not send my `.env` files to anyone.  
- [ ] I did not move, rename or delete any lab files, except a broken `.venv` folder.  
- [ ] I saved my work and closed each notebook with Ctrl+C in PowerShell before shutting down.

---

## Part 11: Glossary

- **AI model:** the program that writes the answers in the labs. The labs call it through OpenAI.  
- **Chain:** a set of steps where the output of one step becomes the input of the next.  
- **Prompt template:** a set of instructions with blank spaces that the lab fills in, such as `{ticket_text}`.  
- **Parser:** the part that turns the AI reply into plain text the next step can use.  
- **JSON file:** a text file that stores structured results. The labs save their results as JSON.  
- **Sequential chain:** steps that run one after another, in a fixed order.  
- **Router chain:** a chain that picks a different path depending on the question.  
- **Conversational chain:** a chain that remembers earlier messages in the same conversation.

---

*End of guide. If you get stuck, raise your hand and ask your facilitator. Bring the error message with you.*