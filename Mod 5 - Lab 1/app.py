# =====================================================================
# Prompt Evaluation & Optimization Framework for Operations
# Module 5 - Lab 1
#
# Start the app with:   streamlit run app.py
#
# This is one file on purpose. It has five pages:
#   Home, Prompt Library, Run & Compare, Manual Evaluation,
#   Prompt Leaderboard.
# Data is stored in two CSV files next to this file:
#   prompt_versions.csv      - the prompt catalogue (every version is kept)
#   evaluation_results.csv   - the scores people give to each response
# =====================================================================

# ---------------------------------------------------------------
# 1. IMPORTS AND SETTINGS
# ---------------------------------------------------------------
import os
import uuid
from datetime import datetime

import altair as alt          # comes with Streamlit; used for the highlighted bar chart
import pandas as pd
import streamlit as st
from dotenv import load_dotenv  # reads the optional .env file
from openai import OpenAI       # used only in Live LLM Mode

# Folder that contains this file. The CSV files are stored here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE_DIR, "prompt_versions.csv")
EVAL_FILE = os.path.join(BASE_DIR, "evaluation_results.csv")

# Load settings (API key, model list) from a .env file if one exists.
load_dotenv(os.path.join(BASE_DIR, ".env"))

DEMO_MODE = "Demo Mode"
LIVE_MODE = "Live LLM Mode"
PAGES = ["Home", "Prompt Library", "Run & Compare", "Manual Evaluation", "Prompt Leaderboard"]
SCENARIOS = ["Incident Summarization", "Ticket Classification", "SOP Generation"]
SCENARIO_CODE = {
    "Incident Summarization": "INC",
    "Ticket Classification": "TKT",
    "SOP Generation": "SOP",
}
METRICS = ["Groundedness", "Intent Resolution", "Relevance", "Format Compliance"]

PROMPT_COLUMNS = [
    "Prompt ID", "Scenario", "Version Number", "Prompt Name", "Prompt Text",
    "Business Objective", "Created Date", "Version Description",
]
EVAL_COLUMNS = [
    "Evaluation ID", "Execution ID", "Prompt ID", "Scenario", "Prompt Version",
    "Groundedness", "Intent Resolution", "Relevance", "Format Compliance",
    "Average Score", "Evaluator Comments", "Evaluation Date",
]

# ---------------------------------------------------------------
# 2. BUSINESS CONTENT (sample inputs, objectives, scoring guide)
# ---------------------------------------------------------------
SAMPLE_INPUTS = {
    "Incident Summarization": (
        "Production application experienced intermittent downtime between 10:15 AM and 10:45 AM. "
        "Users reported login failures. Monitoring showed increased database connection timeouts. "
        "The infrastructure team restarted the application service at 10:40 AM. The service recovered "
        "at 10:45 AM. Root cause is still under investigation."
    ),
    "Ticket Classification": (
        "Multiple employees are unable to access the corporate VPN after the latest authentication "
        "policy update. Users receive an authentication failed message. The issue affects approximately "
        "35 employees across two departments."
    ),
    "SOP Generation": (
        "An operations engineer receives an alert that a production server has exceeded 90% CPU "
        "utilization. The engineer must check running processes, review monitoring data, identify the "
        "cause, escalate if required and document the resolution."
    ),
}

OBJECTIVES = {
    "Incident Summarization": (
        "Generate a concise, accurate incident summary containing: incident description, business "
        "impact, timeline, actions taken, current status and pending investigation."
    ),
    "Ticket Classification": (
        "Classify the ticket by category, priority, business impact, assignment group and "
        "recommended next action."
    ),
    "SOP Generation": (
        "Generate an operational SOP with purpose, scope, preconditions, step-by-step procedure, "
        "escalation conditions and a validation checklist."
    ),
}

# The four scoring criteria. 'question' is shown next to the slider.
# 'levels' describes what each score from 1 to 5 means.
CRITERIA = {
    "Groundedness": {
        "question": "Does the response stay faithful to the information in the business input?",
        "levels": {
            1: "Contains major unsupported information.",
            2: "Contains several unsupported statements.",
            3: "Mostly grounded, with some questionable details.",
            4: "Almost entirely grounded.",
            5: "Fully grounded in the supplied information.",
        },
    },
    "Intent Resolution": {
        "question": "Does the response fulfil the original business objective?",
        "levels": {
            1: "Does not address the business requirement.",
            2: "Addresses only a small part.",
            3: "Addresses the main requirement partially.",
            4: "Addresses almost all requirements.",
            5: "Completely fulfils the business requirement.",
        },
    },
    "Relevance": {
        "question": "Is the response relevant, focused and useful to the operations user?",
        "levels": {
            1: "Mostly irrelevant.",
            2: "Contains substantial irrelevant information.",
            3: "Partially relevant.",
            4: "Highly relevant.",
            5: "Directly relevant and actionable.",
        },
    },
    "Format Compliance": {
        "question": "Does the response follow the requested structure and output format?",
        "levels": {
            1: "Completely ignores the requested format.",
            2: "Follows very few formatting requirements.",
            3: "Partially follows the required format.",
            4: "Follows almost all formatting requirements.",
            5: "Fully follows the requested format.",
        },
    },
}

# Tips shown in the business interpretation when a metric is the weakest one.
IMPROVEMENT_TIPS = {
    "Groundedness": "Add the rule 'Use ONLY the information in the business input' and tell the AI to write 'Not stated in input' for unknown facts.",
    "Intent Resolution": "List the exact questions or sections the answer must cover, taken from the business objective.",
    "Relevance": "Name the audience and the purpose, and ask for short, actionable points instead of general background.",
    "Format Compliance": "Give the exact output template (headings, order, bullet points) and a maximum length.",
}

