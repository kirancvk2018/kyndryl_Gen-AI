# Text-to-Speech Assistant for IT Infrastructure

Module 4, Lab 1 - User Guide (step by step)

Written for: participants with basic computer skills who may have little or no Python experience.

## Before you start

Make sure you have the following:

- A computer with Python 3.9 or newer installed. To check, open a terminal and type python --version, then press Enter.

- A valid OpenAI API key that can use the Text-to-Speech service. Keep it private.

- An internet connection. The audio is created by the OpenAI service, so the lab cannot make audio offline.

- The lab package: MODULE4_LAB1_Text_to_Speech_Assistant.zip.

*Note: You do not need to write any code. You will run commands that are given to you, and run the notebook one cell at a time.*

### Words used in this guide

| Word | What it means |
| --- | --- |
| Terminal | A window where you type commands. On Windows it is called PowerShell or Command Prompt. On a Mac it is called Terminal. |
| Notebook | A web page with boxes called cells. Some cells explain things, and some cells run actions when you press Shift + Enter. |
| Cell | One box in the notebook. A grey or text cell explains. A cell with a number and code runs an action. |
| API key | A secret code that proves your OpenAI account is allowed to create audio. Treat it like a password. |
| MP3 | A standard audio file that most computers and phones can play. |
| Environment variable | A named setting stored by your computer for a session. The lab reads the setting OPENAI_API_KEY. |

## Part 1: Set up the lab (one-time steps)

### Step 1: Extract the project ZIP

- Find the file MODULE4_LAB1_Text_to_Speech_Assistant.zip.

- Right-click the file and choose Extract All (Windows) or double-click it (Mac).

- Choose a location you can find again, such as Documents.

- You should now see a folder named MODULE4_LAB1 with four files inside.

### Step 2: Open the MODULE4_LAB1 folder

Use either option:

- In VS Code: choose File > Open Folder, then select MODULE4_LAB1.

- In File Explorer: double-click the MODULE4_LAB1 folder so it is open on your screen.

### Step 3: Open a terminal in the folder

- In VS Code: choose Terminal > New Terminal. The terminal opens in the right folder.

- On Windows (without VS Code): click the address bar at the top of the folder window, type powershell, and press Enter.

- On a Mac: open Terminal, type cd followed by a space, drag the MODULE4_LAB1 folder into the window, and press Enter.

### Step 4: Install the required tools

Type this command in the terminal and press Enter:

```
pip install -r lab1_m4_requirements.txt
```

- Wait until the text stops moving and the cursor returns.

- Red error text means something went wrong. Check the Troubleshooting section at the end of this guide.

*Note: If pip is not recognised on Windows, try typing py -m pip install -r lab1_m4_requirements.txt instead.*

### Step 5: Give the notebook your OpenAI API key

Your key is secret. Do not paste it into the notebook, an email, or a shared document.

Choose one option.

Option A (recommended): type the command for your system in the SAME terminal you will use in Step 6.

Windows PowerShell:

```
$env:OPENAI_API_KEY = "paste-your-key-here"
```

macOS or Linux:

```
export OPENAI_API_KEY="paste-your-key-here"
```

- Replace paste-your-key-here with your real key. Keep the quotation marks.

- The key lasts only while this terminal window is open.

Option B: create a file named .env in the MODULE4_LAB1 folder.

- The file must contain one line: OPENAI_API_KEY=paste-your-key-here

- On Windows, make sure the file is not saved as .env.txt.

## Part 2: Run the notebook

### Step 6: Start Jupyter

In the same terminal, type this command and press Enter:

```
jupyter notebook
```

- Your web browser opens a page listing the files in the folder.

- If the browser does not open, copy the address that starts with http://localhost from the terminal and paste it into your browser.

- Keep the terminal window open while you work. Closing it stops Jupyter.

### Step 7: Open the notebook

- In the browser, click module4_lab1_text_to_speech.ipynb.

- The notebook opens with the title Module 4, Lab 1: Text-to-Speech Assistant for IT Infrastructure.

### Step 8: Run the cells in order

- Click inside a cell.

- Press Shift + Enter to run it. The cursor moves to the next cell.

- Run the cells from the top. Do not skip any cells.

- Read each text cell before running the code cell below it. It explains what will happen.

- Wait for each cell to finish. A number in square brackets, such as [3], shows that it ran. An asterisk, [*], means it is still running.

Quick reference: which cells create audio?

