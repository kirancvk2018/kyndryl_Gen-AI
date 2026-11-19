"""
Module 6 Lab 2 (Corporate Operations Variant)
=============================================

A sequential LangChain workflow that processes routine corporate operations
requests (supplies, badges, equipment faults, vendor invoices, meeting room
issues) in four steps:

1. Request summary      - what is being asked, category and priority
2. Cause and blockers   - likely reason for the issue and what is blocking it
3. Business impact      - who is affected and what happens if it is delayed
4. Action plan          - numbered next steps with an owner and a target time

Each step is a simple LCEL chain:  prompt | llm | StrOutputParser()
The output of each step is plain text and is passed to the next step.

Prerequisites:
- OPENAI_API_KEY set in a .env file or as an environment variable
- Packages from requirements_module6_lab2.txt

Example:
    python ops_workflow.py
"""

import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# ----------------------------------------------------------------------------
# Step 1: Prompt templates
# ----------------------------------------------------------------------------

SUMMARY_TEMPLATE = """You are an operations coordinator at a corporate office.
Read the routine operations request below.

Request type: {request_type}
Requester: {requester} ({department})
Details: {details}
Needed by: {due_date}

Answer in this format:
Summary: <two sentences describing the request>
Category: <one of: Facilities, IT Access, Supplies, Equipment, Vendor, Other>
Priority: <one of: High, Medium, Low>
"""

CAUSE_TEMPLATE = """You are an operations analyst. Using the request and summary below,
explain why the issue happened and what is blocking it from being resolved.

Request type: {request_type}
Details: {details}
Summary: {summary}

Answer in this format:
Likely cause: <one or two sentences>
Blockers:
- <blocker 1>
- <blocker 2>
Confidence: <High, Medium or Low>
"""

IMPACT_TEMPLATE = """You are an operations manager. Using the summary and likely cause below,
describe the business impact of this request if it is not resolved on time.

Summary: {summary}
Likely cause and blockers: {cause}
Needed by: {due_date}

Answer in this format:
Who is affected: <teams, people or customers>
Impact if delayed: <one or two sentences>
Cost level: <High, Medium or Low>
Deadline at risk: <Yes or No>
"""

ACTION_TEMPLATE = """You are a senior operations coordinator. Using the information below,
write a short action plan to resolve this request.

Request type: {request_type}
Summary: {summary}
Likely cause and blockers: {cause}
Business impact: {impact}
Needed by: {due_date}

Answer in this format:
Immediate (next 30 minutes):
1. <action> - Owner: <team>
Same day:
1. <action> - Owner: <team>
Follow-up to prevent recurrence:
1. <action> - Owner: <team>
"""


# ----------------------------------------------------------------------------
# Step 2: Build the chains
# ----------------------------------------------------------------------------

def build_chains(model_name="gpt-4o-mini", temperature=0.3):
    """Create the four LCEL chains. Returns a dictionary of chains."""
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    parser = StrOutputParser()

    summary_chain = PromptTemplate.from_template(SUMMARY_TEMPLATE) | llm | parser
    cause_chain = PromptTemplate.from_template(CAUSE_TEMPLATE) | llm | parser
    impact_chain = PromptTemplate.from_template(IMPACT_TEMPLATE) | llm | parser
    action_chain = PromptTemplate.from_template(ACTION_TEMPLATE) | llm | parser

    return {
        "summary": summary_chain,
        "cause": cause_chain,
        "impact": impact_chain,
        "action": action_chain,
    }


# ----------------------------------------------------------------------------
# Step 3: Run the sequential workflow
# ----------------------------------------------------------------------------

def analyze_request(chains, request):
    """Run the four steps in order. Each step uses the outputs of the steps before it."""
    request_id = request.get("request_id", "UNKNOWN")
    request_type = request.get("request_type", "")
    details = request.get("details", "")
    due_date = request.get("due_date", "")

    print(f"\nProcessing {request_id}: {request_type}")

    # Step 1: summary
    print("  [Step 1/4] Summarizing request...")
    summary = chains["summary"].invoke({
        "request_type": request_type,
        "requester": request.get("requester", ""),
        "department": request.get("department", ""),
        "details": details,
        "due_date": due_date,
    })

    # Step 2: cause and blockers (uses step 1)
    print("  [Step 2/4] Finding cause and blockers...")
    cause = chains["cause"].invoke({
        "request_type": request_type,
        "details": details,
        "summary": summary,
    })

    # Step 3: business impact (uses steps 1 and 2)
    print("  [Step 3/4] Assessing business impact...")
    impact = chains["impact"].invoke({
        "summary": summary,
        "cause": cause,
        "due_date": due_date,
    })

    # Step 4: action plan (uses steps 1, 2 and 3)
    print("  [Step 4/4] Writing action plan...")
    action_plan = chains["action"].invoke({
        "request_type": request_type,
        "summary": summary,
        "cause": cause,
        "impact": impact,
        "due_date": due_date,
    })

    return {
        "request_id": request_id,
        "request_type": request_type,
        "summary": summary,
        "cause": cause,
        "impact": impact,
        "action_plan": action_plan,
    }


# ----------------------------------------------------------------------------
# Step 4: Helper functions
# ----------------------------------------------------------------------------

def load_requests(filepath):
    """Load the list of requests from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("requests", [])


def format_report(result):
    """Turn one analysis result into a readable text report."""
    line = "=" * 70
    return (
        f"\n{line}\n"
        f"OPERATIONS REQUEST REPORT: {result['request_id']} - {result['request_type']}\n"
        f"{line}\n\n"
        f"1. SUMMARY\n{result['summary']}\n\n"
        f"2. CAUSE AND BLOCKERS\n{result['cause']}\n\n"
        f"3. BUSINESS IMPACT\n{result['impact']}\n\n"
        f"4. ACTION PLAN\n{result['action_plan']}\n"
        f"{line}\n"
    )


def save_results(results, output_file):
    """Save all analysis results to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {output_file}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    requests = load_requests("data/ops_requests.json")
    chains = build_chains(model_name="gpt-4o-mini", temperature=0.3)

    results = []
    for request in requests[:2]:  # First two requests for the demo; change as needed
        result = analyze_request(chains, request)
        results.append(result)
        print(format_report(result))

    save_results(results, "ops_analysis_results.json")
    print("\nAnalysis complete.")
