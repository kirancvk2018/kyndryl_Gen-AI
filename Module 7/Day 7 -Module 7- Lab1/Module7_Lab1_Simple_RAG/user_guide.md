# Module 7 – Lab 1: Simple RAG with LangChain

User Guide: step-by-step instructions to run the lab on Windows

| Item | Details |
| --- | --- |
| Audience | Module 7 participants (Python beginners with an introductory GenAI background) |
| Time needed | About 60 to 90 minutes, including time for API calls |
| Lab folder | `Module7_Lab1_Simple_RAG` |
| Main file | `module7_lab1_simple_rag.ipynb` (the notebook you will run) |
| Python | The Python already installed on your computer (3.10 or newer) |

## About this lab

In this lab you will build an **Operations Knowledge Assistant**. It answers questions such as “What should be checked when CPU utilization exceeds 90%?” by using only the information in a knowledge base file. If the answer is not in the file, the assistant says so instead of guessing.

You will work through the five stages of a RAG (Retrieval-Augmented Generation) application: **load** the documents, **split** them into chunks, **embed** the chunks as numbers, **retrieve** the most relevant chunks for a question, and **generate** an answer with an LLM.

## Part 1 – Before you start

Check each item before you begin. Tick the box when it is ready.

| Requirement | How to check | Ready |
| --- | --- | --- |
| Python 3.10 or newer is installed | Open PowerShell and type `python --version` | ☐ |
| The lab folder is complete | The folder contains `requirements.txt`, `module7_lab1_simple_rag.ipynb`, `operations_knowledge_base.csv`, `.env.example`, `README.md` and `.gitignore` | ☐ |
| VS Code is installed with the Python and Jupyter extensions | Open VS Code, press Ctrl+Shift+X and search for “Python” and “Jupyter” | ☐ |
| You have an OpenAI API key | Your facilitator will give you a key or explain how to create one | ☐ |
| You are connected to the internet | The lab calls the OpenAI API while it runs | ☐ |

> **Important rules.** Do not create a virtual environment and do not install another Python. Use the Python that is already on your computer. Never paste your API key into the notebook, a chat or a screenshot, and never share the `.env` file.

## Part 2 – Set up Python and the packages

### Step 1 – Open PowerShell in the lab folder

1. Open File Explorer and go to the `Module7_Lab1_Simple_RAG` folder.
2. Click in the address bar, type `powershell` and press Enter.

**Expected result:** a PowerShell window opens and its prompt ends with `Module7_Lab1_Simple_RAG>`.

### Step 2 – Check the Python interpreter

Type these two commands, one after the other, pressing Enter after each:

```powershell
python --version
python -m pip --version
```

**Expected result:** `Python 3.10.11` (or another 3.10 or newer version). The pip line should show the same Python installation. If PowerShell says that `python` is not recognized, stop and ask your facilitator. Do not install another Python.

### Step 3 – Install the required packages

Run the install command from the lab folder:

```powershell
python -m pip install -r requirements.txt
```

- Wait until the prompt (`PS ...>`) returns. This can take a few minutes the first time.
- You may see “Collecting” lines (a fresh install) or “Requirement already satisfied” lines (already installed). Both are fine.
- The command does not upgrade the LangChain packages, so the versions stay as the lab expects.

### Step 4 – Confirm the LangChain version

Check that the main LangChain package is the expected version:

```powershell
python -m pip show langchain
```

**Expected result:** a line that reads `Version: 1.3.14`. If it shows a different version, ask your facilitator before continuing.

## Part 3 – Add your OpenAI API key

### Step 5 – Create your .env file

The lab reads your key from a file called `.env`. Create it by copying the template:

```powershell
Copy-Item .env.example .env
```

**Expected result:** no message appears. Run `dir .env` to confirm a file named `.env` now exists.

### Step 6 – Add your API key

1. Open the file in Notepad with this command: `notepad .env`
2. Replace `your_openai_api_key_here` with your key. The line must stay on one line and look like this:

   ```text
   OPENAI_API_KEY=sk-...your key...
   ```