# The nine seeded prompt versions: three per scenario.
# V1 = basic, V2 = role-based with context, V3 = structured with rules and format.
SEED_PROMPTS = [
    {
        "Scenario": "Incident Summarization", "Version Number": 1, "Prompt Name": "Basic summary",
        "Prompt Text": "Summarize this incident for me.",
        "Version Description": "V1 - Basic prompt with no role, context, rules or output format.",
    },
    {
        "Scenario": "Incident Summarization", "Version Number": 2, "Prompt Name": "Role-based update",
        "Prompt Text": (
            "You are an IT operations analyst writing an incident update for the operations manager. "
            "Read the incident details below and write a short summary. Include what happened, how it "
            "affected users, and what has been done so far."
        ),
        "Version Description": "V2 - Adds a role and audience context, but no explicit output structure.",
    },
    {
        "Scenario": "Incident Summarization", "Version Number": 3, "Prompt Name": "Structured incident report",
        "Prompt Text": (
            "You are an IT operations analyst. Using ONLY the information in the business input, write an "
            "incident summary with exactly these sections, in this order:\n"
            "1. Incident description (2-3 sentences)\n"
            "2. Business impact (who was affected and how)\n"
            "3. Timeline (bulleted list with the times stated in the input)\n"
            "4. Actions taken (bulleted list)\n"
            "5. Current status (one sentence)\n"
            "6. Pending investigation (bulleted list)\n"
            "Rules: Do not add any cause, number or fact that is not in the input. If something is unknown, "
            "write 'Not stated in input'. Keep the total length under 250 words."
        ),
        "Version Description": "V3 - Explicit sections, order, grounding rules and a length limit.",
    },
    {
        "Scenario": "Ticket Classification", "Version Number": 1, "Prompt Name": "Basic classification",
        "Prompt Text": "Classify this IT ticket.",
        "Version Description": "V1 - Basic prompt with no role, context, rules or output format.",
    },
    {
        "Scenario": "Ticket Classification", "Version Number": 2, "Prompt Name": "Role-based classification",
        "Prompt Text": (
            "You are an IT service desk specialist. Read the ticket below and classify it. Give the "
            "category, priority, business impact, assignment group and the next action you recommend."
        ),
        "Version Description": "V2 - Adds a role and the fields to decide, but no fixed template.",
    },
    {
        "Scenario": "Ticket Classification", "Version Number": 3, "Prompt Name": "Structured service desk template",
        "Prompt Text": (
            "You are an IT service desk specialist. Classify the ticket using ONLY the information in the "
            "business input. Return the answer in this format:\n"
            "Category:\n"
            "Priority: (P1 Critical / P2 High / P3 Medium / P4 Low)\n"
            "Business impact: (number of users, departments, business effect)\n"
            "Assignment group:\n"
            "Recommended next action:\n"
            "Justification for priority: (one or two sentences that refer to the input)\n"
            "Rules: Do not invent facts. Choose one value for each field. Keep the answer under 150 words."
        ),
        "Version Description": "V3 - Fixed template, priority scale, grounding rules and a length limit.",
    },
    {
        "Scenario": "SOP Generation", "Version Number": 1, "Prompt Name": "Basic SOP",
        "Prompt Text": "Write an SOP for this alert.",
        "Version Description": "V1 - Basic prompt with no role, context, rules or output format.",
    },
    {
        "Scenario": "SOP Generation", "Version Number": 2, "Prompt Name": "Role-based SOP",
        "Prompt Text": (
            "You are an experienced operations engineer. Write a standard operating procedure (SOP) for "
            "handling the situation described below, so that a new engineer can follow it. Cover the "
            "purpose, scope, steps and when to escalate."
        ),
        "Version Description": "V2 - Adds a role and the topics to cover, but no fixed section layout.",
    },
    {
        "Scenario": "SOP Generation", "Version Number": 3, "Prompt Name": "Structured SOP template",
        "Prompt Text": (
            "You are an experienced operations engineer. Write an SOP using ONLY the information in the "
            "business input. Use exactly these six numbered sections:\n"
            "1. Purpose\n"
            "2. Scope\n"
            "3. Preconditions (bulleted list)\n"
            "4. Step-by-step procedure (numbered list, low-risk steps first)\n"
            "5. Escalation conditions (bulleted list)\n"
            "6. Validation checklist (checkbox list)\n"
            "Rules: Do not invent application names or facts that are not in the input. Keep it under 350 words."
        ),
        "Version Description": "V3 - Six fixed sections, safety order for steps and a length limit.",
    },
]

