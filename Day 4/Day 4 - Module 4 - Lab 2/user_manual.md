# User Manual

**Day 3 Practical Lab: Speech-to-Text Transcription using the OpenAI API**

| Item | Details |
| --- | --- |
| Module | Day 3 – Module 03: Introduction to Large Language Models |
| Topic | Task-Based Text AI LLMs – Automatic Speech Recognition (ASR) |
| Notebook to run | day3_lab_speech_to_text.ipynb |
| Document version | 1.0 – 17 November 2026 |
| Scenario | Simulated IT infrastructure incident update for training. It contains no real incident, customer or personal data. |

## 1. About this manual

This manual gives step-by-step instructions to set up and run the lab notebook. In the lab you convert a recorded IT infrastructure incident update into text with the OpenAI transcription model `gpt-transcribe`. You then compare results with and without hints, save the transcripts, and process a recording of your own.

Follow the steps in order. Each step says what to do and what you should see. The instructions use the browser-based Jupyter Notebook, which is the path that has been tested.

## 2. Before you start

| Requirement | Details |
| --- | --- |
| Computer | Windows, macOS or Linux, with internet access |
| Python | Version 3.10 or newer |
| OpenAI API key | Created on the OpenAI API platform. It is separate from a ChatGPT subscription. API use is billed to your OpenAI API account. |
| Lab package | The ZIP file DAY3_Speech_to_Text_OpenAI_API_Lab.zip, extracted to a folder |
| Tools | A web browser, a terminal, and Visual Studio Code (VS Code) if you want to use it to open the folder |

## 3. Files in the lab package

| File | Purpose |
| --- | --- |
| day3_lab_speech_to_text.ipynb | The notebook you run, step by step |
| day3_asr_requirements.txt | The list of Python packages to install |
| DAY3_ASR_README.md | Technical reference for facilitators |
| DAY3_ASR_QUICKSTART.md | Short guide for participants |
| sample_incident_audio.wav | The sample recording, about 49 seconds long |
| transcripts (folder) | Created automatically when the notebook runs. Holds the saved transcripts. |

## 4. Part A – One-time setup

### Step 1 – Extract the ZIP file

- Windows: right-click the ZIP file and choose **Extract All**.
- Mac: double-click the ZIP file.

You should now have a folder containing these five files: day3_lab_speech_to_text.ipynb, day3_asr_requirements.txt, DAY3_ASR_README.md, DAY3_ASR_QUICKSTART.md and sample_incident_audio.wav. Keep them all in the same folder. The notebook needs the sample recording in that folder.

### Step 2 – Check that Python 3.10 or newer is installed

- On Windows, press the Start key, type PowerShell and press Enter to open a terminal.
- Type the command below and press Enter.

```
python --version
```

**Expected result:** a line such as `Python 3.11.4`. Any version 3.10 or higher is fine.

> **Note:** If the command reports that Python was not found, or it opens the Microsoft Store, try `py --version`. If that does not work either, install Python 3.10 or newer from python.org. On Windows, tick **Add python.exe to PATH** during installation, then open a new terminal.

### Step 3 – Create your OpenAI API key

- Go to the OpenAI API platform at platform.openai.com and sign in with your OpenAI account.
- Open the API keys page and choose the option to create a new secret key.
- Copy the key straight away and store it somewhere private, such as a password manager. Some platforms show a key only once.
- Check that billing is set up for your API account. Each transcription request is charged to that account.

> **Warning:** The API key is different from a ChatGPT subscription. Never paste the key into a notebook cell, a document, an email or a chat.

### Step 4 – Open the lab folder in VS Code (optional)

- Open Visual Studio Code.
- Choose **File → Open Folder** and select the folder you extracted in Step 1.
- The Explorer panel should now list the five lab files.

If you do not use VS Code, open File Explorer, go to the lab folder, click the address bar, type `powershell` and press Enter. A terminal opens in that folder, and you can continue with Step 5.

### Step 5 – Open a terminal in the lab folder

