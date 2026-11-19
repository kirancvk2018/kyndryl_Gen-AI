# Day 3 Lab – Quickstart: Turn a Recording into Text

> Written for: participants with little or no programming experience.

This guide takes you from a ZIP file to a finished text transcript. You will mostly copy and paste short commands and press Shift + Enter to run the notebook cells.

**Before you start, you need:**
- Python version 3.10 or newer installed on your computer.
- An **OpenAI API key**. You create it on the OpenAI API platform. It is **separate from a ChatGPT subscription**, and API use is charged to your OpenAI API account. Keep the key private.
- Visual Studio Code (VS Code) or any other way to open a terminal. The steps below use VS Code.

---

### Step 1: Extract the ZIP file

Right-click the ZIP file and choose **Extract All** (Windows) or double-click it (Mac). You should now see a folder containing:

- `day3_lab_speech_to_text.ipynb` (the notebook)
- `day3_asr_requirements.txt`
- `DAY3_ASR_README.md`
- `DAY3_ASR_QUICKSTART.md` (this guide)
- `sample_incident_audio.wav` (the sample recording)

### Step 2: Open the extracted folder in VS Code or Jupyter Notebook

In VS Code, choose **File → Open Folder** and select the extracted folder.

### Step 3: Open the terminal

In VS Code, choose **Terminal → New Terminal**. Check that you are in the extracted folder: type `dir` (Windows) or `ls` (Mac) and press Enter. You should see `day3_asr_requirements.txt` in the list.

### Step 4: Install the dependencies

Type this command in the terminal and press Enter:

```text
pip install -r day3_asr_requirements.txt
```

Wait until the installation finishes. This can take a few minutes.

### Step 5: Configure the OPENAI_API_KEY environment variable

The notebook needs your API key. Choose one of the options below. Replace `your-key-here` with your own key. Do not share it with anyone.

**Option A – Windows, permanent (recommended):** in the terminal, type:

```text
setx OPENAI_API_KEY "your-key-here"
```

Then **close VS Code completely and open it again**, and open a new terminal. A permanent setting is only read by programs that start after it was made.

**Option B – Windows, this session only (PowerShell):**

```text
$env:OPENAI_API_KEY = "your-key-here"
```

**Option C – Mac or Linux, this session only:**

```text
export OPENAI_API_KEY="your-key-here"
```

**Option D – no setup:** skip this step. When the notebook reaches Section 3, it asks you to paste the key into a hidden box.

### Step 6: Start Jupyter

In the same terminal (in the extracted folder), type:

```text
jupyter notebook
```

Your web browser opens with a list of files. Keep the terminal window open while you work.

### Step 7: Open the notebook

In the browser, click **day3_lab_speech_to_text.ipynb**.

### Step 8: Execute the cells in order

Click inside a cell and press **Shift + Enter** to run it. Run every cell from the top, without skipping any. Each cell prints a message or a result below it.

If a cell shows a message such as `CONFIGURATION REQUIRED` or `FILE NOT FOUND`, read it and check the troubleshooting table in the last section of the notebook. Then run the notebook again from the top.

### Step 9: Listen to the sample audio

Find the cell in **Section 4 and 5** (it shows the file name and file size). Press the **play** button in the audio player under the cell. Listen to the recording so that you know what was said.

### Step 10: Execute the transcription code

Run the cell in **Section 6 and 7**. The notebook sends the recording to OpenAI. This can take up to a minute. The text appears under the cell with the heading `--- TRANSCRIPT ---`.

### Step 11: Review the generated transcript

Compare the transcript with what you heard. Check:
- Are the words correct?
- Are the numbers correct (10:15 AM, 95 percent, 120 users, 30 minutes)?
- Are the technical terms correct (CPU utilization, database, latency)?

Then run the cells in **Section 11 and 12** to transcribe the recording again with extra hints, and compare the two results.

### Step 12: Review the saved file in the transcripts folder

The notebook creates a folder called **transcripts** in the extracted folder. Open it and double-click a file, such as `incident_transcript.txt`, to open it in Notepad or another text editor.

---

## Optional: Transcribe your own recording

1. Copy your audio file into the extracted folder. Supported types include MP3, WAV, M4A, MP4, FLAC, OGG and WebM. The file must be **25 MB or smaller**.
2. In the notebook, find the cell in **Section 13 and 14** that contains `CUSTOM_AUDIO_FILE = "your_audio_file.wav"`.
3. Change the file name to your file's name, keeping the quotation marks. For example: `CUSTOM_AUDIO_FILE = "my_meeting.mp3"`.
4. Press Shift + Enter to run the cell.
5. Your transcript appears on screen and is saved in the **transcripts** folder with a unique name. Earlier transcripts are not overwritten.

---

## Stopping the lab

When you have finished, go to the terminal and press **Ctrl + C**, then type `y` and press Enter if asked. This stops Jupyter.

## If something goes wrong

Read the message shown in the notebook first. The troubleshooting table in the last section of the notebook explains the most common messages. The README document (`DAY3_ASR_README.md`) has more detail.
