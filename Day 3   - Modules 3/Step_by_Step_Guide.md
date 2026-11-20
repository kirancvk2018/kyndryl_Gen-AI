# Module 3: Multimodal GenAI - Step-by-Step Guide

This guide is for everyone taking Module 3, including people who are new to programming. You will use two hands-on tools, called **labs**, to see how AI can read pictures of IT systems (such as server racks and dashboards) and explain what it sees.

- **Lab 1** runs in your web browser as a notebook. You press a button to run each part, one at a time.
- **Lab 2** is a small website that runs on your own computer. You upload a picture and get an analysis back.

You do not need to write any code. You only need to type the commands shown in this guide, one line at a time, and follow the steps in order.

## Part 0: Before You Start

### What you need

- **An OpenAI API key.** This is a secret password that lets the labs use OpenAI's AI service. Your trainer will tell you where to get one. Keep it private.
- **The project folder** on your computer.
- **A text editor** such as Notepad, to change one setting file. Every computer has one.
- **A terminal window.** This is a black or blue window where you type commands. In this guide we use **Windows PowerShell**. To open it, click the Start button, type `PowerShell`, and press **Enter**.

### Cost: please read before you start

The labs use a paid service. Each image you analyze costs about $0.01 to $0.02. A few test runs cost very little, but running all six sample images in batch costs a few cents more. Always check with your trainer before running large batches.

### Key words used in this guide

| Word | What it means |
|------|---------------|
| **Terminal / PowerShell** | A window where you type commands instead of clicking buttons. |
| **Command** | One line of text you type into the terminal, then press Enter. |
| **Folder** | A place on your computer that holds files. Also called a directory. |
| **Virtual environment (venv)** | A private, self-contained toolbox for one lab. It keeps each lab's software separate from the others. |
| **Package / requirements** | Extra software a lab needs. The requirements file is a list of those packages. |
| **API key** | A secret code that gives the lab permission to use the AI service. |
| **`.env` file** | A small settings file that stores your API key. |
| **Jupyter notebook** | A web page made of boxes called cells. You run one cell at a time. |
| **Streamlit** | The tool that turns Lab 2 into a web page you can use in your browser. |
| **JSON** | A structured text format for results, with labels such as `"health_status"`. |
| **Database (SQLite)** | A single file that remembers every analysis Lab 2 has done. |
| **Port 8501** | The address on your own computer where Lab 2 is running. |

### How the project is organized

Think of the project as a set of folders. You will mainly work in two of them.

```
Day 3   - Modules 3-20261116T100755Z-1-001/        <- the main project folder
├── Step_by_Step_Guide.docx                        <- this guide (Word version)
├── Step_by_Step_Guide.md                          <- this guide (text version)
├── Detailed_Module_03_..._Learner_Guide.docx      <- reading material
├── Introduction-to-Large-Language-Models-LLMs.pptx <- slides for the module
└── Day 3   - Modules 3/
    ├── Module 3 - Lab 1/                          <- Lab 1 (notebook) lives here
    │   ├── module3_lab1_image_analysis.ipynb
    │   ├── sample_images/                         <- the pictures you will analyze
    │   ├── analysis_results/                      <- saved results appear here
    │   └── incident_reports/                      <- saved reports appear here
    └── Module3  - Lab 2/                          <- Lab 2 (web app) lives here
        ├── module3_lab2_image_app.py
        └── analysis_history.db                    <- the app's memory of past analyses
```

### Where the virtual environment goes

Each lab gets its own virtual environment, called `venv`. You create it **inside the same folder as that lab**, so each lab folder ends up with its own `venv` subfolder. Do not use one `venv` for both labs.

### Keep your API key safe

- Never share the `.env` file.
- Never paste your key into a chat, email, or document.
- If you think someone else has your key, ask your trainer to help you delete it and create a new one.

## Part 1: Lab 1 - Analyzing Pictures in a Notebook