- In VS Code, choose **Terminal → New Terminal**.
- Check the folder by typing the command below and pressing Enter. On Mac or Linux, use `ls` instead.

```
dir
```

You should see day3_asr_requirements.txt and day3_lab_speech_to_text.ipynb in the list. If you do not, the terminal is in the wrong folder. Use `cd` followed by the folder path, for example `cd "C:\Lab\DAY3_ASR_LAB"`, then run `dir` again.

### Step 6 – Install the required packages

- Type the command below and press Enter. Wait until it finishes. This can take a few minutes.

```
pip install -r day3_asr_requirements.txt
```

**Expected result:** the last line says `Successfully installed` and lists `openai` with version 2.54.0 or newer. If the message says that `pip` is not recognised, use this command instead: `python -m pip install -r day3_asr_requirements.txt`

You only need to repeat this step if you change Python or see a missing-module error later.

### Step 7 – Choose how the notebook gets your API key

Choose one option. You do not need to create a `.env` file, and the notebook never saves your key.

| Option | When to use it | What to do |
| --- | --- | --- |
| A. Enter the key when asked (simplest) | You want no setup. You enter the key once per run. | Do nothing now. In Step 12 the notebook asks you to paste the key into a hidden box. |
| B. Permanent Windows setting | You use Windows and want the key remembered. | Type `setx OPENAI_API_KEY "your-key-here"`. Then close VS Code and all terminals completely, and reopen them. Repeat Step 5 and Step 8 in the new terminal. |
| C. This terminal only | Mac, Linux, or a one-off session on Windows. | Windows PowerShell: `$env:OPENAI_API_KEY = "your-key-here"`. Mac or Linux: `export OPENAI_API_KEY="your-key-here"`. Then run Step 8 in this same terminal. |

Replace `your-key-here` with your own key and keep the quotation marks.

> **Warning:** Do not show the terminal on a shared screen while your key is visible. If you used Option B, you can remove the key later (see Step 23).

## 5. Part B – Running the notebook

### Step 8 – Start Jupyter Notebook

- In the terminal, type the command below and press Enter.

```
jupyter notebook
```

- Your web browser opens a page that lists the lab files. If the browser does not open, copy the address shown in the terminal (it starts with `http://localhost:8888`) into your browser.
- Keep the terminal open while you work. Closing it stops Jupyter.

### Step 9 – Open the notebook

- In the browser, click **day3_lab_speech_to_text.ipynb**.
- The notebook opens with the title “Day 3 – Practical Lab: Speech-to-Text Transcription using OpenAI API”.

### Step 10 – Learn how to run a cell

- The notebook is made of cells. Text cells hold explanations and do not run. Code cells hold Python code.
- To run a code cell, click inside it and press **Shift + Enter**. The cell runs and the next cell is selected.
- While a cell is running, its number shows an asterisk, `[*]`. When it finishes, the number changes, for example `[4]`.
- Run the code cells in order, from top to bottom. Do not skip cells, because later cells use values created by earlier ones.
- If a cell reports a problem, read the message, fix the cause (see section 9 of this manual) and run that cell again.

### Step 11 – Run the Section 2 cell: environment setup

- Click the code cell under **Section 2 – Environment Setup** and press Shift + Enter.

**Expected result:** `Environment ready.`, then the OpenAI library version (2.54.0 or newer) and the full path of the transcripts folder. A folder called `transcripts` now exists in the lab folder.

### Step 12 – Run the Section 3 cell: API configuration

- Click the code cell under **Section 3 – OpenAI API Configuration** and press Shift + Enter.
- If you chose Option B or C, the notebook prints `OpenAI client is ready. The API key is hidden for safety.`
- If you chose Option A, the notebook prints `OPENAI_API_KEY is not set in this environment.` A box appears with the text `Paste your OpenAI API key and press Enter (input is hidden):`. Paste your key and press Enter. Nothing appears on screen while you paste. This is normal.

If you see `CONFIGURATION REQUIRED: no API key was provided.`, no key was entered. Run this cell again.

### Step 13 – Check and listen to the sample recording (Sections 4 and 5)

