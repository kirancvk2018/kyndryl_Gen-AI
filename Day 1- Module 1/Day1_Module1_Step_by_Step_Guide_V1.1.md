# Day 1- Module 1

## Step-by-Step Guide: How to Run the Project on Windows

This guide is for consultants using a Windows virtual machine where Python is already installed. Follow the steps in order to prepare the project environment, install the required libraries, and run both Jupyter notebooks directly in Visual Studio Code (VS Code).

## Contents

1. Before you begin
2. What this project does (in plain words)
3. The flowchart at a glance
4. Part A: Verify Python and prepare VS Code
5. Part B: Create a workspace and activate it
6. Part C: Install the libraries
7. Part D: Open the project in VS Code and configure Jupyter
8. Part E: Run the Logistic Regression notebook in VS Code
9. Part F: Run the Linear Regression notebook in VS Code
10. Part G: Check your results
11. Part H: Close the notebooks and come back later
12. Troubleshooting
13. Important notes about the project files
14. Glossary (word list)

VS Code: Visual Studio Code, the editor used to open and run the project notebooks.

---

## 1. Before you begin

| What you need | Details |
|---|---|
| A Windows computer | Windows 10 or Windows 11. |
| An internet connection | Needed once, to download Python and the libraries (about 1 GB in total). |
| Free disk space | About 2 GB free on the C: drive. |
| Time | About 1 to 2 hours the first time, including downloads. Later runs take a few minutes. |
| The project folder | The folder named Day 1- Module 1. It must contain the two .ipynb notebooks and the two .csv data files. |
| A web browser | Microsoft Edge or Google Chrome. Jupyter opens the notebooks in your browser. |
| Administrator rights | Not normally needed. If an installer asks for permission, click Yes. |

> **Read this first:** Type the commands exactly as shown, including the quotation marks. Press Enter after each command. Wait for the prompt to come back before typing the next command.

---

## 2. What this project does (in plain words)

The project teaches Machine Learning, which means teaching a computer to find patterns in data and make predictions. It contains two Jupyter notebooks. A notebook is a document that mixes explanations with small pieces of Python code. Each piece of code is called a cell. You run each cell to see the results directly beneath it.

| Notebook | What it does | Data it uses |
|---|---|---|
| Module_01_Logistic_Regression_FIXED.ipynb | Predicts whether a server will FAIL (yes or no). This is a classification problem. | server_failure_logistic_regression_21000.csv |
| Enterprise_ML_Module_01.ipynb | Predicts a server's resource utilization score (a number). This is a regression problem. | server_resource_utilization_linear_regression_25000.csv |

You will run both notebooks. Start with the Logistic Regression notebook (Part E), then the Linear Regression notebook (Part F).

---

## 3. The flowchart at a glance

Read the flowchart from top to bottom. Yellow diamonds are checks: if the answer is NO, follow the red FIX box and return to the step it points to. Blue boxes are the steps you perform. The parts of this guide match the STEP labels.

Updated workflow: Verify existing Python → install VS Code extensions → create and activate the project virtual environment → install libraries → open the project folder in VS Code → select the virtual-environment kernel → run both notebooks → validate the results.

*Figure 1. Updated workflow for running the project in VS Code. The earlier Python-installation flowchart is not applicable to this VM setup.*

---

## 4. Part A: Verify Python and prepare VS Code

Python is already installed on the consultants' virtual machine. Do not install another copy. First verify that Windows can access the existing Python installation, then prepare VS Code for notebook execution.

**A1.** Open Windows PowerShell or the VS Code integrated terminal (Terminal > New Terminal). Type the following command and press Enter:

```powershell
python --version
```

You should see the Python version already installed on the virtual machine (for example, Python 3.12.x or another approved version). If the command is not recognised, try `py --version`. If neither command works, contact the VM administrator; do not install Python yourself.

> **If you see "Python was not found":** Windows may be using a shortcut to the Microsoft Store instead of Python. To turn it off: open Settings > Apps > Advanced app settings > App execution aliases. Switch OFF the entries named python.exe and python3.exe. Close PowerShell, open it again, and repeat step A7.

---

## 5. Part B: Create a workspace and activate it

A virtual environment is a private box that holds the libraries for this project, so they do not interfere with anything else on your computer. You will create it in a short folder, `C:\PyML`. The short name avoids a Windows problem with long folder paths that can break the installation.

**B1.** In the PowerShell window, create the folder:

```powershell
mkdir C:\PyML
```

If it says the folder already exists, that is fine.

