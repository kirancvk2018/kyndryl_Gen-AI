# Module 7 – Lab 2 User Guide

Build a Vector Store and Retriever with LangChain and FAISS

| Item | Details |
|---|---|
| Lab | Module 7, Lab 2 (continues Module 7 Lab 1) |
| Project folder | Module7_Lab2_Vector_Store_Retriever |
| Notebook to run | module7_lab2_vector_store_retriever.ipynb |
| Python used for preparation | Python 3.10.11 (the interpreter already installed) |
| LangChain version | 1.3.14, the same version as Module 7 Lab 1 |

## 1. What this lab covers

In this lab you build a small search system over IT Operations knowledge-base records. The system finds the records most relevant to an engineer's question, and an AI model writes an answer using only those records. You will:

- Load 29 operations records from a CSV file.
- Split the records into 71 chunks of up to 500 characters, with 50 characters of overlap.
- Create embeddings with OpenAI and store them in a local FAISS vector index.
- Save the index to disk, and reload it later without creating the embeddings again.
- Use a retriever and an OpenAI language model to answer questions from the retrieved records.

## 2. Before you start

Check that you have the following:

- Python is already installed on your computer. Do not install another Python version.
- Visual Studio Code (VS Code), with the **Python** and **Jupyter** extensions.
- Module 7 Lab 1 completed. This lab reuses its dataset and LangChain versions.
- An OpenAI API key with available credit.
- An internet connection. The notebook sends text to the OpenAI service.

> **Important:** Do not create a new virtual environment or Conda environment, do not install Anaconda, and do not change the default Python interpreter. Use the Python interpreter that is already set up on your computer for this course.

## 3. Project files

| File | What it is for |
|---|---|
| module7_lab2_vector_store_retriever.ipynb | The lab notebook. You run this file. |
| operations_knowledge_base.csv | The IT Operations knowledge base: 29 records with seven columns. |
| requirements.txt | The list of packages the lab needs. |
| README.md | Reference notes: setup, architecture and troubleshooting. |
| .env.example | Template for your API-key file. Keep it unchanged. |
| .gitignore | Tells Git to ignore .env and the index folder. |
| .env | Created by you in Step 5. Holds your API key. Keep it private. |
| faiss_operations_index/ | Created automatically when the notebook runs. Holds the saved index. |

## 4. Step-by-step instructions

### Step 1 – Open the project folder in VS Code

1. Start VS Code.
2. Select **File > Open Folder**.
3. Select the **Module7_Lab2_Vector_Store_Retriever** folder, then select **Select Folder**.
4. If VS Code asks whether you trust the authors of the files, select the option to trust the folder (the files come from your facilitator).

**Check:** the Explorer panel lists the project files shown in Section 3.

### Step 2 – Open a terminal in the project folder

1. Select **Terminal > New Terminal**.
2. Check that the terminal location ends with **Module7_Lab2_Vector_Store_Retriever**.

### Step 3 – Check your Python installation

Type each command in the terminal and press Enter after each one:

```text
python --version
python -m pip --version
```

**Expected:** the first line shows **Python 3.10.x**. The second line shows the pip version, followed by a path inside the same Python 3.10 installation.

> **Note:** If the terminal says that Python was not found, ask your facilitator. Do not install Python yourself.

### Step 4 – Install the required packages

1. In the terminal, type the command below and press Enter.

```text
python -m pip install -r requirements.txt
```

2. Wait until the command finishes.

**Expected:** lines that say **Requirement already satisfied** (packages already installed), or installation progress, finishing without an error message.

This command installs only the packages listed in requirements.txt and keeps the LangChain versions used in Module 7 Lab 1. Do not run upgrade commands.

### Step 5 – Create your .env file and add your API key

1. Copy the template. In the terminal, use one of these commands. Copy the file; do not rename it.

```text
PowerShell:  Copy-Item .env.example .env
Command Prompt:  copy .env.example .env
```

2. Open the new **.env** file in VS Code.
3. Replace `your_openai_api_key_here` with your key. Keep `OPENAI_API_KEY=` and paste the key directly after the equals sign. Do not add spaces or quotation marks.
4. Save the file with **Ctrl+S**.