# Pre-written answers for Demo Mode. They are illustrative examples written for
# teaching, not output from a live model. Keyed by Prompt ID.
DEMO_OUTPUTS = {
    "INC-V1": """
The production application had downtime from 10:15 AM to 10:45 AM. Users could not log in. The database had connection timeouts. The team restarted the service at 10:40 AM and it recovered at 10:45 AM. The outage was caused by a faulty database update deployed earlier that morning, and about 2,000 customers could not place orders. The team is now rolling back the update.
""",
    "INC-V2": """
As an IT operations analyst, here is the incident update for the operations manager:

Between 10:15 and 10:45 AM, the production application had intermittent downtime and users saw login failures. Monitoring showed more database connection timeouts. The infrastructure team restarted the application service at 10:40 AM, and the service recovered at 10:45 AM.

Business impact: users could not log in during the outage window. The root cause is still under investigation, so the team should confirm what triggered the database connection timeouts before closing the incident.
""",
    "INC-V3": """
**Incident description**
Intermittent downtime of the production application occurred between 10:15 AM and 10:45 AM. Users reported login failures, and monitoring showed increased database connection timeouts.

**Business impact**
Users were unable to log in during the incident window. The number of affected users is not stated in the input.

**Timeline**
- 10:15 AM - Intermittent downtime begins
- 10:40 AM - Infrastructure team restarts the application service
- 10:45 AM - Service recovers

**Actions taken**
- The infrastructure team restarted the application service.

**Current status**
The service has recovered. The root cause is still under investigation.

**Pending investigation**
- Determine the cause of the database connection timeouts.
- Confirm how many users were affected.
""",
    "TKT-V1": """
Category: Network access
Priority: High
Assignment group: Network team
Action: Fix the VPN.
""",
    "TKT-V2": """
This is a network issue with Priority P1 (Critical). The VPN is down for the entire company, so all staff are unable to work remotely.

Business impact: company-wide outage affecting all employees.
Assignment group: Network Operations.
Recommended next action: Roll back the VPN server to the previous version and send a company-wide notice.
""",
    "TKT-V3": """
Category: Access and authentication (VPN)
Priority: P2 (High)
Business impact: About 35 employees across two departments cannot connect to the corporate VPN. The input does not state any effect on customers or revenue.
Assignment group: Identity and Access Management (IAM)
Recommended next action: Review the latest authentication policy change, check the authentication failure logs for the affected accounts, and decide whether a rollback or a temporary exception is needed.
Justification for priority: Several employees in two departments are blocked, which needs quick action. The input does not say the whole company is affected, so P2 is more accurate than P1.
""",
    "SOP-V1": """
1. Log in to the production server.
2. Check the CPU usage.
3. Look at the running processes.
4. Kill the process that uses the most CPU.
5. Write down what you did.
""",
    "SOP-V2": """
Purpose: This SOP helps an operations engineer respond to high CPU alerts on production servers.

Scope: Production servers that trigger a CPU alert above 90 percent.

Procedure: First, open the monitoring dashboard and check how CPU has changed over time. Next, open the process list and find the process that uses the most CPU. If it is a known application process, restart it. Note the time and what you did. If the problem continues, contact your manager.

Escalation: Escalate to the on-call team if the problem continues.
""",
    "SOP-V3": """
**1. Purpose**
Provide a standard way to investigate and resolve a production server alert for CPU utilisation above 90%.

**2. Scope**
Applies to operations engineers who respond to CPU alerts on production servers.

**3. Preconditions**
- The alert is confirmed in the monitoring tool.
- The engineer has access to the server and its monitoring data.
- The engineer knows the application owner of the server.

**4. Step-by-step procedure**
1. Confirm the alert and note the start time and the CPU level.
2. Check the running processes and identify the top CPU users.
3. Review monitoring data for the last 24 hours to see when the increase began.
4. Identify the likely cause and record it.
5. Apply a low-risk fix (for example, stop a runaway non-critical process) only with approval from the process owner.
6. Confirm that CPU returns to normal and record the resolution.

**5. Escalation conditions**
- CPU stays above 90% after the fix.
- The high-CPU process belongs to a critical business service.
- The cause is still unknown after 30 minutes.

**6. Validation checklist**
- [ ] CPU is below the alert threshold.
- [ ] Services are running normally.
- [ ] The cause and the fix are documented.
- [ ] The application owner has been informed.
""",
}

# The Home page workflow steps: (title, short explanation).
WORKFLOW_STEPS = [
    ("Select a business scenario", "Choose Incident Summarization, Ticket Classification or SOP Generation."),
    ("Create multiple prompt versions", "Write or improve prompts. Every change is saved as a new version."),
    ("Execute and compare prompts", "Run the versions on the same input and read the answers side by side."),
    ("Manually evaluate the responses", "Score each answer on four criteria from 1 (poor) to 5 (excellent)."),
    ("Review the Prompt Leaderboard", "See which prompt version scored best, and why."),
]


# ---------------------------------------------------------------
# 3. SMALL HELPER FUNCTIONS
# ---------------------------------------------------------------
def new_short_id():
    # A short random code, for example "3F9A1C07". Unique enough for this lab.
    return uuid.uuid4().hex[:8].upper()


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def go_to(page):
    # Button callback: changes the page shown in the sidebar.
    st.session_state["nav"] = page


def switch_to_demo():
    # Button callback: used after a Live error so the participant can continue in Demo Mode.
    st.session_state["mode"] = DEMO_MODE


def get_api_key():
    # Reads OPENAI_API_KEY from the environment or .env. Returns "" if missing.
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if key in ("", "your-api-key-here"):
        return ""
    return key


def get_model_options():
    # OPENAI_MODELS is a comma-separated list, for example "gpt-4o-mini,gpt-4o".
    raw = os.getenv("OPENAI_MODELS", "gpt-4o-mini,gpt-4o")
    models = [item.strip() for item in raw.split(",") if item.strip()]
    return models or ["gpt-4o-mini"]


def show_mode_banner(mode, model=""):
    # Makes it obvious whether the answers are live or pre-written.
    if mode == DEMO_MODE:
        st.warning(
            "**Demo Mode:** answers are pre-written, illustrative examples. They are NOT live AI output "
            "and no API call is made."
        )
    else:
        st.success(f"**Live LLM Mode:** prompts are sent to the OpenAI model '{model}'. This uses API credits.")


# ---------------------------------------------------------------
# 4. CSV STORAGE
# ---------------------------------------------------------------
def file_has_content(path):
    return os.path.exists(path) and os.path.getsize(path) > 0


def make_seed_prompts_df():
    # Builds the nine sample prompt versions with their IDs and dates.
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []
    for item in SEED_PROMPTS:
        code = SCENARIO_CODE[item["Scenario"]]
        version = item["Version Number"]
        rows.append({
            "Prompt ID": f"{code}-V{version}",
            "Scenario": item["Scenario"],
            "Version Number": str(version),
            "Prompt Name": item["Prompt Name"],
            "Prompt Text": item["Prompt Text"],
            "Business Objective": OBJECTIVES[item["Scenario"]],
            "Created Date": today,
            "Version Description": item["Version Description"],
        })
    return pd.DataFrame(rows, columns=PROMPT_COLUMNS)


def ensure_data_files():
    # Creates the two CSV files with headers (and the sample prompts) if they are missing.
    if not file_has_content(PROMPT_FILE):
        save_prompts(make_seed_prompts_df())
    if not file_has_content(EVAL_FILE):
        save_evals(pd.DataFrame(columns=EVAL_COLUMNS))


def load_prompts():
    # Everything is read as text so that IDs and dates are never changed by pandas.
    return pd.read_csv(PROMPT_FILE, dtype=str, keep_default_na=False)


def save_prompts(df):
    df[PROMPT_COLUMNS].to_csv(PROMPT_FILE, index=False)