**B2.** Create the virtual environment inside that folder:

```powershell
python -m venv C:\PyML\venv
```

No messages usually appear. Wait about 30 seconds until the prompt (`PS C:\...>`) returns.

**B3.** Activate (switch on) the environment:

```powershell
C:\PyML\venv\Scripts\Activate.ps1
```

When it works, the start of the line changes to `(venv)`. Everything you install from now on goes into this environment.

> **If you see "running scripts is disabled":** Type the following line, press Enter, type Y, and press Enter. Then repeat step B3.
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

> **Remember:** Every time you open a new PowerShell window, you must activate the environment again (step B3). You will know it is active when `(venv)` appears at the start of the line.

---

## 6. Part C: Install the libraries

A library is ready-made Python code written by others. The project uses several libraries for loading data, calculating statistics, building models, and drawing charts. Python installs them with a tool called pip.

**C1.** Make sure `(venv)` is shown at the start of the line. Then update the installer tool:

```powershell
python -m pip install --upgrade pip
```

**C2.** Install all the libraries in one command. This takes 5 to 15 minutes. Text will scroll past; that is normal. Wait until the prompt returns:

```powershell
python -m pip install pandas numpy matplotlib seaborn scikit-learn scipy joblib jupyter
```

The last line should say `Successfully installed` followed by a long list of names.

**C3.** Check that everything loads. Type this and press Enter:

```powershell
python -c "import pandas, sklearn, seaborn, joblib; print('All libraries ready')"
```

You should see: `All libraries ready`

> **If you see red ERROR text in step C2:** Do not panic. Check that the environment is active `(venv)` and that you are working inside `C:\PyML`, then run the same command again. If it still fails, see Troubleshooting, problem 4.

---

## 7. Part D: Open the project in VS Code and configure Jupyter

VS Code can open and run Jupyter notebooks directly in its editor. The Microsoft Python and Jupyter extensions provide notebook support.

**D1.** Open Visual Studio Code from the Windows Start menu.

**D2.** Install the Microsoft Python extension. In VS Code, select the Extensions icon on the left (or press Ctrl+Shift+X). Search for "Python", choose the extension published by Microsoft, and select Install.

**D3.** Install the Microsoft Jupyter extension in the same way. Search for "Jupyter", choose the extension published by Microsoft, and select Install. If VS Code prompts you to reload, select Reload.

**D4.** Open the project folder. Select File > Open Folder, browse to the Day 1- Module 1 folder, and select it. The folder must contain both .ipynb notebooks and both .csv data files.

**D5.** Open the integrated terminal using Terminal > New Terminal. Confirm that the terminal is PowerShell. Move to the project folder if needed, using: `cd "C:\Users\YourName\Downloads\Day 1- Module 1"`. Replace the example path with the actual folder path.

**D6.** Check that the four project files are visible by typing: `dir`

**D7.** Open `Module_01_Logistic_Regression_FIXED.ipynb` from the Explorer panel in VS Code. The notebook opens in the editor.

**D8.** Select the Python kernel. In the notebook toolbar, select Select Kernel (or the kernel name), choose Python Environments, and select the interpreter at `C:\PyML\venv\Scripts\python.exe` after completing Part B. If the virtual environment has not yet been created, complete Part B first and then return to this step.

**D9.** Confirm that the selected kernel is the project virtual environment. The notebook should show the selected Python environment in its top-right kernel area.

> **Keep the PowerShell window open.** Jupyter runs inside that window. If you close it, Jupyter stops and the notebooks stop working.
>
> **Not seeing the two notebook files on the Home page?** Jupyter shows the files of the folder you started it from, so you are in the wrong folder. In PowerShell press Ctrl + C, type y and press Enter, then repeat steps D2 and D4.

---

## 8. Part E: Run the Logistic Regression notebook in VS Code

A notebook is read from top to bottom. There are two kinds of boxes:

- **Text cells** contain explanations. Just read them. They have no `In [ ]` label.
- **Code cells** contain Python code and have a grey background with an `In [ ]` label on the left. You run these.

**E1.** In VS Code, click the first code cell. It is the first grey code box, and its first line is `import warnings`.

**E2.** Run the selected cell by clicking the Run icon shown beside the cell, or press Shift+Enter. The output appears directly below the cell.

**E3.** Run every code cell in order from top to bottom. This notebook has 24 code cells. Alternatively, use the notebook toolbar's Run All command. If a red error appears, stop and read Section 12 (Troubleshooting).

