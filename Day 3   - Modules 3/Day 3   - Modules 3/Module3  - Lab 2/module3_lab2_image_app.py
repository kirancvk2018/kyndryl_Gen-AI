"""
Module 3, Lab 2: IT Infrastructure Image Analyzer
Streamlit web app that sends an infrastructure image to OpenAI GPT-4o Vision.

Workflow: Upload image -> Select category -> Analyze -> Review -> Download TXT
Results live only in the current browser session. There is no database.
"""

import base64
import logging
import os
from datetime import datetime
from io import BytesIO
from logging.handlers import RotatingFileHandler
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError
from PIL import Image

# ---------------------------------------------------------------------------
# 1. Environment configuration
# ---------------------------------------------------------------------------
# Read OPENAI_API_KEY from the .env file next to this script. Never hard-code the key.
load_dotenv(Path(__file__).with_name(".env"))

APP_TITLE = "IT Infrastructure Image Analyzer"
APP_SUBTITLE = (
    "Upload an infrastructure image and use Generative AI to identify "
    "components, potential issues and recommendations."
)
MODEL_NAME = "gpt-4o"
MAX_TOKENS = 1024
MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
# Pillow format name -> MIME type (also the list of formats we accept)
ALLOWED_FORMATS = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}

# ---------------------------------------------------------------------------
# 2. Logging configuration (writes to app.log in the project folder)
# ---------------------------------------------------------------------------
logger = logging.getLogger("module3_lab2")
# Streamlit re-runs this whole file on every click, so set up logging only once
if not logger.handlers:
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        Path(__file__).with_name("app.log"),
        maxBytes=1_000_000,  # start a new file after 1 MB
        backupCount=3,       # keep up to 3 old files
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(file_handler)
    logger.info("Application started")

# ---------------------------------------------------------------------------
# 3. Streamlit page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title=APP_TITLE, page_icon="🔍")

# ---------------------------------------------------------------------------
# 4. Analysis prompts (one per category; edit these to change the analysis)
# ---------------------------------------------------------------------------
ANALYSIS_PROMPTS = {
    "General": """Analyze this IT infrastructure image.
- Describe what the image shows.
- Identify the visible infrastructure components.
- Identify potential issues.
- Assess the overall condition.
- Provide recommendations.""",
    "Server Rack": """Analyze this server rack or data centre equipment image.
- Identify the visible equipment (servers, switches, storage, power units).
- Examine cable management.
- Assess power distribution.
- Examine cooling and ventilation.
- Identify potential risks.
- Recommend improvements.""",
    "Dashboard": """Analyze this monitoring dashboard screenshot.
- Identify the displayed metrics.
- Interpret the visible values.
- Identify abnormal trends.
- Identify alerts and anomalies.
- Recommend actions.""",
    "Network": """Analyze this network diagram or network equipment image.
- Identify the visible network components.
- Explain the apparent connectivity.
- Assess the visible topology.
- Identify potential bottlenecks.
- Identify possible failure points.
- Recommend improvements.""",
    "Error Log": """Analyze this error message or error log screenshot.
- Identify the error messages.
- Identify the affected components.
- Assess the severity (Low, Medium, High or Critical).
- Suggest possible causes.
- Recommend troubleshooting steps.""",
}

# Rules added to every category prompt (output layout and honesty)
OUTPUT_RULES = """
Format your answer in plain language with exactly these Markdown headings, in this order:
## Analysis Summary
## Key Observations
## Potential Issues
## Recommendations

Honesty rules:
- Mark statements you can directly see with "(Visible)" and statements you infer with "(Assumption)".
- Do not claim certainty about details you cannot read in the image, such as exact IP addresses, serial numbers or blurry values. Say "not clearly visible" instead.
- If the image is not an IT infrastructure image, say so in the Analysis Summary."""


def get_analysis_prompt(category):
    """Return the category prompt plus the shared output rules."""
    return ANALYSIS_PROMPTS[category] + "\n" + OUTPUT_RULES


# ---------------------------------------------------------------------------
# 5. Image validation
# ---------------------------------------------------------------------------
def validate_image(uploaded_file):
    """Check the file extension, size and real content. Returns (is_valid, message)."""
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False, "Unsupported file type. Please upload a JPG, JPEG, PNG or WEBP image."

    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, f"File is too large. The maximum size is {MAX_FILE_SIZE_MB} MB."

    # Check the actual content with Pillow, so a renamed text file is rejected
    try:
        image = Image.open(BytesIO(uploaded_file.getvalue()))
        image_format = image.format
        image.verify()
    except Exception:
        return False, "This file could not be read as an image. It may be corrupted."

    if image_format not in ALLOWED_FORMATS:
        return False, f"The file contains a {image_format} image, which is not supported."

    return True, "Valid image"


