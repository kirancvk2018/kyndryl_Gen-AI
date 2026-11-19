# Day 3 – Speech-to-Text Transcription Lab (OpenAI API)

**Module:** Day 3 – Module 03: Introduction to Large Language Models
**Topic:** Task-Based Text AI LLMs – Automatic Speech Recognition (ASR)

> Written for: lab facilitators and participants who will run the notebook.

## 1. Lab overview

This is a standalone practical lab. Participants convert a recorded IT infrastructure incident update into text with an OpenAI transcription model, using the OpenAI Python SDK in a Jupyter Notebook.

The lab covers audio-to-text conversion only. It does not cover incident ticket generation, RAG, LangChain, agents, the Realtime API or translation.

## 2. Learning outcomes

Participants will be able to:

1. Explain Speech-to-Text and Automatic Speech Recognition (ASR).
2. Load an audio file and check that it is valid.
3. Play a recording inside the notebook.
4. Connect to the OpenAI API with an API key kept out of the notebook.
5. Transcribe spoken English with the `gpt-transcribe` model.
6. Provide contextual hints (prompt, keywords and language) for technical terms.
7. Compare a transcript with and without hints.
8. Save transcripts and process another audio recording.

## 3. Business scenario

An IT operations professional receives a recording of an incident discussion or service desk call and needs a readable text record of it.

The sample recording, **"IT Infrastructure Incident Discussion"**, is a **simulated business scenario for training**. It contains no real incident, customer or personal data.

## 4. Technology stack

| Component | Purpose |
|---|---|
| Python 3.10 or newer | Programming language |
| `openai` (2.54.0 or newer) | Official OpenAI Python SDK, used to call `client.audio.transcriptions.create()` |
| `jupyter`, `ipykernel`, `ipython` | Notebook environment, Python kernel, audio playback and formatted output |
| `gpt-transcribe` | OpenAI model recommended for transcribing completed audio recordings |

No other services or frameworks are used.

## 5. Project structure

```text
DAY3_ASR_LAB/
├── day3_lab_speech_to_text.ipynb   the lab notebook (22 cells)
├── day3_asr_requirements.txt       the Python packages to install
├── DAY3_ASR_README.md              this document
├── DAY3_ASR_QUICKSTART.md          step-by-step guide for participants
├── sample_incident_audio.wav       the sample recording (about 49 seconds)
└── transcripts/                    created automatically when the notebook runs
```

## 6. Notebook execution sequence

Run the cells from top to bottom. Each section of the notebook maps to the cells below.

| Section | Topic | Calls the API? |
|---|---|---|
| 1 | Lab introduction (Markdown) | No |
| 2 | Environment setup: imports, `transcripts` folder, readiness message | No |
| 3 | OpenAI API configuration: API key, client, error messages | No (creates the client only) |
| 4–5 | Audio file checks and audio player | No |
| 6–7 | How the API works, then the first transcription | Yes, one request |
| 8–9 | Transcript counts, readable display, saving and reading back | No |
| 10 | Transcription context, keywords and language settings | No |
| 11–12 | Transcription with hints, then side-by-side comparison | Yes, one request |
| 13–14 | Your own recording and language settings | Yes, only if your file is found |
| 15 | Complete workflow function, run once on the sample | Yes, one request |
| 16–17 | Knowledge check, summary and troubleshooting (Markdown) | No |

Sections 7, 11 and 15 each send the same sample recording to OpenAI. Section 13 sends your own file.

## 7. OpenAI API integration

**Requirements:** an OpenAI API platform account and an API key. The key is separate from a ChatGPT subscription.

**Key handling:** the notebook reads the key from the environment variable `OPENAI_API_KEY`. If the variable is not set, it asks for the key in a hidden input box. The key is never printed and is never written into the notebook.

**The core call:**

```python
with open("sample_incident_audio.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="gpt-transcribe",
        file=audio_file,
    )
text = transcription.text
```

**Parameters used with `gpt-transcribe`:** `model`, `file`, `prompt`, `keywords` and `languages`.

- `keywords` and `languages` are passed as named arguments. These arguments exist in the `openai` 2.54.0 SDK, which is why the requirement is `openai>=2.54.0`. The OpenAI guide shows these two options passed through `extra_body`; the notebook does not need that.
- `languages` (plural) is used. The singular `language` option is not sent with `gpt-transcribe`, because the documentation says not to send both.