**What you will do:** Ask the AI to look at infrastructure pictures, such as a server rack or a monitoring dashboard. You will get a written analysis, structured results, and a ready-to-file incident report.

### Step 1: Open a terminal in the Lab 1 folder

1. Open PowerShell (see Part 0).
2. Type the command below and press **Enter**. It moves the terminal into the Lab 1 folder.

```powershell
cd "Day 3   - Modules 3\Module 3 - Lab 1"
```

**You have succeeded when:** the line in the terminal ends with `Module 3 - Lab 1>`.

*What this does:* `cd` means "change folder". The quotation marks are needed because folder names contain spaces.

### Step 2: Create the virtual environment

```powershell
python -m venv venv
```

**What this does:** It creates a private toolbox called `venv` inside the Lab 1 folder. It takes a few seconds and prints nothing when it finishes.

**You have succeeded when:** a new folder called `venv` appears in the Lab 1 folder.

### Step 3: Turn on the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

**What this does:** It switches the terminal to use the private toolbox from Step 2.

**You have succeeded when:** the line in the terminal starts with `(venv)`.

**If you see a red error about scripts being disabled,** type this once, press Enter, type `Y` and press Enter if asked, and then repeat this step:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

*What this does:* It allows PowerShell to run the activation script on your computer. It affects only your user account.

### Step 4: Install the software the lab needs

```powershell
pip install -r module3_requirements.txt
```

**What this does:** It downloads and installs the packages listed in the requirements file. This takes a few minutes, and you will see a lot of text scroll past. That is normal.

**You have succeeded when:** the text stops scrolling and a line starting with `Successfully installed` appears.

### Step 5: Add your API key

1. In File Explorer, open the Lab 1 folder.
2. Right-click the file named `.env`, choose **Open with**, and pick **Notepad**.
3. Find the line that starts with `OPENAI_API_KEY=`.
4. Make sure it reads exactly like this, with your key after the equals sign and no spaces:

```env
OPENAI_API_KEY=your-openai-key-here
```

5. Save the file (**Ctrl + S**) and close Notepad.

*Tip:* Leave the other lines in the file alone. The notebook reads only the `OPENAI_API_KEY` line.

### Step 6: Know what the sample pictures are

The folder `sample_images` contains six pictures. You do not need to make any new ones.

| File | What it shows |
|------|---------------|
| `01_server_rack.png` | A server rack with the health of each computer in it |
| `02_monitoring_dashboard.png` | Graphs of computer load over 24 hours, with service status |
| `03_network_topology.png` | A diagram of how the network connects |
| `04_error_screenshot.png` | An error message from a database connection |
| `05_data_center_layout.png` | A floor plan of the server room |
| `06_alert_log.png` | A list of system alerts from the last 24 hours |

*Note:* The old documentation mentions a script called `generate_sample_images.py`. It is **not** in the project, and you do not need it.

### Step 7: Open the notebook

```powershell
jupyter notebook module3_lab1_image_analysis.ipynb
```

**What this does:** It opens the notebook in your web browser. Keep the terminal window open while you work. Closing it will close the notebook.

**You have succeeded when:** a page titled with the notebook name opens in your browser.

### Step 8: Run the setup cells

A notebook is a list of boxes called **cells**. Each cell contains a small piece of code. To run a cell, click inside it and press **Shift + Enter**. Run the cells **in order from top to bottom**. Do not skip any.

Most of the first cells only define helper tools. They do not call the AI, so they cost nothing and are safe to run.