- Run the code cell under **Sections 4 and 5**.
- **Expected result:** `File name : sample_incident_audio.wav`, `Format : .wav`, a file size of about 2.05 MB (limit 25 MB), `File check passed.`, and an audio player.
- Press the play button and listen to the whole recording, which lasts about 49 seconds.
- Note the key facts, which you will check the transcript against: the time (about 10:15 AM), the CPU utilization (95 percent), the number of users (about 120) and the next update (30 minutes).

### Step 14 – Run the first transcription (Sections 6 and 7)

- Run the code cell under **Sections 6 and 7**.
- The notebook prints `Sending the recording to OpenAI. This can take up to a minute...`. Wait. The cell shows `[*]` while it works.
- **Expected result:** a heading `--- TRANSCRIPT ---`, followed by the spoken text.

> **Note:** This cell sends one request to OpenAI. Small differences in punctuation or format are normal. For example, the transcript may write `10:15 a.m.` instead of `10:15 AM`.

### Step 15 – Review the transcript and save it (Sections 8 and 9)

- Run the code cell under **Section 8**. It shows the character count (about 700), the word count (close to 99, the number of words in the script) and the transcript as a quote.
- Run the code cell under **Section 9**. It saves the transcript to `transcripts\incident_transcript.txt`, then reads the file back and shows its contents.
- Check the transcript against your notes from Step 13. Are the numbers correct? Are the technical terms correct (CPU utilization, database, latency)? Do the sentences read in the right order?

### Step 16 – Review the context settings (Section 10)

- Run the code cell under **Section 10** without changing anything for your first run.
- **Expected result:** `Context, keyword and language settings are ready.`, `Number of keywords: 8` and `Language option: {'languages': ['en']}`.
- The three settings are `TRANSCRIPTION_CONTEXT` (a description of the recording), `TECHNICAL_KEYWORDS` (terms you expect to hear) and `LANGUAGE_CODE` (`en` means English). Change them only when you want to test how hints affect the result.

### Step 17 – Transcribe with hints and compare the results (Sections 11 and 12)

- Run the code cell under **Section 11**. It sends the same recording together with the hints.
- **Expected result:** a heading `--- CONTEXT-ASSISTED TRANSCRIPT ---`, the text, and `Saved to:` followed by the file `incident_transcript_with_context.txt`. This cell sends one request to OpenAI.
- Run the code cell under **Section 12**. It shows transcript A (no hints) and transcript B (with hints), each with its word count.
- Compare A and B using this checklist:
- **Technical terminology:** are CPU utilization, database failover and network latency written correctly?
- **Recognised words:** are any words replaced by similar-sounding words?
- **Punctuation and sentence structure:** do the sentences read clearly?
- **Words that were never spoken:** the sample does not mention PostgreSQL, Kubernetes, VPN, DNS or firewall. If one of these appears, the hints added a word that was not spoken.

Hints do not always help. Write down any differences you notice.

### Step 18 – Run the custom-recording cell without changes (Sections 13 and 14)

- Run the code cell under **Sections 13 and 14** without changing anything.
- **Expected result:** `FILE NOT FOUND: 'your_audio_file.wav'`. This is correct until you name your own recording (see Part D).

### Step 19 – Run the complete workflow (Section 15)

- Run the code cell under **Section 15**. The cell checks the file, transcribes it, shows the transcript, saves it and returns the text.
- **Expected result:** `--- TRANSCRIPT ---`, the text, and `Saved to:` followed by a file called `sample_incident_audio_workflow_<date and time>.txt`.

> **Note:** This cell sends one more request to OpenAI for the sample recording.

### Step 20 – Read the knowledge check and summary (Sections 16 and 17)

These are text cells with no code to run. Read the five questions and their answers, the lab summary and the troubleshooting table at the end of the notebook.

## 6. Part C – After the lab

### Step 21 – Find your transcripts

- In the lab folder, open the `transcripts` folder.
- You may see these files: `incident_transcript.txt` (Section 9), `incident_transcript_with_context.txt` (Section 11), `sample_incident_audio_workflow_<date and time>.txt` (Section 15) and `custom_<your file name>_<date and time>.txt` (your own recording).
- Open a file in Notepad or any text editor.