While a cell is running, its label shows `In [*]`. When it finishes, the label shows a number such as `In [5]`.

Alternative: use the notebook toolbar's Restart and Run All command to restart the kernel and execute all cells in order.

**E4.** Compare what you see with Part G, Table 2. Your numbers should match.

> **Hint:** Run the cells slowly and read each result. The confusion matrix cell and the feature importance cell are the most interesting to read.

---

## 9. Part F: Run the Linear Regression notebook in VS Code

**F1.** Open `Enterprise_ML_Module_01.ipynb` from the VS Code Explorer panel.

**F2.** Run its code cells one by one with Shift+Enter, from top to bottom. This notebook has 9 code cells. You can also use Run All.

**F3.** Check the results against Part G, Table 3.

---

## 10. Part G: Check your results

These are the numbers produced when the notebooks were run for testing. Small rounding differences are fine.

**Table 2. Logistic Regression notebook (classification)**

| Cell output | Expected value |
|---|---|
| Dataset Shape | 1032 rows × 17 columns |
| Server Failure Distribution | 680 failures (65.9%) and 352 healthy (34.1%) |
| Training / Testing set size | 825 samples (79.9%) and 207 samples (20.1%) |
| Test set Accuracy | 0.7295 (72.95%) |
| Test set Precision | 0.7597 (75.97%) |
| Test set Recall | 0.8603 (86.03%) |
| Test set F1-Score | 0.8069 |
| Test set ROC-AUC | 0.7635 |
| Test set R² Score | -0.2005 (a negative value is expected here; see Section 13) |
| Confusion matrix (test set) | [[34 37] [19 117]] (TN=34, FP=37, FN=19, TP=117) |
| Files saved at the end | logistic_regression_server_failure_model.pkl, feature_scaler.pkl, label_encoders.pkl |

**Table 3. Linear Regression notebook (regression)**

| Cell output | Expected value |
|---|---|
| Dataset loaded | 1,018 rows × 27 columns |
| Training / Testing set size | 814 samples and 204 samples |
| Features | 1059 (the server_id column is turned into many extra columns; see Section 13) |
| Training R² Score | 1.0000 |
| Testing R² Score | 0.6432 (64.32%) |
| Testing MAE | 4.1771 |
| Testing RMSE | 5.3568 |
| Top feature (largest coefficient) | server_id_SRV100303, coefficient about -16.86 |
| Files saved at the end | resource_utilization_model.pkl, feature_names.pkl |

> **Why do the numbers not match the text in the notebook?** Some explanations in the notebook and in the other documents were written before the data was finalised. Their claims (for example 81% accuracy, 25,000 rows, or R² of 0.70 to 0.90) do not match what the code produces. Trust the numbers your screen shows, and compare them with Tables 2 and 3.

---

## 11. Part H: Close the notebooks and come back later

**H1.** Save each notebook using Ctrl+S. Close the notebook editor tabs when finished.

**H2.** If VS Code shows a running kernel, use the notebook toolbar's kernel menu and select Shut Down Kernel.

**H3.** Close the VS Code integrated terminal when you have finished. If a process is still running, stop it with Ctrl+C.

**H4.** Next time, open the project folder in VS Code, open a terminal, activate the environment using `C:\PyML\venv\Scripts\Activate.ps1`, and open the required notebook. You do not need to reinstall Python, extensions, or libraries.

> **About the saved files:** Running the notebooks creates a few .pkl files in the project folder. These hold the trained models. They are expected. Do not delete them unless you want to start over; if you run the notebooks again, they are simply replaced.

---

## 12. Troubleshooting

Find what you see in the left column, then follow the fix in the right column.