| Cell | What it does | Creates audio? |
| --- | --- | --- |
| 3 | Sets up folders and checks your API key | No |
| 5, 7, 9, 11, 17 | Loads the sample messages and defines the functions | No |
| 13 | Creates an accessibility version of the maintenance notice | Yes (1 file) |
| 15 | Creates audio from a sample analysis text | Yes (1 file) |
| 19 | Example 1: critical database alert | Yes (1 file) |
| 21 | Example 2: server status update | Yes (1 file) |
| 23 | Example 3: slower maintenance notice | Yes (1 file) |
| 25 | Example 4: same security message at three speeds | Yes (3 files) |
| 27 | Lists your audio files and the log, and plays one file | No |
| 29 | Complete workflow for the critical alert | Yes (about 5 files) |
| 31 | Compares three voices for the same message | Yes (3 files) |

*Note: Each audio cell makes a small charge to your OpenAI account. Run only the cells you need.*

### Step 9: Listen to the audio

- Under the code of an audio cell, an audio player appears.

- Press the play button to listen.

- If no player appears, check that the cell finished and that the volume is on.

- To hide the players, change PLAY_AUDIO = True to PLAY_AUDIO = False in Cell 3, then run Cell 3 again.

### Step 10: Review your files

- Audio files are saved in the audio_output folder inside MODULE4_LAB1. Open them with any media player.

- The log is saved as tts_logs/audio_generation_log.csv. Open it with Excel or Notepad. It lists the time, scenario, voice, speed, model and file name for each file.

- Each new run adds rows to the log. Earlier rows are kept.

## Part 3: Make changes (optional)

You can change a few settings without writing code. Change only the value after the equals sign, then run the cell again.

| Setting | Cell | Example change | What it controls |
| --- | --- | --- | --- |
| PLAY_AUDIO | 3 | True to False | Shows or hides audio players |
| SELECTED_VOICE | 9 | 'alloy' to 'nova' | Voice for your own tests |
| ALERT_VOICE_MAP | 11 | 'critical_alert': 'alloy' | Voice for each sample alert |
| STATUS_VOICE | 21 | 'echo' to 'shimmer' | Voice for the status update |
| MAINTENANCE_SPEED | 23 | 0.8 to 0.7 | Speed for the accessibility example (0.25 to 4.0) |
| SPEED_VALUES | 25 | [0.75, 1.0, 1.25] | Speeds used in the speed variations |
| SELECTED_FILE_NUMBER | 27 | 1 to 3 | Which listed file to play |
| VOICES_TO_COMPARE | 31 | ['alloy', 'echo', 'nova'] | Voices used in the comparison |

Allowed voices: alloy, echo, fable, onyx, nova, shimmer.

Allowed speeds: from 0.25 (slowest) to 4.0 (fastest). 1.0 is normal speed.

### Starting over

- To run everything again from the beginning, choose Kernel > Restart & Run All from the notebook menu.

- Restart & Run All creates new audio and new log rows, so it uses your account credits again.

### Stopping the lab

- Save the notebook with Ctrl + S (Command + S on a Mac).

- Click the terminal where Jupyter is running and press Ctrl + C, then type y and press Enter.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| 'pip' is not recognised | Use py -m pip install -r lab1_m4_requirements.txt on Windows, or check that Python was installed with the option to add it to PATH. |
| OPENAI_API_KEY is not configured | The key is not set in this terminal. Repeat Step 5 in the same terminal, then restart Jupyter (Step 6). |
| The OpenAI API key was rejected (error 401) | The key is wrong, expired or revoked. Check that you pasted the whole key, without spaces. |
| Audio generation failed | Check your internet connection. Then read the details in the red message and run the cell again. |
| Invalid voice | Use one of: alloy, echo, fable, onyx, nova, shimmer. |
| Unsupported speed | Use a number from 0.25 to 4.0. |
| NameError: name '...' is not defined | A cell was run out of order. Choose Kernel > Restart & Run All, or run the cells again from Cell 3. |
| No sound from the player | Check the volume and the speaker or headphone selection. The MP3 file is still saved in audio_output. |
| ModuleNotFoundError | Run Step 4 again, then restart Jupyter. |
| The log file is empty or missing | Run at least one audio cell. The log is created the first time audio is made. |
| Jupyter does not open in the browser | Copy the http://localhost address from the terminal into your browser. |

## Checklist

- I extracted the ZIP and opened the MODULE4_LAB1 folder.

- I installed the requirements with pip.

- I set OPENAI_API_KEY in the same terminal (or created a .env file).

- I started Jupyter and opened module4_lab1_text_to_speech.ipynb.

- I ran the cells from the top, in order.

- I listened to at least one audio file.

- I checked audio_output and tts_logs.
