# Module 3, Lab 2: IT Infrastructure Image Analyzer

A simple Streamlit web app. Upload an infrastructure image, pick an analysis category, and let OpenAI GPT-4o Vision describe the components, potential issues and recommendations. Download the result as a TXT file.

---

## 1. Lab Overview

This lab shows how to put a multimodal Generative AI model behind a small web interface. The whole app is one Python file, with no database and no multi-page navigation, so you can read and explain all of it in one session.

## 2. Learning Objectives

By the end of this lab you will be able to:

1. Build a single-page web app with Streamlit.
2. Upload, validate and preview an image with Pillow.
3. Send an image and a text prompt to the OpenAI GPT-4o Vision API.
4. Change the analysis behaviour by editing prompts.
5. Offer a file download from a Streamlit app.
6. Add basic file logging with Python's `logging` module.

## 3. Prerequisites

- Python 3.10 or newer
- Basic Python (variables, functions, dictionaries, `if` statements)
- An OpenAI API key with access to GPT-4o
- An infrastructure image (JPG, JPEG, PNG or WEBP), such as a server rack photo, a monitoring dashboard screenshot, a network diagram or an error log screenshot

## 4. Technology Stack

| Package | Purpose |
|---------|---------|
| `streamlit` | Web user interface |
| `openai` | Official OpenAI Python SDK (GPT-4o Vision) |
| `pillow` | Image validation and preview |
| `python-dotenv` | Loads `OPENAI_API_KEY` from the `.env` file |

Logging uses Python's built-in `logging` module, so it needs no extra package.

## 5. Project Structure

```text
Module3 - Lab 2/
├── module3_lab2_image_app.py   # The complete Streamlit application
├── requirements.txt            # The four Python dependencies
├── README.md                   # This guide
├── .env.example                # API key template (copy to .env)
└── .gitignore                  # Keeps secrets, virtual environments and logs out of git
```

After the app runs, `app.log` appears in the same folder. You do not need to create it.

## 6. Setup Instructions