def load_evals():
    return pd.read_csv(EVAL_FILE, dtype=str, keep_default_na=False)


def save_evals(df):
    df[EVAL_COLUMNS].to_csv(EVAL_FILE, index=False)


def load_evals_numeric():
    # Same as load_evals, but the score columns are converted to numbers for maths and charts.
    evals = load_evals()
    for col in METRICS + ["Average Score"]:
        evals[col] = pd.to_numeric(evals[col], errors="coerce")
    return evals.dropna(subset=["Average Score"])


def get_scenario_prompts(prompts, scenario):
    # Returns the versions of one scenario, oldest first, with a numeric version number.
    df = prompts[prompts["Scenario"] == scenario].copy()
    df["Version Number"] = df["Version Number"].astype(int)
    return df.sort_values("Version Number").reset_index(drop=True)


def prompt_labels(df):
    # Friendly labels for dropdowns, for example "INC-V2 - Role-based update".
    labels = {}
    for _, row in df.iterrows():
        labels[row["Prompt ID"]] = f"{row['Prompt ID']} - {row['Prompt Name']}"
    return labels


def find_prompt(df, prompt_id):
    return df[df["Prompt ID"] == prompt_id].iloc[0]


def make_prompt_row(scenario, version, name, text, objective, description):
    # A new record for the catalogue. Old records are never changed.
    code = SCENARIO_CODE[scenario]
    return {
        "Prompt ID": f"{code}-V{version}",
        "Scenario": scenario,
        "Version Number": str(version),
        "Prompt Name": name,
        "Prompt Text": text,
        "Business Objective": objective,
        "Created Date": datetime.now().strftime("%Y-%m-%d"),
        "Version Description": description,
    }


def find_evaluation(evals, execution_id):
    # Returns the saved evaluation for one response, or None if it has not been scored yet.
    rows = evals[evals["Execution ID"] == execution_id]
    if len(rows) == 0:
        return None
    return rows.iloc[0]


def save_evaluation(execution, scores, comments, update_existing):
    # Saves one evaluation. If update_existing is True, the old row for this response is replaced.
    evals = load_evals()
    average = round(sum(scores) / len(scores), 2)
    matches = evals.index[evals["Execution ID"] == execution["Execution ID"]].tolist()

    row = {
        "Evaluation ID": "EV-" + new_short_id(),
        "Execution ID": execution["Execution ID"],
        "Prompt ID": execution["Prompt ID"],
        "Scenario": execution["Scenario"],
        "Prompt Version": execution["Prompt Version"],
        "Groundedness": str(scores[0]),
        "Intent Resolution": str(scores[1]),
        "Relevance": str(scores[2]),
        "Format Compliance": str(scores[3]),
        "Average Score": f"{average:.2f}",
        "Evaluator Comments": comments,
        "Evaluation Date": now_text(),
    }

    if update_existing and len(matches) > 0:
        # Keep the original Evaluation ID, replace the scores and the date.
        index = matches[0]
        row["Evaluation ID"] = evals.loc[index, "Evaluation ID"]
        for col in EVAL_COLUMNS:
            evals.loc[index, col] = row[col]
    else:
        evals = pd.concat([evals, pd.DataFrame([row])], ignore_index=True)

    save_evals(evals)
    return row["Evaluation ID"]


# ---------------------------------------------------------------
# 5. RUNNING PROMPTS (LIVE AND DEMO)
# ---------------------------------------------------------------
def run_demo(prompt_id):
    # Returns the pre-written answer for a seeded prompt version.
    return DEMO_OUTPUTS[prompt_id].strip()


def run_live(prompt_text, business_input, model):
    # Sends the prompt and the business input to the OpenAI API.
    # Returns (answer, error). Exactly one of them is None.
    api_key = get_api_key()
    if not api_key:
        return None, ("No API key was found. Add your key to the .env file (see QUICKSTART.md) "
                      "or switch to Demo Mode.")
    try:
        client = OpenAI(api_key=api_key)
        full_message = prompt_text + "\n\nBusiness input:\n" + business_input
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": full_message}],
        )
        answer = completion.choices[0].message.content or ""
        return answer.strip(), None
    except Exception as error:
        # Show the real problem (bad key, rate limit, network...) instead of hiding it.
        return None, f"{type(error).__name__}: {error}"


def make_execution(row, scenario, response, mode, model):
    # One record per run. Stored in session memory and used by Manual Evaluation.
    return {
        "Execution ID": "EX-" + new_short_id(),
        "Prompt ID": row["Prompt ID"],
        "Prompt Name": row["Prompt Name"],
        "Scenario": scenario,
        "Prompt Version": "V" + str(row["Version Number"]),
        "Business Input": SAMPLE_INPUTS[scenario],
        "Generated Response": response,
        "Execution Mode": mode,
        "Model": model if mode == LIVE_MODE else "Pre-written demo answer",
        "Execution Timestamp": now_text(),
    }


# ---------------------------------------------------------------
# 6. LEADERBOARD CALCULATIONS
# ---------------------------------------------------------------
def build_leaderboard(evals, prompts):
    # One row per prompt version: the average of each criterion across all its evaluations.
    agg = {}
    for metric in METRICS:
        agg[metric] = "mean"
    agg["Average Score"] = "mean"
    agg["Execution ID"] = "count"

    board = evals.groupby(["Prompt ID", "Scenario"], as_index=False).agg(agg)
    board = board.rename(columns={"Execution ID": "Evaluations"})
    board[METRICS + ["Average Score"]] = board[METRICS + ["Average Score"]].round(2)

    names = dict(zip(prompts["Prompt ID"], prompts["Prompt Name"]))
    board["Prompt Name"] = board["Prompt ID"].map(names).fillna("")

    board = board.sort_values(["Average Score", "Prompt ID"], ascending=[False, True])
    board = board.reset_index(drop=True)
    return add_rank_column(board)