**Not used, on purpose:**
- `whisper-1` and the other older speech models, which are deprecated.
- The audio translations endpoint.
- The Realtime API, because this lab processes an existing recording.
- Third-party transcription services.

**File limits:** up to 25 MB per file. Accepted formats: FLAC, MP3, MP4, MPEG, MPGA, M4A, OGG, WAV and WebM.

**Official documentation:**
- https://developers.openai.com/api/docs/guides/speech-to-text
- https://developers.openai.com/api/reference/python/resources/audio/subresources/transcriptions/methods/create

## 8. Transcription context

The notebook uses three settings in Section 10. Each one is guidance for speech recognition, not a chat question.

| Setting | Sent as | Purpose |
|---|---|---|
| `TRANSCRIPTION_CONTEXT` | `prompt` | Describes the recording and its terminology |
| `TECHNICAL_KEYWORDS` | `keywords` | Lists exact terms expected in the audio |
| `LANGUAGE_CODE` | `languages` | Names the spoken language (`"en"`). Leave empty for automatic detection |

Hints can help, make no difference, or cause new mistakes. Section 12 asks participants to compare the two results.

**Note for this sample:** the recording does not mention PostgreSQL, Kubernetes, VPN, DNS or firewall. If those words appear in the context-assisted transcript, the hints have caused words that were never spoken to be written. This is a useful lesson in checking results.

## 9. Output files

| File | Created by | Behaviour when run again |
|---|---|---|
| `transcripts/incident_transcript.txt` | Section 9 | Replaced with the new transcript |
| `transcripts/incident_transcript_with_context.txt` | Section 11 | Replaced with the new transcript |
| `transcripts/<file name>_workflow_<date_time>.txt` | Section 15 | New file each run |
| `transcripts/custom_<file name>_<date_time>.txt` | Section 13 (own recording) | New file each run; never overwrites |

The two sample transcript files are regenerated from the same recording. Participant transcripts always get unique names, so earlier results are kept.

## 10. Sample recording

`sample_incident_audio.wav` was generated from the supplied training script with the Windows built-in speech synthesis engine (Microsoft Zira voice). It is a WAV file of about 49 seconds, mono, 22,050 Hz, 16-bit, about 2 MB. It is a computer-generated voice, not a human recording.

## 11. Troubleshooting

| Message or symptom | Likely cause and fix |
|---|---|
| `CONFIGURATION REQUIRED: no API key` | `OPENAI_API_KEY` is not set. Set it (see the Quickstart), restart Jupyter and run the notebook again from the top. |
| `The API key was rejected` | The key is wrong, revoked or from another account. Create a new key on the OpenAI API platform. |
| `Could not reach OpenAI` | No internet connection, or a firewall or proxy blocks the request. Check the connection and try again. |
| `OpenAI returned an error (status ...)` | Read the message shown. Rate limits and temporary service problems can be resolved by running the cell again later. |
| `FILE NOT FOUND` | The audio file is not in the notebook folder, or the name is wrong (names are case-sensitive on some systems). |
| `UNSUPPORTED FORMAT` | Convert the recording to MP3 or WAV. |
| `FILE TOO LARGE` | The file is over 25 MB. Compress it or split it into shorter files. |
| `No API key available` in later cells | Section 3 did not complete. Run Section 3 first. |
| `pip install` fails | Check that Python 3.10 or newer is installed and that the terminal is in the project folder. |
| Environment variable not found after `setx` | Close and reopen the terminal and VS Code, then start Jupyter again. |
| Transcript differs slightly from the script | Expected. Speech models can change punctuation, numbers and wording. Check the transcript against what you heard. |
| The notebook cannot find the sample file | Keep the notebook and `sample_incident_audio.wav` in the same folder, and start Jupyter from that folder. |

The notebook shows short messages by design. It does not display full technical stack traces.

## 12. Security notes

- Never put an API key into a notebook cell, a file in the project folder, a shared document or an email.
- Do not distribute `.env` files or any file that contains credentials.
- The project folder contains no credentials. Each participant supplies their own key.