| Cell | What it does | Costs money? |
|------|--------------|--------------|
| Setup and Imports | Loads your key and creates the result folders if they are missing | No |
| Step 1: Load and Display Images | Lists and shows the sample pictures | No |
| Step 2: Image Encoding Function | Prepares pictures to send to the AI | No |
| Step 3: Analyze Images | Defines the analysis tool (five types) | No |
| Step 4: Extract Structured Insights | Defines the tool that produces structured results | No |
| Step 5: Generate Incident Reports | Defines the tool that writes the report | No |
| Step 6: Complete Analysis Workflow | Defines the full end-to-end process | No |
| Step 7: Batch Analysis | Defines the tool that processes a whole folder | No |
| Step 8: Utility Functions | Defines the export and summary tools | No |

**You have succeeded when:** the Setup cell prints `OpenAI API Key loaded: True`.

**If it prints `False`:** go back to Step 5 and check the `.env` file, then close the notebook, stop the terminal with **Ctrl + C**, and start again from Step 7.

### Step 9: Analyze one picture (Example 1)

Click the cell labelled **Example 1** and press **Shift + Enter**. The lab will analyze the server rack picture.

**What happens:**

1. The picture appears on the screen.
2. The AI writes a description of the picture, its problems, and what to do about them.
3. The AI produces a structured summary, with a health status such as `critical`.
4. Two files are saved for you (see Step 12).

**You have succeeded when:** a report with a ticket number such as `INC-2026...` appears below the cell.

### Step 10: Analyze a dashboard (Example 3)

Click the cell labelled **Example 3** and press **Shift + Enter**. This analyzes the monitoring dashboard picture.

Compare the result with Example 1. The AI focuses on different things because the type of picture and the question are different.

### Step 11: Analyze all six pictures (Example 2)

**Warning: this costs money.** Example 2 analyzes all six pictures, and each one needs two calls to the AI. Check with your trainer before you run it.

Click the cell labelled **Example 2** and press **Shift + Enter**. It runs by itself when you do this. Wait until it finishes. You will see one line per picture showing a tick or a cross.

### Step 12: Find your results

Open File Explorer and look in these two folders, inside the Lab 1 folder:

| Folder | What you will find |
|--------|--------------------|
| `incident_reports` | One text file per analysis. Each one is a ticket with a ticket number, the picture name, the AI's findings, and next steps. |
| `analysis_results` | Structured files (`.json`) with the health status and the list of issues. |

*Tip:* Double-click a `.txt` file to open it in Notepad.

### Step 13: Practice (optional)

Try one of these tasks:

1. Analyze one picture and write down the three most serious issues the AI found.
2. Compare the dashboard and the server rack. Which one shows more urgent problems?
3. Run all six pictures and list them from most to least serious.
4. Change one sentence in the analysis instructions and run it again to see how the answer changes. Ask your trainer which sentence to change first.

### Step 14: Stop Lab 1

1. Close the notebook browser tab.
2. Click in the terminal window and press **Ctrl + C**. If asked whether to stop, type `Y` and press Enter.
3. Turn off the toolbox by typing this and pressing Enter:

```powershell
deactivate
```

**You have succeeded when:** the `(venv)` at the start of the line disappears.

## Part 2: Lab 2 - The Picture Analysis Website

**What you will do:** Run a small website on your own computer. Upload a picture, choose what kind of analysis you want, read the result, download it, and look back at everything you have analyzed before.

### Step 1: Open a terminal in the Lab 2 folder

Type this in PowerShell and press **Enter**. Note the **two spaces** in `Module3  - Lab 2`. They must be typed exactly.

```powershell
cd "..\Module3  - Lab 2"
```

*If the terminal is still in the Lab 1 folder,* this line moves you up one level and into Lab 2. If you are not sure where you are, type `cd` followed by the full path to the project. Your trainer can show you where the project is saved.

**You have succeeded when:** the line in the terminal ends with `Module3  - Lab 2>`.

### Step 2: Create the virtual environment

```powershell
python -m venv venv
```

**You have succeeded when:** a new folder called `venv` appears in the Lab 2 folder.

### Step 3: Turn on the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

**You have succeeded when:** the line starts with `(venv)`.

*If you see a red error about scripts being disabled,* use the fix from Lab 1, Step 3.