def add_rank_column(board):
    # Rank = 1 + number of prompts with a strictly higher average.
    # Prompts with the same average get the same rank and are marked "(Tied)".
    averages = list(board["Average Score"])
    labels = []
    for average in averages:
        ahead = len([value for value in averages if value > average])
        same = len([value for value in averages if value == average])
        label = str(ahead + 1)
        if same > 1:
            label = label + " (Tied)"
        labels.append(label)
    board.insert(0, "Rank", labels)
    return board


def average_bar_chart(filtered, top_id):
    # Bar chart of average scores. The best prompt is coloured green.
    chart_df = filtered[["Prompt ID", "Average Score"]].copy()
    chart_df["Highlight"] = [
        "Highest performer" if pid == top_id else "Other prompts" for pid in chart_df["Prompt ID"]
    ]
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Prompt ID:N", sort=None, title="Prompt version"),
        y=alt.Y("Average Score:Q", scale=alt.Scale(domain=[0, 5]), title="Average score (out of 5)"),
        color=alt.Color(
            "Highlight:N",
            scale=alt.Scale(domain=["Highest performer", "Other prompts"], range=["#2E7D32", "#90A4AE"]),
            legend=alt.Legend(title=None),
        ),
        tooltip=["Prompt ID", "Average Score"],
    ).properties(height=320)
    st.altair_chart(chart)


# ---------------------------------------------------------------
# 7. SIDEBAR AND SESSION SETUP
# ---------------------------------------------------------------
def init_session():
    # Sets default values the first time the page opens in this browser session.
    if "executions" not in st.session_state:
        st.session_state["executions"] = []
    if "mode" not in st.session_state:
        st.session_state["mode"] = DEMO_MODE
    if "nav" not in st.session_state:
        st.session_state["nav"] = "Home"


def render_sidebar():
    st.sidebar.title("Lab navigation")
    st.sidebar.radio("Go to", PAGES, key="nav")
    st.sidebar.divider()
    st.sidebar.radio(
        "Execution mode",
        [DEMO_MODE, LIVE_MODE],
        key="mode",
        help="Demo Mode needs no API key. Live LLM Mode calls the OpenAI API.",
    )
    if st.session_state["mode"] == LIVE_MODE:
        if get_api_key():
            st.sidebar.success("API key found.")
        else:
            st.sidebar.error("No API key found. See QUICKSTART.md, or switch to Demo Mode.")
        st.sidebar.selectbox("Model", get_model_options(), key="model")
    else:
        st.sidebar.info("Demo Mode uses pre-written sample answers. No API key is needed.")


# ---------------------------------------------------------------
# 8. PAGE 1 - HOME
# ---------------------------------------------------------------
def find_next_step():
    # Works out which of the five steps the participant should do next.
    executions = st.session_state["executions"]
    if len(executions) == 0:
        return 3
    evaluated_ids = set(load_evals()["Execution ID"])
    waiting = [item for item in executions if item["Execution ID"] not in evaluated_ids]
    if len(waiting) > 0:
        return 4
    return 5


def page_home():
    st.title("Prompt Evaluation & Optimization Framework for Operations")
    st.write(
        "**Lab objective:** show how a small change in a prompt changes the quality of a GenAI answer, "
        "and how to measure that change with a simple, repeatable method."
    )

    st.info("**Start by opening the Prompt Library and selecting a business scenario.**")
    st.button("Open the Prompt Library", type="primary", on_click=go_to, args=("Prompt Library",))

    st.subheader("What you will learn")
    st.markdown(
        "- Why the wording and structure of a prompt change the quality of the answer.\n"
        "- How to create new prompt versions without losing the old ones.\n"
        "- How to compare answers fairly, using the same business input.\n"
        "- How to score answers on four criteria and calculate an average.\n"
        "- How to use the evidence to choose and improve the best prompt."
    )

    st.subheader("Three business scenarios")
    scenario_cols = st.columns(3)
    for col, scenario in zip(scenario_cols, SCENARIOS):
        with col:
            with st.container(border=True):
                st.markdown(f"**{scenario}**")
                st.caption(OBJECTIVES[scenario])

    st.subheader("The five-step workflow")
    next_step = find_next_step()
    step_cols = st.columns(5)
    for number, (col, step) in enumerate(zip(step_cols, WORKFLOW_STEPS), start=1):
        title, text = step
        with col:
            with st.container(border=True):
                st.markdown(f"**Step {number}**")
                st.markdown(f"**{title}**")
                st.caption(text)
                if number == next_step:
                    st.success("Do this next")

    st.subheader("Current status")
    prompts = load_prompts()
    evals = load_evals_numeric()
    best_text = "None yet"
    if len(evals) > 0:
        board = build_leaderboard(evals, prompts)
        top = board.iloc[0]
        best_text = f"{top['Prompt ID']} ({top['Average Score']:.2f} / 5)"

    stat_cols = st.columns(4)
    stat_cols[0].metric("Execution mode", st.session_state["mode"])
    stat_cols[1].metric("Prompts in the catalogue", len(prompts))
    stat_cols[2].metric("Evaluations completed", len(load_evals()))
    stat_cols[3].metric("Highest-rated prompt", best_text)

    st.subheader("How to complete the lab")
    st.markdown(
        "1. Open **Prompt Library**, choose a scenario and read the sample business input.\n"
        "2. Optional: create a new version of a prompt. Old versions are always kept.\n"
        "3. Open **Run & Compare**, choose at least two versions and run them.\n"
        "4. Open **Manual Evaluation** and score each answer on the four criteria.\n"
        "5. Open **Prompt Leaderboard** to see which version performed best and what to improve."
    )