| # | What you see | What to do |
|---|---|---|
| 1 | 'python' is not recognized as an internal or external command | Python was installed without the PATH tick. Uninstall Python from Settings > Apps, reinstall it (Part A), and tick Add python.exe to PATH. Then reopen PowerShell. |
| 2 | Python was not found; run without arguments to install from the Microsoft Store | Turn off the python.exe and python3.exe app execution aliases (see the note in Part A, step A7). Reopen PowerShell. |
| 3 | ...cannot be loaded because running scripts is disabled on this system | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, type Y, then activate again (step B3). |
| 4 | OSError, No such file or directory, or a message about Windows long path support during pip install | Make sure you created the environment in C:\PyML (Part B). If it still fails, ask your IT contact to turn on Windows long path support (registry setting `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem`, `LongPathsEnabled = 1`, then restart). Alternatively, install Anaconda, which includes Jupyter. |
| 5 | ModuleNotFoundError: No module named 'pandas' (or sklearn, seaborn, joblib) | The environment was not active when Jupyter started. Close Jupyter (Part H), activate the environment (B3), run the install command (C2), then start Jupyter again (D4). |
| 6 | FileNotFoundError ... server_failure_logistic_regression_21000.csv | The notebook is not in the same folder as the .csv file. Start Jupyter from the Day 1- Module 1 folder (Part D). Check the file name is spelled exactly the same. |
| (no number) | Notebook does not open in VS Code | Confirm the Microsoft Python and Jupyter extensions are installed and enabled. Reopen the .ipynb file in VS Code. Copy the line that starts with `http://localhost:8888/` from PowerShell and paste it into your browser. |
| (no number) | Kernel does not start | Use Select Kernel in the notebook toolbar and choose `C:\PyML\venv\Scripts\python.exe`. Confirm that the project virtual environment is active and that the libraries were installed into it. Jupyter will use another port. Copy the new `http://localhost:.../` line it prints, or close the other Jupyter window first. |
| 9 | A cell label stays `In [*]` for a long time | Wait one or two minutes. If it is still stuck, choose Kernel > Interrupt Kernel, then run the cell again. |
| 10 | Kernel Restarting or The kernel has died | Choose Kernel > Restart Kernel and Run All Cells. If it repeats, close Jupyter and restart it from an active environment. |
| 11 | Numbers look different from Part G | Check you ran the cells in order from the top. Use Kernel > Restart Kernel and Run All Cells. Small rounding differences are fine. |
| 12 | Strange characters such as `Ã×` or `RÂ²` appear | This is a text-display issue only. The numbers are still correct. Ignore it. |
| 13 | A chart does not appear | Make sure the cell above the chart has finished (it shows a number in its `In [ ]` label). Run the chart cell again. |

---

## 13. Important notes about the project files

The project was built as a learning exercise. While checking it, the following points were found. Knowing them will help you read the results correctly.

- **Row counts in file names and documents are wrong.** The logistic file is named 21000 but contains 1,032 servers. The regression file is named 25000 but contains 1,018 records. The code and the data are consistent; the names and the documents are not.
- **Linear Regression overfits.** The notebook turns server_id into 1,059 input columns, one per server. As a result the model memorises the training data (training R² = 1.0000) and generalises less well (testing R² = 0.6432). A better version would remove server_id before modelling. You do not need to fix this to complete the course.
- **Logistic Regression also uses server_id.** The notebook treats the server name as an input, which adds no real information about failure.
- **A negative R² is expected here.** For the classification model, R² does not describe the result well. A negative value means it is worse than simply predicting the average. Accuracy, precision, recall and ROC-AUC are the more useful measures.
- **Some documents describe slightly different data.** README.md, START_HERE.md, QUICKSTART.md and the instructor guide contain numbers and column names that do not match the data. Use this guide and Tables 2 and 3 as the reference.
- **Two notebooks have no code.** ML_Module_01_Complete.ipynb and Module_01_Introduction_to_ML_Linear_Regression.ipynb contain only text. You can read them, but there is nothing to run.

---

## 14. Glossary (word list)

| Word | Plain meaning |
|---|---|
| PowerShell | A Windows program where you type commands. Also called the command prompt. |
| Python | The programming language used by the project. |
| PATH | A list of places Windows searches for programs. Ticking Add python.exe to PATH lets you type `python` in PowerShell. |
| pip | The tool Python uses to download and install libraries. |
| Library | Ready-made code written by others, such as pandas (data tables) or scikit-learn (machine learning). |
| Virtual environment (venv) | A private, separate set of libraries for this project. Activate it before running anything. |
| Activate | Switch on the virtual environment. You know it is on when `(venv)` appears at the start of the line. |
| Jupyter notebook | A document with explanations and runnable code cells, opened in a web browser. |
| Cell | One block of text or code inside a notebook. |
| Kernel | The engine that runs the code cells in the background. Restart it if it gets stuck. |
| Shift + Enter | Keyboard shortcut to run the selected cell and move to the next one. |
| CSV file | A simple table of data saved as plain text, with values separated by commas. Opens in Excel too. |
| Model | The result of training: a set of learned rules that makes predictions on new data. |
| .pkl file | A saved model file that can be loaded later without training again. |
| R² (R-squared) | A score showing how much of the variation the model explains. Closer to 1 is better. |
| Accuracy / Precision / Recall | How often the model is right, how reliable its failure alarms are, and how many real failures it catches. |