> **Note:** Running Section 9 or Section 11 again replaces its file. Other transcript files are never overwritten.

### Step 22 – Stop Jupyter

- Go to the terminal where Jupyter is running.
- Press **Ctrl + C**. If Jupyter asks whether to shut down the server, type `y` and press Enter.
- Close the browser tab.

### Step 23 – Remove the key from Windows (only if you used Option B)

- In the Windows search box, type **Edit environment variables for your account** and open it.
- Select **OPENAI_API_KEY** in the list, choose **Delete**, then choose **OK**.

Option A stores nothing on your computer. Option C lasts only until you close the terminal, so it needs no clean-up.

## 7. Part D – Process your own recording

You can transcribe any supported recording of your own. Your transcript is saved with a unique name, so earlier transcripts are kept.

### Step 24 – Put your recording in the lab folder

- Copy your audio file into the same folder as the notebook.
- Supported formats: FLAC, MP3, MP4, MPEG, MPGA, M4A, OGG, WAV and WebM.
- The file must be 25 MB or smaller. For longer recordings, compress the file (for example to MP3) or split it into shorter files.

### Step 25 – Change the file name in the notebook

- In the notebook, find the code cell under **Sections 13 and 14**. It contains `CUSTOM_AUDIO_FILE = "your_audio_file.wav"`.
- Replace `your_audio_file.wav` with your file name and keep the quotation marks, for example:

```
CUSTOM_AUDIO_FILE = "my_meeting.mp3"
```

### Step 26 – Run the cell

- Click the cell and press Shift + Enter.
- **Expected result:** your transcript appears under `--- YOUR TRANSCRIPT ---`, followed by `Saved to:` and a file such as `custom_my_meeting_<date and time>.txt`.
- Each run creates a new file. This cell sends one request to OpenAI.

### Step 27 – Set the language (optional)

- The language is set in the code cell under **Section 10** (`LANGUAGE_CODE`). `en` means English.
- Change it to another code, such as `de` (German) or `fr` (French), only if your recording is in that language. Leave it empty (`""`) to let the model detect the language.
- After changing the setting, run the Section 10 cell again, then run the Section 13 and 14 cell.

## 8. Expected results by code cell

The notebook has 11 code cells. The table lists them in order.

| Code cell | Section | Sends a request to OpenAI? | What you should see |
| --- | --- | --- | --- |
| 1 | 2 – Environment setup | No | `Environment ready.`, the library version and the transcripts folder path |
| 2 | 3 – API configuration | No | `OpenAI client is ready`, or a configuration message |
| 3 | 4–5 – Audio check and player | No | File details, `File check passed.` and a play button |
| 4 | 6–7 – First transcription | Yes (one request) | `--- TRANSCRIPT ---` and the spoken text |
| 5 | 8 – Output and counts | No | Character count, word count and the transcript as a quote |
| 6 | 9 – Save and read back | No | `Saved to:` and the saved text |
| 7 | 10 – Settings | No | `Context, keyword and language settings are ready.`, 8 keywords, language `en` |
| 8 | 11 – Transcription with hints | Yes (one request) | `--- CONTEXT-ASSISTED TRANSCRIPT ---` and a saved file |
| 9 | 12 – Comparison | No | Transcripts A and B with their word counts |
| 10 | 13–14 – Your own recording | Only if the file is found | `FILE NOT FOUND` until you name your file; then your transcript |
| 11 | 15 – Complete workflow | Yes (one request) | The transcript, a saved file and the returned text |

Sections 1, 16 and 17 are text only and have no code cells.

## 9. Troubleshooting

Find the message or symptom in the first column. The notebook shows short messages by design and does not display full technical error traces.