# ---------------------------------------------------------------
# 9. PAGE 2 - PROMPT LIBRARY
# ---------------------------------------------------------------
def page_library():
    st.title("Prompt Library")
    st.write(
        "A **prompt** is the instruction given to the AI. Every change creates a **new version**. "
        "Earlier versions are never overwritten, so you can always compare them."
    )

    scenario = st.selectbox("Choose a business scenario", SCENARIOS, key="lib_scenario")
    st.info(f"**Sample business input:** {SAMPLE_INPUTS[scenario]}\n\n**Business objective:** {OBJECTIVES[scenario]}")

    prompts = load_prompts()
    scen_df = get_scenario_prompts(prompts, scenario)
    labels = prompt_labels(scen_df)

    tab_view, tab_edit, tab_compare = st.tabs(["1. View versions", "2. Create or edit a version", "3. Compare two versions"])

    # --- Tab 1: list and read the versions ---
    with tab_view:
        st.write("All saved versions for this scenario:")
        st.dataframe(
            scen_df[["Prompt ID", "Prompt Name", "Version Number", "Created Date", "Version Description"]],
            hide_index=True,
        )
        chosen = st.selectbox(
            "Open a version to read the full text",
            list(scen_df["Prompt ID"]),
            format_func=labels.get,
            key=f"view_pick_{scenario}",
        )
        row = find_prompt(scen_df, chosen)
        st.text_area(
            "Full prompt text (read only)",
            value=row["Prompt Text"],
            height=220,
            disabled=True,
            key=f"view_text_{chosen}",
        )
        st.caption(f"Business objective: {row['Business Objective']}")

    # --- Tab 2: create a new prompt, or edit an old one (saved as a new version) ---
    with tab_edit:
        st.write(
            "To **edit** a prompt, choose the version to start from, change the text and save. "
            "This creates a **new version**. The old version stays unchanged."
        )
        source_options = ["NEW"] + list(scen_df["Prompt ID"])
        source_labels = {"NEW": "Start a brand-new blank prompt"}
        source_labels.update(labels)
        source = st.selectbox(
            "Start from",
            source_options,
            format_func=source_labels.get,
            key=f"edit_source_{scenario}",
        )

        # When the starting point changes, the form is filled with that version's text.
        if source == "NEW":
            base_name, base_text = "", ""
        else:
            base = find_prompt(scen_df, source)
            base_name, base_text = base["Prompt Name"], base["Prompt Text"]

        name = st.text_input("Prompt name", value=base_name, key=f"edit_name_{source}")
        text = st.text_area("Prompt text", value=base_text, height=240, key=f"edit_text_{source}")
        objective = st.text_area("Business objective", value=OBJECTIVES[scenario], height=80, key=f"edit_obj_{scenario}")
        description = st.text_input(
            "Version description - what did you change, and why?",
            key=f"edit_desc_{source}",
        )

        if st.button("Save as new version", type="primary", key=f"save_version_{scenario}"):
            if not name.strip() or not text.strip() or not description.strip():
                st.error("Please fill in the prompt name, the prompt text and the version description.")
            else:
                new_version = int(scen_df["Version Number"].max()) + 1
                new_row = make_prompt_row(
                    scenario, new_version, name.strip(), text.strip(), objective.strip(), description.strip()
                )
                updated = pd.concat([prompts, pd.DataFrame([new_row])], ignore_index=True)
                save_prompts(updated)
                st.session_state["flash"] = (
                    f"Saved new version {new_row['Prompt ID']}. All earlier versions were kept unchanged."
                )
                st.rerun()

    # --- Tab 3: compare two versions side by side ---
    with tab_compare:
        ids = list(scen_df["Prompt ID"])
        col_a, col_b = st.columns(2)
        with col_a:
            left_id = st.selectbox("Version A", ids, index=0, format_func=labels.get, key=f"cmp_a_{scenario}")
        with col_b:
            right_id = st.selectbox("Version B", ids, index=min(1, len(ids) - 1), format_func=labels.get, key=f"cmp_b_{scenario}")

        left_row = find_prompt(scen_df, left_id)
        right_row = find_prompt(scen_df, right_id)
        with col_a:
            st.text_area("Version A text", value=left_row["Prompt Text"], height=260, disabled=True, key=f"cmp_text_a_{left_id}")
        with col_b:
            st.text_area("Version B text", value=right_row["Prompt Text"], height=260, disabled=True, key=f"cmp_text_b_{right_id}")

        # A simple structure check: does the text mention a format, sections or rules?
        comparison = pd.DataFrame([
            {"Version": left_id, "Words": len(left_row["Prompt Text"].split()),
             "Mentions format or sections": "Yes" if ("format" in left_row["Prompt Text"].lower() or "section" in left_row["Prompt Text"].lower()) else "No"},
            {"Version": right_id, "Words": len(right_row["Prompt Text"].split()),
             "Mentions format or sections": "Yes" if ("format" in right_row["Prompt Text"].lower() or "section" in right_row["Prompt Text"].lower()) else "No"},
        ])
        st.dataframe(comparison, hide_index=True)
        st.caption("More structure (roles, sections, rules, length limits) usually gives more predictable answers.")


# ---------------------------------------------------------------
# 10. PAGE 3 - RUN & COMPARE
# ---------------------------------------------------------------
def run_prompts(scen_df, chosen, scenario, mode):
    # Runs each chosen prompt version on the same business input.
    model = st.session_state.get("model", get_model_options()[0])
    results = []
    for prompt_id in chosen:
        row = find_prompt(scen_df, prompt_id)
        if mode == DEMO_MODE:
            if prompt_id not in DEMO_OUTPUTS:
                st.warning(f"{prompt_id} has no pre-written demo answer, so it was skipped. Use Live LLM Mode to run it.")
                continue
            response = run_demo(prompt_id)
            error = None
        else:
            response, error = run_live(row["Prompt Text"], SAMPLE_INPUTS[scenario], model)

        if error is not None:
            # Show the error. Never replace it with a demo answer silently.
            st.error(f"The live call for {prompt_id} failed. {error}")
            if mode == LIVE_MODE:
                st.button("Switch to Demo Mode", on_click=switch_to_demo, key="switch_demo_button")
            break

        execution = make_execution(row, scenario, response, mode, model)
        results.append(execution)
        st.session_state["executions"].append(execution)

    st.session_state["last_run"] = results
    if len(results) > 0:
        st.success(f"Finished. {len(results)} response(s) were added to the Manual Evaluation list.")