### Step 4: Fix one line in the requirements file

The file `lab2_requirements.txt` has a line that will cause the installation to fail:

```text
sqlite3  # Built-in, no need to install
```

This package is already part of Python, so it should not be installed.

1. Open `lab2_requirements.txt` in Notepad.
2. Put a `#` at the very start of that line, so it reads `# sqlite3  # Built-in, no need to install`.
3. Save the file (**Ctrl + S**) and close Notepad.

### Step 5: Install the software the lab needs

```powershell
pip install -r lab2_requirements.txt
```

**What this does:** It downloads and installs the packages. This takes a few minutes.

**You have succeeded when:** a line starting with `Successfully installed` appears and the text stops scrolling.

### Step 6: Check your API key

1. Open the `.env` file in the Lab 2 folder with Notepad.
2. Find the line starting with `OPENAI_API_KEY=` and make sure your key is after the equals sign, with no spaces:

```env
OPENAI_API_KEY=your-openai-key-here
```

3. Save and close the file.

*Tip:* The other lines in this file are not used by the website. Leave them alone.

### Step 7: Start the website

```powershell
streamlit run module3_lab2_image_app.py
```

**What this does:** It starts the website on your computer. The terminal will show a few lines of text, including an address such as `http://localhost:8501`.

**You have succeeded when:** your web browser opens a page titled **IT Infrastructure Image Analyzer**. If it does not open, copy the address from the terminal into your browser yourself.

*Keep the terminal open while you use the website.* Closing it stops the website.

The first time the website runs, it creates a file called `analysis_history.db` in the Lab 2 folder. This file stores your history.

### Step 8: Analyze a picture

1. **Pick a page.** On the left side of the screen, under **Navigation**, click **Analyze Image**.
2. **Pick an analysis type.** Under **Settings**, open the drop-down list. Choose one:
   - **General** - for anything
   - **Server Rack** - for server pictures
   - **Dashboard** - for graphs and monitoring screens
   - **Network** - for network diagrams
   - **Error Log** - for error messages
3. **Upload a picture.** Under **Upload Image**, click **Browse files**. Go to the Lab 1 folder, then into `sample_images`, and choose a picture. You can use JPG, PNG, GIF, or WEBP files up to 20 MB.
4. **Check the upload.** A green message confirms the picture is accepted, and a preview appears.
5. **Choose extra details (optional).** The box **Extract structured insights (JSON)** is ticked by default. Leave it ticked to get the numbers and labels, such as the health status.
6. **Start the analysis.** Click the big **Analyze Image** button. A spinner shows while the AI works. This takes a few seconds.
7. **Read the result.** The page shows:
   - a written summary,
   - the health status and severity,
   - how many components and issues were found,
   - the detailed structured results (under **View JSON Insights**).
8. **Download (optional).** Under **Download Results**, click **Download Analysis (TXT)** for the written summary or **Download Insights (JSON)** for the structured data. The file goes to your browser's Downloads folder.

**Good to know:** every analysis is saved automatically, even if it fails.

### Step 9: Look back at past analyses

1. On the left, click **Analysis History**.
2. A table shows the 50 most recent analyses, with the date and time, the picture name, the type, and whether it succeeded.
3. To see one in full, click its **View** button. The full result appears below the table.

### Step 10: Try different analysis types

Use the same picture with two different analysis types, and compare the results. Good pairs to try:

- `01_server_rack.png` with **Server Rack**, then with **General**
- `02_monitoring_dashboard.png` with **Dashboard**, then with **General**
- `04_error_screenshot.png` with **Error Log**
- `03_network_topology.png` with **Network**

### Step 11: Read the About page (optional)

On the left, click **About** to read a short description of the website and how it works.

### Step 12: Stop the website

1. Click in the terminal window.
2. Press **Ctrl + C**.
3. Type this and press Enter to turn off the toolbox:

