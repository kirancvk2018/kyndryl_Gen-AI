# Module 6 Lab 3: Conversational Chain for Corporate Operations

## 📋 Overview

This lab teaches you how to build a **two-step conversational chain** with LangChain. The chain keeps the conversation history across turns and helps with routine corporate operations tasks.

**Key Difference from Lab 2:**
- **Lab 2:** Sequential chain (stateless, single pass)
- **Lab 3:** Conversational chain (two steps, keeps history across turns)

## 🎯 Learning Objectives

By completing this lab, you will understand:
- ✅ Keeping conversation history in a list of messages
- ✅ Multi-turn conversational flows
- ✅ `MessagesPlaceholder` for injecting history into prompts
- ✅ Chaining a prompt with a model (`prompt | llm`)
- ✅ Two-step workflow: Diagnosis → Solution
- ✅ Saving a conversation transcript

## 📚 Use Case: Routine Corporate Operations

**Problem:**
- Routine operations issues need back-and-forth questions before anyone can act
- Staff gather the same information again and again
- Follow-up messages are slow when nobody has the full history

**Solution:**
- A diagnosis step asks clarifying questions over several turns
- The history is kept between turns
- A solution step reads the whole conversation and writes an action plan

Example areas:
- IT service desk (account lockouts, storage, reports)
- Finance operations (invoice approval backlogs)
- HR onboarding (new hire equipment and access)
- Business operations (scheduled reports that did not run)

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│    Staff member describes an issue   │
│    "Employee cannot log in"          │
└────────────────┬─────────────────────┘
                 │
                 ▼
    ╔════════════════════════════════╗
    ║  STEP 1: DIAGNOSIS CHAIN       ║
    ║  (multi-turn)                  ║
    ║  Turn 1: asks a clarifying Q   ║
    ║  Turn 2: refines the picture   ║
    ║  Turn 3: narrows the cause     ║
    ║  History is kept between turns ║
    ╚────────────────┬───────────────╝
                     │ (full history)
                     ▼
    ╔════════════════════════════════╗
    ║  STEP 2: SOLUTION CHAIN        ║
    ║  • Reads the whole history     ║
    ║  • Immediate and short-term    ║
    ║    actions                     ║
    ║  • Risks and fallback          ║
    ║  • How to confirm it is fixed  ║
    ╚────────────────┬───────────────╝
                     ▼
        ┌─────────────────────────┐
        │  Action plan            │
        └─────────────────────────┘
```

## 🔧 Key Components

### 1. Conversation History
```python
history = []   # list of HumanMessage / AIMessage objects
```
- Each turn appends the user message and the assistant reply
- The same list is passed to both chains

### 2. MessagesPlaceholder
```python
MessagesPlaceholder(variable_name="chat_history")
```
- Injects the history into the prompt
- The model sees earlier turns before it answers

### 3. Chain with History
```python
chain = prompt | llm
response = chain.invoke({"chat_history": history, "user_input": "CPU is at 95%"})
history.append(HumanMessage(content="CPU is at 95%"))
history.append(AIMessage(content=response.content))
```

### 4. Two Prompts

**Diagnosis Prompt:**
- Role: experienced corporate operations assistant
- Focus: ask one or two clarifying questions at a time
- Style: friendly, clear, practical

**Solution Prompt:**
- Role: senior operations manager
- Focus: practical action plan with urgent steps first
- Style: direct and easy to follow

## 📊 Data Structure

### Sample Conversations Format

```json
{
  "conversation_id": "CONV-001",
  "scenario": "Employee Account Lockout",
  "context": "Service desk handling a routine password and account access request",
  "conversation_history": [
    { "turn": 1, "role": "user", "message": "..." },
    { "turn": 2, "role": "assistant", "message": "..." },
    { "turn": 3, "role": "user", "message": "..." }
  ]
}
```

### 5 Sample Scenarios Included

1. **Employee Account Lockout** - IT service desk, password and access
2. **Month-End Invoice Processing Backlog** - Finance operations
3. **Shared Drive Storage Nearly Full** - Routine IT administration
4. **New Hire Laptop Setup Delay** - HR and IT onboarding
5. **Weekly Sales Report Not Generated** - Business operations

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements_module6_lab3.txt
```

### Step 2: Configure API Key
Create a `.env` file in the lab folder:
```
OPENAI_API_KEY=your_key_here
```

### Step 3: Run the Lab
```bash
# Interactive learning (recommended)
jupyter notebook module6_lab3_conversational_chain.ipynb

# Or run the script
python conversational_workflow.py
```