**Step 1: Create a virtual environment** (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`.

If PowerShell reports that scripts are disabled, run this once and try again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 3: Configure your API key**

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Open `.env` and replace the placeholder with your own key:

```env
OPENAI_API_KEY=sk-your-real-key
```

Notes:
- Never share your `.env` file, paste the key into the code, or commit it to git. `.gitignore` already excludes it.
- If you think a key was exposed, delete it in the OpenAI dashboard and create a new one.

## 7. Run the Application

**Step 4: Run the app**

```bash
streamlit run module3_lab2_image_app.py
```

**Step 5: Open the app**

Streamlit opens your browser automatically. If it does not, go to:

```text
http://localhost:8501
```

## 8. Application Workflow

**Step 6: Perform an image analysis**

1. **Upload** an infrastructure image (JPG, JPEG, PNG or WEBP, maximum 20 MB). The app shows a preview, the filename, the dimensions and the file size.
2. **Select** an analysis category from the dropdown.
3. **Click** *Analyze Image*. A spinner shows while GPT-4o works. Each click makes exactly one API call.
4. **Review** the result, organised into four sections: Analysis Summary, Key Observations, Potential Issues and Recommendations.
5. **Download** the result with *Download Analysis (TXT)*.

Results are kept only in the open browser session. Refreshing the page or restarting the app clears them. Nothing is saved to a database.

## 9. The Five Analysis Categories

| Category | Use it for | The model focuses on |
|----------|-----------|----------------------|
| **General** | Any infrastructure image | Components, issues, overall condition |
| **Server Rack** | Photos of racks and data-centre hardware | Equipment, cable management, power, cooling |
| **Dashboard** | Monitoring dashboard screenshots | Metrics, trends, alerts, anomalies |
| **Network** | Network diagrams and equipment | Connectivity, topology, bottlenecks, failure points |
| **Error Log** | Error messages and log screenshots | Error details, severity, causes, troubleshooting |

Every category uses the same four-section output. The model is told to separate what it can see from what it assumes, and not to claim certainty about details it cannot read.

## 10. Code Explanation

`module3_lab2_image_app.py` is organised in seven numbered sections:

| # | Section | What it does |
|---|---------|--------------|
| 1 | Environment configuration | Loads `.env`, sets constants (model name, 20 MB limit, allowed formats) |
| 2 | Logging configuration | Writes INFO-level events to `app.log` |
| 3 | Page configuration | Sets the browser tab title and icon |
| 4 | Analysis prompts | One prompt per category in `ANALYSIS_PROMPTS`, plus the shared `OUTPUT_RULES` |
| 5 | `validate_image()` | Checks extension, size and real image content with Pillow |
| 6 | `analyze_image_with_openai()` | Makes the single GPT-4o call and turns API errors into friendly messages |
| 7 | `main()` | Builds the Streamlit page: upload, preview, category, button, results, download |

Points worth discussing in class:

- **Session-only results.** The result is stored in `st.session_state`. Streamlit re-runs the script on every click, so the result must be stored to stay on screen when the download button is clicked.
- **Validation before the API call.** Invalid files never reach OpenAI, which saves cost and avoids confusing errors.
- **Friendly errors.** Each OpenAI error type (authentication, rate limit, network, other API error) has its own message. The UI never shows the raw exception or the key.
- **Logging only once.** Streamlit re-runs the file on every click, so the logging setup checks whether a handler already exists.

## 11. Logging

The app writes to `app.log` in the project folder. The file is created automatically the first time the app runs.

Each line has a timestamp, a level and a message. Example (your times and filenames will differ):

```text
2026-11-18 15:30:02,114 | INFO | Application started
2026-11-18 15:30:20,905 | INFO | Image uploaded: server_rack.jpg (482113 bytes)
2026-11-18 15:30:21,003 | INFO | Image validation passed: server_rack.jpg
2026-11-18 15:30:30,227 | INFO | Selected analysis category: Server Rack
2026-11-18 15:30:30,229 | INFO | Analysis started for image: server_rack.jpg
2026-11-18 15:30:41,870 | INFO | Analysis completed successfully (1830 characters)
```

What is **not** logged: the API key, request headers, base64 image data or the full API response.

`RotatingFileHandler` starts a new file at 1 MB and keeps 3 old files (`app.log.1` to `app.log.3`).

## 12. Downloading Results

Click **Download Analysis (TXT)**. The browser saves a file named after the category and the date and time, for example:

```text
analysis_server_rack_20261118_153041.txt
```

The file contains the image filename, the category, the analysis date and time, and the generated analysis.

## 13. Troubleshooting

| Symptom | Likely cause and fix |
|---------|----------------------|
| `OPENAI_API_KEY is missing` | `.env` is missing, not in the same folder as the `.py` file, or the key line is empty. Fix it and restart the app. |
| `Authentication failed` | The key is wrong or was revoked. Copy the key again or create a new one. |
| `Rate limit or quota reached` | Your OpenAI account has hit a limit or needs billing set up. Wait, or check the usage page. |
| `Network error` | Check your internet connection and any proxy or firewall settings. |
| `Unsupported file type` | Only JPG, JPEG, PNG and WEBP are accepted. Convert GIF or BMP files first. |
| `File is too large` | The limit is 20 MB. Resize or compress the image. |
| `could not be read as an image` | The file is corrupted or only renamed to an image extension. Try another file. |
| `streamlit` is not recognised | The virtual environment is not active. Run `venv\Scripts\activate` first. |
| Port 8501 is already in use | Run `streamlit run module3_lab2_image_app.py --server.port 8502` and open `http://localhost:8502`. |
| Analysis is slow | A single analysis usually takes 5 to 20 seconds. Larger images take longer. |

To see the detailed error, open `app.log`.

## 14. Hands-On Exercises

**Exercise 1: Image Upload**
Upload an infrastructure image. Note its filename, dimensions and file size. Then try a file that is too large or not an image, and read the error message.

**Exercise 2: Analysis Category**
Select **General** and analyze an image. Then select **Server Rack** and analyze the same image. Compare the two responses. Which one gives more detail about the hardware?

**Exercise 3: Prompt Engineering**
Open `module3_lab2_image_app.py` and find the `"Server Rack"` entry in `ANALYSIS_PROMPTS`. Change the prompt so that it focuses more on cooling and ventilation (for example, airflow, hot and cold aisles, and fan status). Restart the app, analyze a server rack image and compare the result with the original.

**Exercise 4: Download Results**
Analyze an image and click **Download Analysis (TXT)**. Open the file and check that it contains the filename, the category, the date and time, and the analysis.

**Exercise 5: Basic Logging**
Open `app.log` in the project folder. Find the lines for the image upload, the validation, the category selection, the start of the analysis and its completion. Write down the time it took between "Analysis started" and "Analysis completed successfully".

---

## Security Notes

- `.env` holds your secret key. It is listed in `.gitignore`. Share only `.env.example`.
- The app never prints or logs the key, and it never shows it in the browser.
- Uploaded images are sent to OpenAI for analysis. Do not upload images that contain confidential data unless your organisation allows it.