3. Save the file (Ctrl+S) and close Notepad.

> **Tip.** If you cannot see the file extension, open File Explorer, choose **View > Show > File name extensions**. The file must be named `.env`, not `.env.txt`.

## Part 4 – Open the notebook in VS Code

### Step 7 – Open the lab folder in VS Code

In the PowerShell window from Step 1, type:

```powershell
code .
```

If PowerShell says that `code` is not recognized, open VS Code, choose **File > Open Folder** and select the `Module7_Lab1_Simple_RAG` folder.

### Step 8 – Open the notebook

In the Explorer panel on the left (Ctrl+Shift+E), click `module7_lab1_simple_rag.ipynb`. The notebook opens with Markdown explanations and grey code cells.

### Step 9 – Select the Python interpreter

1. Press Ctrl+Shift+P.
2. Type `Python: Select Interpreter` and press Enter.
3. Choose the Python 3.10.x entry that matches the version you checked in Step 2.

**Expected result:** the bottom-right corner of VS Code shows Python 3.10.x.

### Step 10 – Select the kernel

1. At the top right of the notebook, click **Select Kernel**.
2. Choose **Python Environments** and the same Python 3.10.x entry.

**Expected result:** the kernel name appears at the top right of the notebook. If several Python 3 entries are listed, choose the one whose version matches Step 2.

## Part 5 – Run the notebook section by section

### How to run a cell

- Click inside a grey code cell and press **Shift+Enter**. The cell runs and the cursor moves to the next cell.
- A number such as `[3]` appears to the left of a cell when it has finished. A `[*]` means it is still running.
- Run the cells **in order, from top to bottom**. Each section uses variables created in the sections above it.
- To start again from a clean state, click **Restart** on the notebook toolbar, then **Run All**.
- Each full run calls the OpenAI API, so it has a small cost. Avoid repeating a full run unless you need to.

### Step 11 – Run each section

Work through the sections in this order. The table shows the cells to run and what you should see.

| Section | Cells to run | What you should see |
| --- | --- | --- |
| 1. Introduction to RAG | Nothing to run. Read the explanation and the flow diagram. | Explanation text only. |
| 2. Environment Setup | The imports cell, the configuration cell and the verification cell, in that order. | `All libraries imported.` A list of package versions, including `langchain 1.3.14`. The line `OPENAI_API_KEY loaded: True`. If it says `False`, stop and fix the `.env` file (Part 3). |
| 3. Load the knowledge base | The loader cell, then the inspection cell. | `Loaded 29 documents from operations_knowledge_base.csv`. Then the first record (`Record_ID: OPS-001`) and its metadata. |
| 4. Text splitting | The splitter cell, then the chunk display cell. | `29 documents were split into 34 chunks.` Then two sample chunks. Chunk 1 starts at `Procedure:`, which is expected. |
| 5. Embedding generation | The embedding model cell, then the sample embedding cell. | `Embedding model ready: text-embedding-3-small`, then `Embedding dimensions: 1536`. |
| 6. Vector store and retrieval | The cell that builds the FAISS vector store, then the search cell. | `FAISS vector store created with 34 vectors.` Then `Number of relevant documents returned: 3` and three records. |
| 7. Build the RAG chain | The chat model cell, the prompt cell, the chain cell and the sample question cell. | `Chat model ready: gpt-4o-mini`, then an answer that begins “1) Confirm the CPU reading on the monitoring dashboard…”. |
| 8. Ask questions | The `ask_question` cell, the five-question cell, then the cell with the UPS question. | Five questions with answers taken from the records. The UPS question returns: `The answer could not be found in the available Operations Knowledge Base.` |
| 9. Pipeline trace | Both trace cells. | `Original documents loaded: 29`, `Text chunks created: 34`, `Question embedding length: 1536`, the retrieved records and a final answer. |
| 10. Exercises and quiz | Read only. Do the exercises in Part 8 and the quiz. | Skip the instructor answer key at the end. It is for facilitators. |