**Check:** the file name is exactly **.env**, not .env.txt and not “.env.example copy”. If you cannot see file name extensions in Windows, turn them on in File Explorer under **View > Show > File name extensions**.

> **Keep the key private:** Do not share the .env file, paste it into a chat or a screenshot, or put it in the notebook. The notebook checks that the key exists, but it never prints it. Leave .env.example unchanged.

### Step 6 – Open the notebook and select the Python interpreter

1. In the Explorer, select **module7_lab2_vector_store_retriever.ipynb**. The notebook opens.
2. At the top right of the notebook, select the kernel picker (it may say **Select Kernel**).
3. Choose the **same Python 3.10 interpreter** you checked in Step 3. If several are listed, choose the one that matches the path shown by this PowerShell command:

```text
(Get-Command python).Source
```

**Check:** the kernel shown at the top right is a Python 3.10 interpreter. If the packages are not found later, this is the first thing to recheck.

### Step 7 – Run the notebook from the top

1. Select **Run All** in the notebook toolbar. You can also select the first code cell and press **Shift+Enter**, then press Shift+Enter for each following cell.
2. Read each text (Markdown) cell before running the code cell below it.
3. Do not skip cells. Later cells use variables created by earlier cells.

> **Note:** The first run takes longer than later runs, because every one of the 71 chunks is sent to OpenAI for an embedding. If a cell stops with an error, read the message and see Section 6.

### Step 8 – Check the results

On the first run, look for the following results in the output of each section:

| Notebook section | What you should see |
|---|---|
| 2 – Environment Setup | Python 3.10.x, the LangChain versions, and **OPENAI_API_KEY loaded: True**. |
| 3 – Load the knowledge base | **Number of documents loaded: 29** |
| 4 – Text splitting | **29 documents were split into 71 chunks.** |
| 5 – Embeddings | **Embedding dimensions: 1536** |
| 6 – Create the FAISS index | **Saved index state: missing**, then *Building a new FAISS index*, then **Vectors in the index: 71**. The top result for the processor question is the CPU record **OPS-001**. |
| 7 – Persist the index | **Index saved to: faiss_operations_index**, and three files listed: index.faiss, index.pkl and index_metadata.json. |
| 8 – Reload the index | **Results from the original store and the reloaded store are identical: True** |
| 9 – Reuse rules | **Current index state: current**, and **Index state after a simulated edit: changed**. |
| 10 – Retriever | **Documents returned with k = 3 : 3**, and the k = 5 comparison lists five rows. |
| 11 – Connect to an LLM | **RAG chain built.** Each question retrieves the top 3 chunks. |
| 12 – Ask questions | Five answers, each shown after its context lines. The UPS question returns: *The answer could not be found in the available Operations Knowledge Base.* |

The wording of the AI answers can vary slightly between runs. A good answer uses only the records shown in the context lines above it.

### Step 9 – Look at the saved index

1. In the Explorer, open the **faiss_operations_index** folder.
2. Confirm that it contains three files: **index.faiss** (the vectors), **index.pkl** (the text and metadata of each chunk) and **index_metadata.json** (the settings and checksum).
3. Open **index_metadata.json**. Find `chunk_count` (71) and `embedding_model` (text-embedding-3-small).

> **Do not edit or share:** Do not edit these files by hand, and do not copy the folder to another person's computer. index.pkl is a Python pickle file. See Section 5.

### Step 10 – Test index reuse by restarting the kernel

1. Restart the kernel: select the **Restart** button on the notebook toolbar. You can also run **Notebook: Restart Kernel** from the Command Palette (Ctrl+Shift+P).
2. Select **Run All** again.

**Expected:** **Saved index state: current**, and the message *Reusing the saved index. No document embeddings will be generated.* Section 7 prints *The index was loaded from disk, so there is nothing new to save.*

A restart does not trigger a rebuild, because the checksum of the CSV has not changed. This saves the cost of embedding all 71 chunks again.

### Step 11 – Complete the exercises in Section 14