```powershell
deactivate
```

### Starting over with an empty history (optional)

Only do this if your trainer asks you to. It deletes every saved analysis.

1. Stop the website first (Step 12 above).
2. Type this and press Enter:

```powershell
Remove-Item analysis_history.db
```

3. Start the website again with the command from Step 7. A new, empty history file is created automatically.

## Part 3: Reading Materials

You can read these before, between, or after the labs. You do not need a computer to read them.

1. **Learner Guide** (`Detailed_Module_03_..._Learner_Guide.docx`). A reading of about 4 hours that explains what large language models are, how they work, the types of models, what they are used for, and their limits. It ends with five questions to check your understanding.
2. **Slides** (`Introduction-to-Large-Language-Models-LLMs.pptx`). Ten slides covering the same ideas in a presentation format.
3. **Lab notes.** Each lab folder has a quick-start file (`START_HERE.md` or `LAB2_QUICKSTART.md`) and a longer README.

**Suggested order:** Learner Guide, then Slides, then Lab 1, then Lab 2.

## Part 4: When Something Goes Wrong

Find the message you see in the left column and follow the advice in the right column.

| What you see | What to do |
|--------------|------------|
| No `(venv)` at the start of the line | Make sure you are in the right folder, then type the activate command from Step 3 again. |
| "running scripts is disabled on this system" | Type the `Set-ExecutionPolicy` command from Lab 1, Step 3, then try again. |
| "No module named ..." | Check that `(venv)` is showing. Then run the install command again. |
| The install stops with an error about `sqlite3` | Do the fix in Lab 2, Step 4, then run the install again. |
| "OpenAI API Key loaded: False" (Lab 1) or "OPENAI_API_KEY not found" (Lab 2) | Open `.env` in the same folder, check the key line has no spaces around the `=`, save the file, then restart the notebook or website. |
| An error about authentication, permission, or quota | Your key may be wrong or out of credit. Ask your trainer. |
| The website page is blank, or says the port is in use | Close any other website from this course, or type this instead and press Enter: `streamlit run module3_lab2_image_app.py --server.port 8502`, then open `http://localhost:8502`. |
| "File is too large" or "Invalid file type" | Use a JPG, PNG, GIF, or WEBP picture under 20 MB. |
| The history table is empty | Analyze a picture first. If you still see nothing, check that you started the website from the Lab 2 folder. |
| The notebook says "No images found" | Check that you started the notebook from the Lab 1 folder and that `sample_images` is there. |

## Part 5: Good to Know

These are small problems in the course files. You can ignore them unless something goes wrong.

1. **Some documents mention a different AI company (Anthropic).** These labs use **OpenAI** only. Please follow this guide, not the older documents.
2. **Some links in the old documents are broken.** Use the folder names in this guide instead.
3. **The batch example costs money.** Example 2 in Lab 1 runs as soon as you press Shift + Enter on it.
4. **Some settings in the `.env` files are not used.** Only the `OPENAI_API_KEY` line matters.

## Part 6: Quick Reference

Use this section as a checklist once you know the steps.

### Lab 1 (run from inside `Module 3 - Lab 1`)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r module3_requirements.txt
jupyter notebook module3_lab1_image_analysis.ipynb
deactivate
```

### Lab 2 (run from inside `Module3  - Lab 2`, after fixing the `sqlite3` line)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r lab2_requirements.txt
streamlit run module3_lab2_image_app.py
deactivate
```

### Where to find your results

| Result | Where it is |
|--------|-------------|
| Incident reports (Lab 1) | Lab 1 folder, `incident_reports` |
| Structured results (Lab 1) | Lab 1 folder, `analysis_results` |
| Analysis history (Lab 2) | Lab 2 folder, `analysis_history.db` |
| Downloaded files (Lab 2) | Your browser's Downloads folder |

### Glossary

The words in the table in Part 0 explain everything used in this guide.
