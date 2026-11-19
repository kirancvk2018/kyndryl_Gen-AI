# Module 6, Lab 1: Quick Start Guide
## Your First LangChain App for Routine Corporate Operations

---

## Setup (about 5 minutes)

### Step 1: Install the packages
```bash
pip install -r lab1_m6_requirements.txt jupyter
```

### Step 2: Add your API key
The file `.env` in this folder holds your settings. Open it and put your key on the `OPENAI_API_KEY=` line, with no spaces and no quotation marks.

```
OPENAI_API_KEY=sk-your-key-goes-here
OPENAI_MODEL=gpt-4o-mini
```

### Step 3: Open the notebook
```bash
jupyter notebook module6_lab1_langchain_basics.ipynb
```

Run every cell from top to bottom with **Shift+Enter**.

---

## First Program (2 minutes)

Create a file named `first_reminder.py` in this folder, or paste the code into a notebook cell:

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)

prompt = PromptTemplate.from_template(
    "Write a two-sentence reminder for staff about this task: {task}"
)

chain = prompt | llm | StrOutputParser()
print(chain.invoke({"task": "Submit expense reports by Friday"}))
```

Run it with `python first_reminder.py`.

---

## Common Tasks

### Task 1: Summarize a shift handover
```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Summarize these shift notes for the next shift. Give open issues and next actions.\n\n{notes}"
)
chain = prompt | llm | StrOutputParser()

with open("data/sample_shift_notes.txt", encoding="utf-8") as f:
    print(chain.invoke({"notes": f.read()}))
```

### Task 2: Triage one ticket
```python
prompt = PromptTemplate.from_template(
    "Classify this office or IT ticket. Return ONLY a JSON object with keys "
    '"team" (IT, Facilities, HR, or Finance), "priority" (Low, Medium, or High) '
    'and "reason".\n\nTicket: {ticket}'
)
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"ticket": "Air conditioning on floor 3 is broken."}))
```

### Task 3: Turn meeting notes into a status email
```python
prompt = PromptTemplate.from_template(
    "Write a short status email from these meeting notes. Start with a subject line.\n\n{notes}"
)
chain = prompt | llm | StrOutputParser()

with open("data/sample_meeting_notes.txt", encoding="utf-8") as f:
    print(chain.invoke({"notes": f.read()}))
```

---

## Key Concepts

### Prompt template
A reusable instruction with blanks, such as `{ticket}`. Fill the blanks when you run the chain.

### Chain: `prompt | llm | parser`
The prompt is sent to the model. The parser turns the reply into plain text. Each `|` passes the output of one step to the next.

```python
chain = your_prompt | your_llm | StrOutputParser()
result = chain.invoke({"variable": "value"})
```

### Several steps
Pass the output of one chain into the next:
```python
summary = handover_chain.invoke({"notes": notes})
tasks = action_chain.invoke({"summary": summary})
```

---

## Sample Data

| File | Used for |
|---|---|
| `data/sample_tickets.json` | Batch ticket triage (Section 11) |
| `data/sample_shift_notes.txt` | Shift handover summary (Sections 5 and 6) |
| `data/sample_meeting_notes.txt` | Status email exercise (Section 8) |

To load the tickets:
```python
import json

with open("data/sample_tickets.json", encoding="utf-8") as f:
    tickets = json.load(f)["tickets"]

for ticket in tickets:
    print(ticket["id"], ticket["text"])
```

---

## Success Checklist

- [ ] Packages installed
- [ ] `OPENAI_API_KEY` set in `.env`
- [ ] Notebook opens in Jupyter
- [ ] The first AI call returns an answer
- [ ] I ran a shift handover chain
- [ ] I ran the ticket triage and saw `output/ticket_triage.json`

---

## Quick Fixes

| Problem | Fix |
|---|---|
| "No module named 'langchain'" | Run `pip install -r lab1_m6_requirements.txt` again |
| 401 or "Incorrect API key" | Copy the key again into `.env`, with no spaces |
| 404 or "model does not exist" | Set `OPENAI_MODEL=gpt-4o-mini` in `.env`, then restart the notebook kernel |
| 429 or "quota" | Your OpenAI account needs credit or a higher limit. Ask your facilitator |
| Triage reply is not valid JSON | The cell keeps the raw reply. Run it again or lower `LLM_TEMPERATURE` in `.env` |

---

## Next

- Complete all notebook sections
- Do the Section 8 exercise
- Try your own routine task, such as a weekly report or a vendor invoice reminder
- Move to Lab 2 (sequential chains for routine requests)

**Questions?** See `MODULE6_LAB1_README.md`.