> **Note.** Answers can differ slightly from one run to the next. Check that the facts match the record named in the answer, not the exact wording.

> **If a cell shows a red error,** read the last line of the error first. Part 10 explains the common messages.

## Part 6 – Ask your own question

### Step 12 – Add a cell and ask a question

1. Click below the last cell of Section 8 (the UPS question).
2. Click **+ Code** on the notebook toolbar to add a new code cell.
3. Paste this code and press Shift+Enter:

   ```python
   my_question = "What is the escalation procedure for a critical infrastructure incident?"
   print(ask_question(my_question))
   ```

**Expected result:** the escalation steps from record OPS-015, including the Incident Manager on-call and the one-hour and four-hour points at which escalation rises.

Then try these questions in the same way:

- “Who should be contacted if the database is down?” (answer: the Database Administrator on-call team, record OPS-006).
- “How do I reset a user password?” (the knowledge base does not cover this, so the assistant should say the answer could not be found).

## Part 7 – Switch from the CSV to your own PDF (optional)

### Step 13 – Use your own PDF

1. Copy your PDF into the `Module7_Lab1_Simple_RAG` folder. Use a text-based PDF, where you can select the text. A scanned PDF (an image of pages) does not work.
2. In the configuration cell in Section 2, change the `KB_PATH` line to the name of your file:

   ```python
   KB_PATH = "your_file_name.pdf"
   ```

3. Click **Restart**, then **Run All**.
4. **Expected result:** `Loaded N documents from your_file_name.pdf`, where N is the number of pages.
5. Ask questions that your PDF can answer. The five questions in Section 8 were written for the CSV file, so most will return “not found” for a different document. That is the correct behaviour.
6. To go back to the CSV, set `KB_PATH = "operations_knowledge_base.csv"` and run all cells again.

> **How it works.** The notebook chooses the loader from the file extension. A `.csv` file uses CSVLoader (one document per record). A `.pdf` file uses PyPDFLoader (one document per page).

## Part 8 – Hands-on exercises

### Step 14 – Complete the five exercises

Make each change in the notebook, re-run the cells that depend on it, and compare the results.

| Exercise | What to change | What to check |
| --- | --- | --- |
| 1. Add three records | Add rows OPS-030, OPS-031 and OPS-032 to `operations_knowledge_base.csv`, using the same column order. Save the file, then click **Restart** and **Run All**. | The document count is 32. Ask a question that one of the new records answers. |
| 2. Change the chunk size | Set `CHUNK_SIZE` to 300, then 500, then 1000. Keep `CHUNK_OVERLAP = 100`. Re-run Section 4 and the Section 6 vector store cells. | Chunk counts of about 122, 71 and 29 (800 gives 34). Smaller chunks produce more chunks. Explain why. |
| 3. Change top-k | Set `TOP_K = 5`. Re-run the search cell in Section 6 and the sample question in Section 7. | Five records are retrieved. Do the two extra records help, or do they add noise? |
| 4. Make answers more concise | Edit the text of the prompt cell in Section 7, for example by adding “Answer in at most three short bullet points.” Re-run Section 7 and then Section 8. | Answers are shorter. Keep the exact “not found” sentence in the prompt. |
| 5. Ask an unanswerable question | Ask about a topic the knowledge base does not cover, such as onboarding a new employee, using the same method as Part 6. | The assistant says the answer could not be found. If it invents a procedure, report it to your facilitator. |

**Quiz.** Answer the five multiple-choice questions at the end of Section 10. Write your answers on paper or in a new Markdown cell. Your facilitator has the answer key.

## Part 9 – Finish and save

### Step 15 – Close the session

1. Save the notebook with **Ctrl+S**.
2. Keep the `.env` file on your own computer. Do not upload it, email it or add it to git. The `.gitignore` file already excludes it.
3. Close VS Code and the PowerShell window.

**Expected result:** the notebook is saved and no other steps are needed.

## Part 10 – Troubleshooting

Find the message or symptom you see in the first column and follow the action in the last column.