The script offers three modes:
1. Run a sample scenario (default)
2. Type your own issue
3. List the sample scenarios

## 💻 Usage Example

```python
from conversational_workflow import make_llm, make_diagnosis_chain, make_solution_chain, ask, SOLUTION_REQUEST

llm = make_llm()
diagnosis = make_diagnosis_chain(llm)
solution = make_solution_chain(llm)

history = []
print(ask(diagnosis, "Our invoice approvals are stuck at one manager", history))
print(ask(diagnosis, "That manager is on leave and nobody was reassigned", history))
print(ask(solution, SOLUTION_REQUEST, history))
```

## 📝 Expected Outputs

### Console Output
```
================================================================================
SCENARIO: Month-End Invoice Processing Backlog
================================================================================

[Turn 1 - USER]
We have about 400 supplier invoices waiting for approval...

[Turn 1 - ASSISTANT]
A backlog this size before close is a priority. Are the invoices stuck at one step?

[SOLUTION - reviewing 6 messages]
1. Immediate actions (next 30 minutes)
   • Reassign the approvals for the two managers on leave
   • Confirm which supplier payments are due this week
...
```

### Generated Files
- `conversation_transcript.json` - saved conversation history

## 🔄 Lab 2 vs Lab 3 Comparison

| Aspect | Lab 2 (Sequential) | Lab 3 (Conversational) |
|--------|-------------------|----------------------|
| **Memory** | ❌ None | ✅ Message list kept across turns |
| **History** | ❌ No history | ✅ Full context maintained |
| **Multi-turn** | ❌ Single pass | ✅ Multiple turns |
| **Stateless** | ✅ Yes | ❌ No (stateful) |
| **Steps** | 4 | 2 (Diagnosis → Solution) |
| **Best For** | One-shot analysis | Routine issues that need follow-up questions |

## 📚 Key Concepts

### Conversation History
- Stores every message in order
- Simple and easy to inspect
- Good for moderate-length conversations

### Message Types in History
```python
for msg in history:
    print(msg.type)      # 'human' or 'ai'
    print(msg.content)   # the message text
```

## 🧪 Exercises

### Exercise 1: Your Own Scenario
Write a routine operations issue (for example, a printer offline for a whole floor) and run it through the diagnosis chain.

### Exercise 2: Conversation Depth
Compare the action plan after 2 user turns with the plan after 3 turns.

### Exercise 3: Modify the Prompts
Change the diagnosis prompt to ask more or fewer questions. Observe the difference.

### Exercise 4: Add a Third Step
Add a step that writes a short status update for managers, using the same history.

### Exercise 5: Shorten Long Histories
When the history gets long, keep only the last few turns and a short summary of the earlier ones.

## 🛠️ Customization Guide

### Change the Model
```python
llm = make_llm(model_name="gpt-4o", temperature=0.5)
```

### Change the Prompts
Edit `DIAGNOSIS_SYSTEM_PROMPT` or `SOLUTION_SYSTEM_PROMPT` at the top of `conversational_workflow.py`.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named langchain" | Run: `pip install -r requirements_module6_lab3.txt` |
| "API key not found" | Create `.env` with `OPENAI_API_KEY=...` |
| "Model does not remember earlier turns" | Pass the same `history` list to every `ask()` call |
| "MessagesPlaceholder not working" | Check that the placeholder name is `chat_history` in both the prompt and the `invoke` call |

## 📖 Related Topics

### Before This Lab
- ✅ Module 6 Lab 1: Simple LLM chain
- ✅ Module 6 Lab 2: Sequential chains

### After This Lab
- → Module 7 (RAG): Add company knowledge bases to conversations
- → Module 8 (Agents): Add tools that carry out approved actions
- → Module 10 (Safety): Add conversation filters
- → Module 11 (Capstone): Full integration

## ✅ Completion Checklist

- [ ] Explain how the conversation history is kept
- [ ] Build a prompt with `MessagesPlaceholder`
- [ ] Run a multi-turn conversation
- [ ] Use the same history for the solution step
- [ ] Save a conversation transcript
- [ ] Compare Lab 2 (sequential) with Lab 3 (conversational)
- [ ] Write your own operations scenario

## 🎉 Summary

You now have a simple conversational assistant for routine corporate operations that:
- ✅ Keeps context across turns
- ✅ Asks clarifying questions before suggesting a plan
- ✅ Gives an action plan based on the full conversation
- ✅ Saves a transcript for review
