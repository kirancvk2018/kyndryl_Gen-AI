# Module 6 Lab 3: Conversational Chain for Corporate Operations - Deliverables

## 📦 Files

### Core Lab Files
| File | Purpose |
|------|---------|
| **module6_lab3_conversational_chain.ipynb** | Step-by-step notebook for routine corporate operations |
| **conversational_workflow.py** | Script with plain functions (no classes, no Pydantic) |
| **data/sample_conversations.json** | 5 corporate operations scenarios, 3 turns each |
| **requirements_module6_lab3.txt** | Python dependencies (unchanged) |

### Documentation (folder docs/)
| File | Purpose |
|------|---------|
| **MODULE6_LAB3_README.md** | Guide and reference |
| **LAB3_DELIVERABLES_SUMMARY.md** | This file |

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements_module6_lab3.txt

# 2. Set up API key in .env
OPENAI_API_KEY=your_key_here

# 3. Run the lab
# Interactive: jupyter notebook module6_lab3_conversational_chain.ipynb
# Script:      python conversational_workflow.py
```

---

## 🎯 What You Will Learn
- Keeping conversation history with a message list
- `MessagesPlaceholder` for injecting history into prompts
- Chaining a prompt with a model (`prompt | llm`)
- Multi-turn conversations for routine operations issues
- Two-step workflow: diagnosis → solution
- Saving a conversation transcript

---

## 💾 Sample Scenarios (data/sample_conversations.json)

1. **CONV-001: Employee Account Lockout** - IT service desk
2. **CONV-002: Month-End Invoice Processing Backlog** - Finance operations
3. **CONV-003: Shared Drive Storage Nearly Full** - Routine IT administration
4. **CONV-004: New Hire Laptop Setup Delay** - HR and IT onboarding
5. **CONV-005: Weekly Sales Report Not Generated** - Business operations

Each scenario has:
- Three turns (user → assistant → user)
- Routine, realistic operations details

---

## 🔑 Code Structure (conversational_workflow.py)

Plain functions only:
- `make_llm()` - creates the chat model
- `make_diagnosis_chain(llm)` / `make_solution_chain(llm)` - build the two chains
- `ask(chain, text, history)` - runs one turn and updates the history
- `save_transcript(history, filename)` - saves the transcript as JSON
- `load_samples()` - loads the sample scenarios
- `run_sample()` / `run_interactive()` - the two run modes

---

## 🧪 Lab Structure (Notebook)
- Part 1: Setup
- Part 2: Conversation memory
- Part 3: System prompts
- Part 4: Build the chains
- Part 5: Helper function
- Part 6: Load a sample scenario
- Part 7: Multi-turn diagnosis
- Part 8: Solution step
- Part 9: Review and save the transcript
- Part 10: Run another scenario
- Part 11: Key concepts
- Part 12: Exercises

---

## 📖 Next Steps
→ **Module 7 (RAG):** Add company knowledge bases to conversations
→ **Module 8 (Agents):** Add tools that carry out approved actions
→ **Module 10 (Safety):** Add safety filters and validation
→ **Module 11 (Capstone):** Integrate conversational and agentic workflows