def render_response_card(item):
    st.markdown(f"#### {item['Prompt ID']}")
    st.caption(f"{item['Prompt Name']} | {item['Execution Mode']} | {item['Execution Timestamp']}")
    st.caption(f"Execution ID: {item['Execution ID']}")
    with st.container(border=True):
        st.markdown(item["Generated Response"])


def show_latest_results(scenario):
    results = [item for item in st.session_state.get("last_run", []) if item["Scenario"] == scenario]
    if len(results) == 0:
        return
    st.subheader("Latest responses, side by side")
    if len(results) <= 3:
        columns = st.columns(len(results))
    else:
        columns = [st.container() for _ in results]
    for col, item in zip(columns, results):
        with col:
            render_response_card(item)


def page_run():
    st.title("Run & Compare")
    st.write("Run two or more prompt versions on the **same** business input, then compare the answers.")

    scenario = st.selectbox("Step 1 - Choose a business scenario", SCENARIOS, key="run_scenario")
    st.info(f"**Business input (the same for every version):** {SAMPLE_INPUTS[scenario]}")

    mode = st.session_state["mode"]
    model = st.session_state.get("model", get_model_options()[0])
    show_mode_banner(mode, model)

    scen_df = get_scenario_prompts(load_prompts(), scenario)
    labels = prompt_labels(scen_df)
    all_ids = list(scen_df["Prompt ID"])

    chosen = st.multiselect(
        "Step 2 - Choose at least two prompt versions",
        all_ids,
        default=all_ids[:3],
        format_func=labels.get,
        key=f"run_pick_{scenario}",
    )
    if mode == DEMO_MODE:
        st.caption("Demo Mode has pre-written answers only for the nine sample versions.")

    if st.button("Step 3 - Run the selected prompts", type="primary", key="run_button"):
        if len(chosen) < 2:
            st.warning("Please choose at least two prompt versions so that you can compare them.")
        else:
            with st.spinner("Running the prompts..."):
                run_prompts(scen_df, chosen, scenario, mode)

    show_latest_results(scenario)

    with st.expander("All responses from this browser session"):
        executions = st.session_state["executions"]
        if len(executions) == 0:
            st.write("No responses yet.")
        else:
            history = pd.DataFrame(executions)
            st.dataframe(
                history[["Execution ID", "Prompt ID", "Scenario", "Prompt Version", "Execution Mode", "Execution Timestamp"]],
                hide_index=True,
            )


# ---------------------------------------------------------------
# 11. PAGE 4 - MANUAL EVALUATION
# ---------------------------------------------------------------
def page_evaluation():
    st.title("Manual Evaluation")
    st.write(
        "Read the business input and the AI response, then score the response on four criteria "
        "from **1 (poor)** to **5 (excellent)**. You give the scores yourself. The application does not score automatically."
    )

    executions = st.session_state["executions"]
    if len(executions) == 0:
        st.info("There are no responses to evaluate yet. Open **Run & Compare**, run at least one prompt, then come back here.")
        return

    evals = load_evals()
    evaluated_ids = set(evals["Execution ID"])

    # Build the dropdown labels. Newest responses are shown first.
    labels = {}
    for item in executions:
        status = "Evaluated" if item["Execution ID"] in evaluated_ids else "Not yet evaluated"
        labels[item["Execution ID"]] = (
            f"{item['Prompt ID']} | {item['Scenario']} | {item['Execution Timestamp']} | {status}"
        )
    options = [item["Execution ID"] for item in reversed(executions)]
    choice = st.selectbox("Choose a response to evaluate", options, format_func=labels.get, key="eval_choice")

    item = None
    for candidate in executions:
        if candidate["Execution ID"] == choice:
            item = candidate

    # Show what the evaluator needs to read.
    st.subheader(f"{item['Prompt ID']} - {item['Prompt Name']}")
    st.markdown(
        f"**Scenario:** {item['Scenario']}  \n"
        f"**Prompt version:** {item['Prompt Version']}  \n"
        f"**Execution ID:** {item['Execution ID']}  \n"
        f"**Mode:** {item['Execution Mode']}"
    )
    st.markdown("**Original business input**")
    st.info(item["Business Input"])
    st.markdown("**Generated response**")
    with st.container(border=True):
        st.markdown(item["Generated Response"])

    # Stop duplicate scoring: if this response was already scored, the user must tick 'update'.
    existing = find_evaluation(evals, choice)
    update = False
    if existing is not None:
        st.warning(
            f"This response was already evaluated (average {float(existing['Average Score']):.2f} / 5). "
            "Tick the box below only if you want to replace the scores."
        )
        update = st.checkbox("Yes, update the existing evaluation", key=f"update_{choice}")

    st.subheader("Your scores")
    st.caption("Use the slider for each criterion. The description on the right explains the chosen level.")
    scores = []
    for metric in METRICS:
        info = CRITERIA[metric]
        default_score = 3
        if existing is not None:
            default_score = int(float(existing[metric]))
        left, right = st.columns([1, 2])
        with left:
            score = st.slider(metric, min_value=1, max_value=5, value=default_score, key=f"score_{choice}_{metric}")
        with right:
            st.caption(info["question"])
            st.markdown(f"**{score} -** {info['levels'][score]}")
        scores.append(score)

    average = round(sum(scores) / len(scores), 2)
    st.metric("Average Score", f"{average:.2f} / 5")
    st.caption("Average Score = (Groundedness + Intent Resolution + Relevance + Format Compliance) / 4")

    default_comment = ""
    if existing is not None:
        default_comment = existing["Evaluator Comments"]
    comments = st.text_area(
        "Evaluator comments (what worked, what was missing?)",
        value=default_comment,
        key=f"comment_{choice}",
    )

    if st.button("Submit evaluation", type="primary", key=f"submit_{choice}"):
        if existing is not None and not update:
            st.error("This response is already evaluated. Tick the update box if you want to replace the scores.")
        else:
            eval_id = save_evaluation(item, scores, comments.strip(), existing is not None)
            st.session_state["flash"] = f"Evaluation {eval_id} saved. Average score: {average:.2f} / 5."
            st.rerun()


