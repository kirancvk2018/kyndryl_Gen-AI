# Module 6, Lab 1: LangChain Basics
## Simple LLM App for Routine Corporate Operations

**Version:** 2.0
**Duration:** 2-3 hours
**Level:** Beginner

---

## Overview

This lab introduces LangChain, a Python framework for building apps with Large Language Models (LLMs). You build small AI helpers for everyday office and operations work: shift handovers, helpdesk ticket triage, meeting action items and status emails.

The code uses plain Python: functions, dictionaries and files. There are no classes and no Pydantic models.

### What you will learn
- The LangChain building blocks and the `prompt | llm | parser` pattern
- How to start a chat model with settings from `.env`
- Prompt templates for office tasks
- Single-step and multi-step chains
- Parsing JSON output, with a fallback when the reply is not valid
- Running a batch of tickets and saving the results

### What you will build
- A shift handover summary
- A multi-step list of next-shift tasks
- A helpdesk ticket triage that sorts tickets into teams with a priority
- A meeting status email

---

## Prerequisites

- Python 3.10 or higher
- pip
- An OpenAI API key
- Sample data only. Do not paste real employee, customer or financial records into the prompts.

**Estimated cost:** a few cents for the whole lab, using `gpt-4o-mini`.

---

## Installation

### Step 1: Install the packages
```bash
pip install -r lab1_m6_requirements.txt
pip install jupyter
```

### Step 2: Add your API key
Open `.env` in this folder and set the key on the `OPENAI_API_KEY=` line:
```
OPENAI_API_KEY=sk-your-key-goes-here
OPENAI_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
MAX_TOKENS=1000
```

To keep a private copy of the settings, copy `.env_lab1_m6_example` to `.env_lab1_m6` and fill it in. The notebook reads `.env_lab1_m6` first, then `.env`.

### Step 3: Open the notebook
```bash
jupyter notebook module6_lab1_langchain_basics.ipynb
```

---

## Files

```
Module 6 - Lab 1/
├── module6_lab1_langchain_basics.ipynb   # Main notebook (12 sections)
├── lab1_m6_requirements.txt              # Python packages
├── .env                                  # Your settings and API key (keep private)
├── .env_lab1_m6_example                  # Settings template
├── data/
│   ├── sample_tickets.json               # 8 office and IT tickets
│   ├── sample_shift_notes.txt            # Night-shift handover log
│   └── sample_meeting_notes.txt          # Weekly operations meeting notes
└── docs/
    ├── MODULE6_LAB1_README.md            # This guide
    ├── LAB1_M6_QUICKSTART.md             # Five-minute start
    ├── LAB1_M6_MANIFEST.txt              # File list
    └── MODULE6_LAB1_DELIVERY_SUMMARY.txt # Delivery notes
```

When Section 11 runs, the notebook creates an `output` folder with `ticket_triage.json`.

---

## Lab Structure

| Section | Topic | Time |
|---|---|---|
| 1 | Setup and installation | 5 min |
| 2 | How the pieces fit together | 10 min |
| 3 | Working with the LLM | 15 min |
| 4 | Prompt templates | 20 min |
| 5 | Chains (`prompt \| llm \| parser`) | 15 min |
| 6 | Multi-step chain | 15 min |
| 7 | Output parsing (JSON with a fallback) | 15 min |
| 8 | Hands-on exercise: meeting status email | 20 min |
| 9 | Best practices and tips | 10 min |
| 10 | Routine-operations patterns | 10 min |
| 11 | Complete example: batch ticket triage | 20 min |
| 12 | Summary and next steps | 5 min |

Run every cell from top to bottom. Do not skip cells.

---

## Key Concepts

### Chat model
`ChatOpenAI` sends a request to the model and returns its reply. The lab reads the model name, temperature and token limit from `.env`.

### Prompt template
A reusable instruction with blanks, such as `{ticket_text}`. The blanks are filled in when the chain runs.

### Chain
A chain connects a prompt, the model and a parser:
```python
chain = prompt | llm | StrOutputParser()
```
The output of one chain can be passed to the next one, as in Section 6.

### Output parser
`StrOutputParser` returns plain text. The lab's `parse_json_reply()` function reads JSON, removes code fences, and returns `None` if the reply is not valid JSON.

---

## Configuration

| Setting | Default in code | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | none (required) | Your private key |
| `OPENAI_MODEL` | `gpt-4o-mini` | The model that answers |
| `LLM_TEMPERATURE` | `0.2` (`0.7` in the `.env` template) | Lower values give more consistent answers |
| `MAX_TOKENS` | `1000` | Longest reply the model may write |

---

## Sample Data

- **`data/sample_tickets.json`:** eight office and IT tickets, such as a locked account, a broken air conditioner, an expense query and a past-due invoice.
- **`data/sample_shift_notes.txt`:** one night shift's log, with pending items for the day shift.
- **`data/sample_meeting_notes.txt`:** one weekly operations meeting, with actions for Facilities, Finance, IT and Procurement.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "No module named 'langchain'" | Run `pip install -r lab1_m6_requirements.txt` again |
| "401" or "Incorrect API key" | Copy the key into `.env` again, on the same line, with no spaces or quotes |
| "404" or "model does not exist" | Set `OPENAI_MODEL=gpt-4o-mini` in `.env`, then restart the kernel (Kernel > Restart & Run All) |
| "429" or quota or billing errors | Your OpenAI account has no credit or has hit a limit. Ask your facilitator |
| Triage output is not valid JSON | The cell prints the raw reply and the batch marks that ticket as UNPARSED. Run again, or lower `LLM_TEMPERATURE` |
| Notebook shows old results | Kernel > Restart & Run All |

---

## Verification Checklist

- [ ] Packages installed without errors
- [ ] `OPENAI_API_KEY` set in `.env`
- [ ] Section 3 returns an answer
- [ ] Section 5 returns a shift handover summary
- [ ] Section 7 parses a triage reply (or shows a clear fallback)
- [ ] Section 11 saves `output/ticket_triage.json`
- [ ] I can explain the `prompt | llm | parser` pattern

---

## Next Steps

1. Finish all notebook sections in order.
2. Do the Section 8 exercise and compare the two emails.
3. Change the triage prompt to add a new team, and run Section 11 again.
4. Continue to:
   - **Lab 2:** sequential chains for routine operations requests (four steps)
   - **Lab 3:** conversational chains for routine operations issues (diagnosis, then an action plan)

---

## Notes for Instructors

1. Run the first two sections together so that trainees see a working API call early.
2. Most setup problems are API key problems. Check the `.env` line first.
3. Section 8 is the main exercise. Trainees who finish early can add a second output format.
4. Remind trainees to use sample data only.

---

## Support

1. Check the Troubleshooting table above.
2. Read the error message in full.
3. Check the OpenAI status page if calls fail for everyone.
4. Test with one ticket before running the batch.

When you report a problem, include the Python version, the output of `pip list | findstr langchain`, and the full error message.

---

## License and Attribution

This lab is part of the 11-day Generative AI Training Program.

**Changelog:**
- v2.0: Corporate operations use case. Replaced IT incident examples with office and operations examples. Removed the Pydantic requirement and the Python class. Model default changed to `gpt-4o-mini`.
- v1.0 (2024-08-03): Initial release (IT operations examples).

---

**Summary:** Lab 1 introduces the LangChain basics through routine corporate tasks. You build prompts, chains and a batch triage, and you learn to check the output of an AI model before you act on it.