| Exercise | What to do |
|---|---|
| 1 – Create a vector store | Delete the **faiss_operations_index** folder, run the notebook from the top, and note the number of chunks embedded. |
| 2 – Persist the index | After Section 7, open **index_metadata.json** and find the checksum, the embedding model and the chunk count. |
| 3 – Reload the index | Restart the kernel, run from the top, and confirm the state is **current**. |
| 4 – Change top-k | Change `TOP_K` in the configuration cell from 3 to 5. In the same kernel session, re-run from Section 10 and compare the results. |
| 5 – Rebuild after changes | Add two records to **operations_knowledge_base.csv** with the same seven columns. Put any text that contains a comma in double quotes. Save the file, run the notebook from the top, and confirm the state is **changed** and the index is rebuilt. To undo, remove the new rows and run again. |

Answer the five quiz questions in Section 14 before you look for the answers. The answers are in the instructor section at the end of the notebook.

### Step 12 – Finish and save your work

1. Save the notebook with **Ctrl+S**.
2. Keep the **.env** file private, and do not commit it to Git.
3. Keep the **faiss_operations_index** folder on your own computer.

## 5. Important notes

### Cost

The first build sends every chunk to the OpenAI embedding model, and that is billed. Restarting the notebook does not send the chunks again. Each question costs a small embedding call plus one call to the language model. For this lab the amounts are small, but they depend on your account's pricing.

### Security of the saved index

The index file **index.pkl** is a Python pickle file. Loading a pickle can run any code it contains. The notebook loads only the index that it created on your computer.

- Never load an index folder that someone else created or sent to you.
- Never download an index file from an unknown source.
- Do not share the faiss_operations_index folder with untrusted people.

### Expected messages

- A **DeprecationWarning** about langchain-community appears in the output. It is expected with this version and does not stop the notebook.
- The diagrams in the Markdown cells are text descriptions of the flow. Some viewers do not draw them.

## 6. Troubleshooting

| Problem | What to do |
|---|---|
| The terminal says Python was not found. | Ask your facilitator. Do not install Python yourself. |
| The pip install command fails. | Check that the terminal is in the project folder (Step 2) and run the command again. If the message mentions permissions, ask your facilitator. |
| The notebook stops with **OPENAI_API_KEY not found**. | Check that the file is named exactly **.env** (not .env.txt) and is in the project folder. Save it, then restart the kernel. |
| Error 401, or **Incorrect API key provided**. | The key is wrong, or there are extra spaces or quotation marks in .env. Paste the key again, save, and restart the kernel. |
| Error about **insufficient_quota** or a rate limit. | Your OpenAI account has no credit left or has reached a limit. Check billing in your OpenAI account, or ask your facilitator. |
| **ModuleNotFoundError** for langchain, faiss or dotenv. | The notebook is using a different interpreter. Repeat Step 6 with the interpreter you checked in Step 3. |
| **FileNotFoundError** for operations_knowledge_base.csv. | Open the project folder in VS Code (Step 1) and run the notebook from there. |
| The index is rebuilt on every run. | Check that `REBUILD_INDEX` is `False`, that index_metadata.json exists, and that the CSV and chunk settings have not changed. |
| **Error while loading the saved index**. | Delete the faiss_operations_index folder and run the notebook again. It rebuilds the index from the CSV. |
| A cell seems to run for a long time. | The first build can take several minutes. Check your internet connection. If it stops responding, select the Interrupt button, then run again from the top. |
| The answer wording is different from this guide. | This is normal. Check that the answer uses only the records shown in its context lines. |

## 7. Glossary

| Term | Meaning in this lab |
|---|---|
| Chunk | A piece of a record of up to 500 characters. Chunks are what gets embedded. |
| Embedding | A list of numbers that represents the meaning of a piece of text. |
| Vector store | A store of embeddings that can find the closest matches to a question. |
| FAISS | A library for fast similarity search. It runs on your computer. |
| Index | The searchable structure built from the embeddings. It is saved in faiss_operations_index. |
| Retriever | The component that returns the most relevant chunks for a question. |
| Top-k | The number of chunks returned for each question. This lab uses TOP_K = 3. |
| Checksum | A SHA-256 fingerprint of the CSV file. It changes whenever the file changes. |
| Kernel | The Python process that runs the notebook cells. |
| LLM | The language model (gpt-4o-mini) that writes the answer from the retrieved records. |