| Message or symptom | Likely cause | What to do |
| --- | --- | --- |
| `'python' is not recognized` | Python is not on the PATH. | Ask your facilitator. Do not install another Python. |
| `ModuleNotFoundError: No module named ...` | The packages were installed into a different Python than the one the notebook uses. | Check Step 9. Then repeat Step 3 in the lab folder and click **Restart**, then **Run All**. |
| `OPENAI_API_KEY not found` (in Section 2) | The `.env` file is missing, misnamed or empty. | Repeat Steps 5 and 6. Check that the file is named `.env` and not `.env.txt`. |
| `401` or `Incorrect API key` | The key was copied wrongly or is no longer valid. | Copy the key again with no extra spaces. If it still fails, ask your facilitator. |
| `404` or `model does not exist` | A model name is not available to your account. | Ask your facilitator. Only then change `CHAT_MODEL` or `EMBEDDING_MODEL` in the configuration cell. |
| `429`, quota or rate-limit error | Too many requests, or no credit left. | Wait a minute and try again, avoid repeated full runs, or ask your facilitator. |
| `DeprecationWarning: langchain-community is being sunset` | A normal warning for this LangChain version. | Ignore it. The lab still works. |
| Cells do not run, or there is no kernel | The interpreter or kernel was not selected. | Repeat Steps 9 and 10. |
| `Knowledge base file '...' was not found` | `KB_PATH` does not match the file name, or the file is in another folder. | Check `KB_PATH` in the configuration cell. Keep the file in the lab folder. |
| `Unsupported file type '...'` | `KB_PATH` ends in something other than `.csv` or `.pdf`. | Use a `.csv` or `.pdf` file. |
| `No text was found in the knowledge base` | The PDF is scanned or has no selectable text. | Use a text-based PDF. Scanned pages need OCR first, which is outside this lab. |
| `UnicodeDecodeError` when loading the CSV | The CSV file was not saved as UTF-8. | In Excel, choose **Save As > CSV UTF-8 (Comma delimited)**. |
| Your answers differ from a classmate’s, or look wrong | Cells were run out of order, or the settings were changed. | Click **Restart**, then **Run All**. Check that `CHUNK_SIZE` is 800, `CHUNK_OVERLAP` is 100 and `TOP_K` is 3. |
| `faiss` installation error | There is no FAISS package for this Python version. | Tell your facilitator your Python version. Do not change the Python installation yourself. |

## Appendix A – Quick reference

| Task | Command or action |
| --- | --- |
| Check Python | `python --version` |
| Install the packages | `python -m pip install -r requirements.txt` |
| Check the LangChain version | `python -m pip show langchain` |
| Create the .env file | `Copy-Item .env.example .env` |
| Edit the .env file | `notepad .env` |
| Open the folder in VS Code | `code .` |
| Choose the interpreter | Ctrl+Shift+P, then **Python: Select Interpreter** |
| Run one cell | Shift+Enter |
| Run all cells | **Run All** on the notebook toolbar |
| Start again from a clean state | **Restart**, then **Run All** |
| Add a code cell | **+ Code** on the notebook toolbar |

## Appendix B – Glossary

| Term | Meaning in this lab |
| --- | --- |
| RAG | Retrieval-Augmented Generation: find relevant text first, then ask an LLM to answer using that text. |
| LLM | Large language model. This lab uses `gpt-4o-mini` to write the answers. |
| Document | A LangChain object that holds text (`page_content`) and information about where it came from (`metadata`). |
| Chunk | A piece of a document after it has been split. |
| Embedding | A list of 1,536 numbers that represents the meaning of a piece of text. |
| Vector store (FAISS) | A local index that finds the chunks whose embeddings are closest to a question. |
| Top-k | The number of chunks retrieved for each question. The lab uses `TOP_K = 3`. |
| LCEL chain | The pipeline built with the `\|` symbol that links the retriever, the prompt, the LLM and the output parser. |
| `.env` file | A private file on your computer that holds your API key. |
| Kernel | The Python process that runs the notebook cells. |
