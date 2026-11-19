# Quick Start – Prompt Evaluation & Optimization Framework

This guide takes about 10 minutes. You do not need to write or change any Python code.

---

**Step 1: Open the project folder.**
Open the folder called `Mod 5 - Lab 1`. It contains `app.py`, `requirements.txt` and two CSV files.

**Step 2: Open a terminal in that folder.**
- On Windows: click the address bar at the top of the folder window, type `cmd` and press Enter.
- Or open *Terminal* / *Command Prompt* and use the `cd` command to go to the folder.

**Step 3: Install dependencies.**
Type this command and press Enter:

```
pip install -r requirements.txt
```

Wait until the installation finishes. This only needs to be done once.

**Step 4: Start the application.**
Type this command and press Enter:

```
streamlit run app.py
```

Keep this terminal window open while you work. Closing it stops the application.

**Step 5: Open the browser URL displayed in the terminal.**
The terminal shows a line such as `Local URL: http://localhost:8501`. Open that address in your browser. The application opens on the **Home** page.

**Step 6: Select Demo Mode or configure Live LLM Mode.**
- **Demo Mode** (the default): no API key needed. Answers are pre-written examples. Use this for practice and evaluation.
- **Live LLM Mode**: the prompts are sent to the OpenAI model. You need an API key (see the section below). In the sidebar, choose **Live LLM Mode** and pick a model.

**Step 7: Navigate through the five application pages.**
Use the menu on the left:
1. **Home**: the lab overview and the five-step workflow.
2. **Prompt Library**: choose a business scenario, read the sample input, view, edit or compare prompt versions.
3. **Run & Compare**: choose at least two prompt versions and run them on the same input.
4. **Manual Evaluation**: score each response on four criteria from 1 to 5.
5. **Prompt Leaderboard**: see the rankings, the charts and the best-performing prompt.

**Step 8: Complete the evaluation and view the leaderboard.**
1. Go to **Run & Compare** and run at least two prompt versions.
2. Go to **Manual Evaluation** and score each response.
3. Go to **Prompt Leaderboard** and read the results.

To start again from the beginning, open **Prompt Leaderboard**, scroll to **Reset Sample Data**, tick the confirmation box and click **Reset Sample Data**.

---

## Setting up the OpenAI API key (Live LLM Mode only)

Your API key is a secret, like a password. Keep it private.

1. In the project folder, find the file named `.env.example`.
2. Make a copy of it and rename the copy to exactly `.env`.
   - On Windows, if you cannot see the file extensions, ask your trainer for help with renaming.
3. Open `.env` in Notepad. Replace `your-api-key-here` with your own key, for example:
   ```
   OPENAI_API_KEY=sk-...your key...
   ```
4. Save the file and close it.
5. Stop the application (press `Ctrl + C` in the terminal) and start it again with `streamlit run app.py`.

Rules for the key:
- Never paste it into `app.py`, the CSV files or any document you share.
- Never send the `.env` file to anyone.
- If you think your key has been exposed, revoke it in your OpenAI account and create a new one.

If Live LLM Mode shows an error, check the **Troubleshooting** section in `README.md`, or switch back to Demo Mode from the sidebar.