# ---------------------------------------------------------------
# 12. PAGE 5 - PROMPT LEADERBOARD
# ---------------------------------------------------------------
def render_reset_section():
    with st.expander("Reset Sample Data"):
        st.write(
            "This restores the nine sample prompt versions and **deletes every evaluation record**. "
            "Any prompt versions you created will also be removed."
        )
        confirmed = st.checkbox(
            "Yes, delete all evaluation records and restore the sample prompts",
            key="reset_confirm",
        )
        if st.button("Reset Sample Data", disabled=not confirmed, key="reset_button"):
            save_prompts(make_seed_prompts_df())
            save_evals(pd.DataFrame(columns=EVAL_COLUMNS))
            st.session_state["flash"] = "Sample data restored. The nine sample prompts are back and the evaluation records were cleared."
            st.rerun()


def page_leaderboard():
    st.title("Prompt Leaderboard")
    st.write("Rankings use the average of the four criteria. All four criteria carry equal weight.")

    evals = load_evals_numeric()
    if len(evals) == 0:
        st.info(
            "**The leaderboard is empty because no responses have been evaluated yet.** To fill it:\n\n"
            "1. Open **Run & Compare** and run at least two prompt versions.\n"
            "2. Open **Manual Evaluation** and score each response.\n"
            "3. Come back here to see the rankings."
        )
        render_reset_section()
        return

    prompts = load_prompts()
    board = build_leaderboard(evals, prompts)
    top = board.iloc[0]
    # Every prompt that shares the top average (more than one means a tie).
    tied_ids = list(board[board["Average Score"] == top["Average Score"]]["Prompt ID"])
    is_tie = len(tied_ids) > 1

    # Headline numbers (always for the whole leaderboard, not the filtered view).
    stat_cols = st.columns(4)
    stat_cols[0].metric("Prompts evaluated", board["Prompt ID"].nunique())
    stat_cols[1].metric("Evaluation records", len(evals))
    stat_cols[2].metric("Best-performing prompt", top["Prompt ID"] + (" (tied)" if is_tie else ""))
    stat_cols[3].metric("Highest average score", f"{top['Average Score']:.2f} / 5")

    if board["Prompt ID"].nunique() < 2:
        st.info(
            "To compare prompts, evaluate responses from at least **two different prompt versions**. "
            "Results so far are shown below."
        )

    # Filters for the table and charts.
    st.subheader("Leaderboard table")
    filter_cols = st.columns(2)
    with filter_cols[0]:
        scenario_filter = st.multiselect(
            "Filter by business scenario",
            sorted(board["Scenario"].unique()),
            default=sorted(board["Scenario"].unique()),
            key="lb_scenario_filter",
        )
    with filter_cols[1]:
        version_filter = st.multiselect(
            "Filter by prompt version",
            list(board["Prompt ID"]),
            default=list(board["Prompt ID"]),
            key="lb_version_filter",
        )

    filtered = board[board["Scenario"].isin(scenario_filter) & board["Prompt ID"].isin(version_filter)]
    if len(filtered) == 0:
        st.warning("No prompts match the current filters. Change the filters to see results.")
    else:
        display = filtered.copy()
        display["Prompt Version"] = display["Prompt ID"] + " - " + display["Prompt Name"]
        columns = ["Rank", "Scenario", "Prompt Version"] + METRICS + ["Average Score", "Evaluations"]
        st.dataframe(display[columns], hide_index=True)

        # Charts use the same filtered view.
        st.subheader("Average score by prompt version")
        average_bar_chart(filtered, top["Prompt ID"])

        st.subheader("The four criteria compared")
        st.bar_chart(filtered.set_index("Prompt ID")[METRICS])

    st.subheader("Scenario-wise performance")
    by_scenario = evals.groupby("Scenario")["Average Score"].mean().round(2)
    st.bar_chart(by_scenario)

    # Highlight the best prompt and explain why it won.
    st.subheader("Highest-performing prompt")
    if is_tie:
        st.warning(
            f"**Tie:** {', '.join(tied_ids)} share the highest average of **{top['Average Score']:.2f} / 5**. "
            "Look at the individual criteria below to decide which one is better for your business."
        )
    else:
        st.success(
            f"**{top['Prompt ID']} - {top['Prompt Name']}** ranks first with an average of "
            f"**{top['Average Score']:.2f} / 5** across {int(top['Evaluations'])} evaluation(s)."
        )
    metric_text = ", ".join(f"{metric} {float(top[metric]):.2f}" for metric in METRICS)
    st.write(f"Scores by criterion: {metric_text}.")

    strongest = METRICS[0]
    weakest = METRICS[0]
    for metric in METRICS:
        if float(top[metric]) > float(top[strongest]):
            strongest = metric
        if float(top[metric]) < float(top[weakest]):
            weakest = metric

    st.subheader("Business interpretation")
    st.markdown(
        f"- **Which prompt performed best?** {top['Prompt ID']} ({top['Prompt Name']}).\n"
        f"- **Which metric was strongest?** {strongest} ({float(top[strongest]):.2f} / 5).\n"
        f"- **Which metric needs improvement?** {weakest} ({float(top[weakest]):.2f} / 5).\n"
        f"- **What should the operations user improve next?** {IMPROVEMENT_TIPS[weakest]}"
    )

    render_reset_section()


# ---------------------------------------------------------------
# 13. MAIN - builds the page shown for the selected menu item
# ---------------------------------------------------------------
def main():
    st.set_page_config(page_title="Prompt Evaluation & Optimization", page_icon="🧪", layout="wide")
    ensure_data_files()
    init_session()
    render_sidebar()

    # Short messages from the previous action (for example, "Saved new version").
    flash = st.session_state.get("flash")
    if flash:
        st.success(flash)
        del st.session_state["flash"]

    page = st.session_state["nav"]
    if page == "Home":
        page_home()
    elif page == "Prompt Library":
        page_library()
    elif page == "Run & Compare":
        page_run()
    elif page == "Manual Evaluation":
        page_evaluation()
    elif page == "Prompt Leaderboard":
        page_leaderboard()


main()