| Message or symptom | What it means | What to do |
| --- | --- | --- |
| `python` is not recognised, or the Microsoft Store opens | Python is not installed, or it is not on the PATH | Try `py --version`. Otherwise install Python 3.10 or newer from python.org and tick **Add python.exe to PATH**. |
| `pip` is not recognised | pip is not on the PATH | Use `python -m pip install -r day3_asr_requirements.txt`. |
| `No module named 'openai'` in a cell | The notebook is using a different Python from the one where the packages were installed | Run Step 6 again in the same terminal, then start Jupyter from that terminal (Step 8). |
| `CONFIGURATION REQUIRED: no API key was provided.` | No key was entered | Complete Step 7, then run the Section 3 cell again (Step 12). |
| `The API key was rejected` | The key is wrong, has extra spaces, has been revoked, or belongs to another account | Copy the key again without spaces. If it still fails, create a new key (Step 3) and repeat Step 7. |
| `Could not reach OpenAI` | No internet connection, or a firewall or proxy blocks the request | Check your connection and run the cell again. On a company network, ask IT whether OpenAI access is allowed. |
| `OpenAI returned an error (status …)` | OpenAI refused the request, for example because of usage limits or a temporary problem | Read the message. Wait a few minutes and run the cell again. Check usage and billing on your OpenAI API account. |
| `No API key available. Complete Section 3 first.` | The Section 3 cell has not run successfully | Run the Section 3 cell (Step 12), then run the cells again in order. |
| `No transcript yet`, `Nothing to save yet` or `Both transcripts are needed` | A transcription has not produced a result yet | Run the cells in order: Step 14 first, then Step 17. |
| `FILE NOT FOUND` | The file is not in the lab folder, or its name is spelled differently | Check the spelling and the extension, and keep the file in the same folder as the notebook. |
| `UNSUPPORTED FORMAT` | The file type is not supported | Convert the recording to MP3 or WAV. |
| `FILE TOO LARGE` | The file is larger than 25 MB | Compress the file or split it into shorter files. |
| A cell shows `[*]` for several minutes | The request is taking a long time or has stopped | In the menu, choose **Kernel → Interrupt**, then run the cell again. If it keeps happening, check your internet connection. |
| The browser does not open after `jupyter notebook` | The browser was not started automatically | Copy the address that starts with `http://localhost:8888` from the terminal into your browser. |
| The notebook cannot find `sample_incident_audio.wav` | The notebook and the audio file are in different folders | Put both in the lab folder, then start Jupyter from that folder (Step 8). |
| The transcript differs from the script | Speech recognition is not perfect | Small differences are normal. Check the transcript against what you heard. Report large or repeated errors to your facilitator. |

## 10. Safety and cost notes

- **Keep your API key private.** Anyone who has the key can use your OpenAI API account, and the usage is charged to you. If you think someone else has seen the key, revoke it on the OpenAI API platform and create a new one.
- **Costs.** Each transcription request is billed to your OpenAI API account. For the sample recording, the lab sends three requests (Steps 14, 17 and 19). Each of your own recordings adds one request (Step 26). Check your usage on the OpenAI platform.
- **Sensitive recordings.** The sample is a computer-generated training recording. Do not send recordings that contain confidential, personal or customer information unless your organisation has approved their use with the OpenAI API.
- **Transcripts.** Store transcripts in the lab folder or another approved location, and do not share transcripts of real calls outside your organisation.

## 11. Glossary

| Term | Meaning |
| --- | --- |
| API | Application Programming Interface: a way for one program to ask another program for a service. Here, it sends audio to OpenAI and receives text back. |
| API key | A private code that identifies your OpenAI API account. |
| Automatic Speech Recognition (ASR) | Technology that converts spoken words into written text. |
| Cell | One block in a Jupyter notebook. It holds either text or Python code. |
| Contextual hints | Extra information (the prompt, keywords and language) that helps the model recognise technical terms. |
| Environment variable | A named setting stored by the operating system. Here it is OPENAI_API_KEY, which the notebook reads. |
| Jupyter Notebook | A browser-based tool that runs code cells and shows the results in one document. |
| Terminal | A window where you type commands. In VS Code, choose Terminal → New Terminal. |
| Transcript | The text produced from an audio recording. |