# ---------------------------------------------------------------------------
# 6. OpenAI analysis (exactly one API call per analysis)
# ---------------------------------------------------------------------------
def analyze_image_with_openai(image_bytes, category):
    """Send the image and category prompt to GPT-4o.
    Returns (analysis_text, error_message). One of the two is always None."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        logger.error("OPENAI_API_KEY is missing; add it to the .env file")
        return None, "OPENAI_API_KEY is missing. Copy .env.example to .env, add your key and restart the app."

    # Encode the image as a data URL that the API accepts
    image_format = Image.open(BytesIO(image_bytes)).format
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:{ALLOWED_FORMATS[image_format]};base64,{image_b64}"

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": get_analysis_prompt(category)},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
        )
    except AuthenticationError:
        logger.error("OpenAI authentication failed; check OPENAI_API_KEY")
        return None, "Authentication failed. Check that OPENAI_API_KEY in your .env file is correct."
    except RateLimitError:
        logger.error("OpenAI rate limit or quota reached")
        return None, "Rate limit or quota reached. Wait a minute, then try again."
    except APIConnectionError:
        logger.error("Network error while contacting the OpenAI API")
        return None, "Network error. Check your internet connection and try again."
    except APIError as error:
        logger.error("OpenAI API error: %s", type(error).__name__)
        return None, "The OpenAI API returned an error. Please try again later."
    except Exception:
        logger.exception("Unexpected error during analysis")
        return None, "An unexpected error occurred. Details were written to app.log."

    # Check that the response actually contains text
    text = response.choices[0].message.content if response.choices else None
    if not text:
        logger.error("OpenAI returned an empty response")
        return None, "The API returned an empty response. Please try again."

    logger.info("Analysis completed successfully (%d characters)", len(text))
    return text, None


# ---------------------------------------------------------------------------
# 7. Main Streamlit application
# ---------------------------------------------------------------------------
def main():
    st.title(APP_TITLE)
    st.write(APP_SUBTITLE)

    # Step 1: upload and preview the image
    uploaded_file = st.file_uploader(
        "Upload an infrastructure image",
        type=["jpg", "jpeg", "png", "webp"],
        help=f"JPG, JPEG, PNG or WEBP. Maximum size {MAX_FILE_SIZE_MB} MB.",
    )

    is_valid = False
    if uploaded_file is not None:
        is_valid, message = validate_image(uploaded_file)

        # Log each new upload once, not on every re-run
        upload_key = (uploaded_file.name, uploaded_file.size)
        if st.session_state.get("last_upload") != upload_key:
            st.session_state["last_upload"] = upload_key
            logger.info("Image uploaded: %s (%d bytes)", uploaded_file.name, uploaded_file.size)
            if is_valid:
                logger.info("Image validation passed: %s", uploaded_file.name)
            else:
                logger.warning("Image validation failed: %s - %s", uploaded_file.name, message)

        if is_valid:
            image = Image.open(BytesIO(uploaded_file.getvalue()))
            st.image(image, caption=uploaded_file.name)
            st.write(
                f"**Filename:** {uploaded_file.name}  \n"
                f"**Dimensions:** {image.width} x {image.height} px  \n"
                f"**File size:** {uploaded_file.size / 1024:,.1f} KB"
            )
        else:
            st.error(message)

    # Step 2: choose the analysis category
    category = st.selectbox("Analysis category", list(ANALYSIS_PROMPTS))

    # Step 3: analyze (one API call per click)
    if st.button("Analyze Image", type="primary"):
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        elif not is_valid:
            st.error("Please upload a valid image before analyzing.")
        else:
            logger.info("Selected analysis category: %s", category)
            logger.info("Analysis started for image: %s", uploaded_file.name)
            with st.spinner("Analyzing image with GPT-4o..."):
                analysis, error = analyze_image_with_openai(uploaded_file.getvalue(), category)

            if error:
                st.session_state.pop("result", None)
                st.error(error)
            else:
                # Keep the result in session memory only (not saved to disk)
                st.session_state["result"] = {
                    "filename": uploaded_file.name,
                    "category": category,
                    "timestamp": datetime.now(),
                    "text": analysis,
                }

    # Step 4: show the latest result
    result = st.session_state.get("result")
    if result:
        st.subheader("Analysis Results")
        st.caption(
            f"Image: {result['filename']} | Category: {result['category']} | "
            f"Analysed: {result['timestamp']:%Y-%m-%d %H:%M:%S}"
        )
        st.markdown(result["text"])

        # Step 5: download the report as a TXT file
        report = (
            "IT Infrastructure Image Analysis\n"
            "=================================\n"
            f"Image filename: {result['filename']}\n"
            f"Analysis category: {result['category']}\n"
            f"Analysis date and time: {result['timestamp']:%Y-%m-%d %H:%M:%S}\n\n"
            "Generated analysis\n"
            "------------------\n"
            f"{result['text']}\n"
        )
        category_slug = result["category"].lower().replace(" ", "_")
        file_name = f"analysis_{category_slug}_{result['timestamp']:%Y%m%d_%H%M%S}.txt"
        st.download_button(
            "Download Analysis (TXT)",
            data=report,
            file_name=file_name,
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
