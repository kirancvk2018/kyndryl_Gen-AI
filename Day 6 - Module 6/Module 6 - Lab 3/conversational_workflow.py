"""
Module 6 Lab 3: Conversational Chain for Corporate Operations
=============================================================

A simple two-step conversational chain for routine corporate operations
tasks (IT service desk, finance operations, HR onboarding, business reports):

1. Diagnosis step  - asks clarifying questions over several turns
2. Solution step   - reads the whole conversation and gives an action plan

Prerequisites:
- OpenAI API key (OPENAI_API_KEY in .env)
- LangChain and OpenAI libraries installed (see requirements_module6_lab3.txt)

Run:
    python conversational_workflow.py
"""

import json
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


# ============================================================================
# Prompts
# ============================================================================

DIAGNOSIS_SYSTEM_PROMPT = """You are an experienced corporate operations assistant.
You help staff with routine tasks such as IT support, finance operations,
HR onboarding and business reporting.

Your role is to:
1. Understand the operational issue the user describes
2. Ask one or two clarifying questions at a time
3. Identify likely causes
4. Judge the urgency and who is affected

Be friendly, clear and practical. Use the earlier messages in this conversation."""

SOLUTION_SYSTEM_PROMPT = """You are a senior operations manager who turns issues into clear action plans.

Your role is to:
1. Review the issue and the conversation so far
2. Give practical, step-by-step actions
3. Put the most urgent actions first
4. Note risks and a fallback option
5. Suggest how to confirm the issue is resolved

Be practical and decisive. Keep the answer easy to follow."""

SOLUTION_REQUEST = """Based on our conversation so far, give a short action plan with:
1. Immediate actions (next 30 minutes)
2. Short-term actions (today or this week)
3. Risks to consider
4. Fallback option
5. How we will confirm it is resolved"""


# ============================================================================
# Chain setup
# ============================================================================

def make_llm(model_name="gpt-4o-mini", temperature=0.7):
    """Create the chat model. The API key is read from the environment."""
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def make_diagnosis_chain(llm):
    """Prompt with system role, conversation history and the new user input."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", DIAGNOSIS_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}"),
    ])
    return prompt | llm


def make_solution_chain(llm):
    """Same idea as the diagnosis chain, with the solution request."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SOLUTION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}"),
    ])
    return prompt | llm


# ============================================================================
# Conversation helpers
# ============================================================================

def ask(chain, user_input, history):
    """Send one message through a chain and add both sides to the history list."""
    response = chain.invoke({"chat_history": history, "user_input": user_input})
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response.content))
    return response.content


def history_to_list(history):
    """Turn the message list into plain dictionaries that can be saved as JSON."""
    rows = []
    for i, msg in enumerate(history, 1):
        rows.append({"turn": i, "role": msg.type, "content": msg.content})
    return rows


def save_transcript(history, filename):
    """Save the conversation to a JSON file."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "total_messages": len(history),
        "conversation": history_to_list(history),
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nConversation saved to {filename}")


def load_samples(filepath="data/sample_conversations.json"):
    """Load the sample conversations from the JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["conversations"]


# ============================================================================
# Example runs
# ============================================================================

def run_sample(llm, sample):
    """Run one sample scenario: user turns through diagnosis, then the solution."""
    diagnosis = make_diagnosis_chain(llm)
    solution = make_solution_chain(llm)
    history = []

    print(f"\n{'=' * 80}")
    print(f"SCENARIO: {sample['scenario']}")
    print(f"{'=' * 80}")

    # Only the user turns are sent. Assistant turns come from the model itself.
    user_turns = [t["message"] for t in sample["conversation_history"] if t["role"] == "user"]

    for i, text in enumerate(user_turns, 1):
        print(f"\n[Turn {i} - USER]\n{text}")
        reply = ask(diagnosis, text, history)
        print(f"\n[Turn {i} - ASSISTANT]\n{reply}")

    print(f"\n[SOLUTION - reviewing {len(history)} messages]")
    plan = ask(solution, SOLUTION_REQUEST, history)
    print(plan)

    return history


def run_interactive(llm):
    """Let the user type their own operational issue and follow-up messages."""
    diagnosis = make_diagnosis_chain(llm)
    solution = make_solution_chain(llm)
    history = []

    print("\nDescribe your issue. Type 'solution' to get the action plan, or 'quit' to exit.\n")
    while True:
        text = input("You: ").strip()
        if text.lower() == "quit":
            break
        if text.lower() == "solution":
            print(f"\n{ask(solution, SOLUTION_REQUEST, history)}\n")
            break
        if text:
            print(f"\nAssistant: {ask(diagnosis, text, history)}\n")

    if history:
        save_transcript(history, "conversation_transcript.json")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("\nCorporate Operations Conversation Assistant\n")
    print("Choose mode:")
    print("1. Run a sample scenario (default)")
    print("2. Type your own issue")
    print("3. List sample scenarios only")

    choice = input("\nEnter choice (1, 2 or 3): ").strip() or "1"
    samples = load_samples()

    if choice == "3":
        for s in samples:
            print(f"{s['conversation_id']}: {s['scenario']} - {s['context']}")
    elif choice == "2":
        run_interactive(make_llm())
    else:
        try:
            llm = make_llm()
            history = run_sample(llm, samples[0])
            save_transcript(history, "conversation_transcript.json")
        except Exception as e:
            print(f"\nError: {e}")
            print("\nMake sure:")
            print("  1. OPENAI_API_KEY is set in .env")
            print("  2. All dependencies are installed")
            print("  3. The OpenAI API key is valid")
