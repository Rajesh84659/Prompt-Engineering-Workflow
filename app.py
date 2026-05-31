import streamlit as st
import os
import json
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Prompt Engineering Workflow",
    layout="wide"
)

st.title("Prompt Engineering Workflow Evaluation System")

st.markdown("""
This application demonstrates:
- Prompt Engineering
- AI Response Generation
- Automated AI Evaluation
- Output Comparison
""")

# ---------------------------------------------------
# FOLDER PATHS
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROMPT_FOLDER = os.path.join(BASE_DIR, "prompts")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
EVALUATION_FOLDER = os.path.join(BASE_DIR, "evaluations")
# ---------------------------------------------------
# GET ALL PROMPT FILES
# ---------------------------------------------------

prompt_files = sorted([
    file for file in os.listdir(PROMPT_FOLDER)
    if file.endswith(".txt")
])

# ---------------------------------------------------
# PROCESS EACH PROMPT
# ---------------------------------------------------

for prompt_file in prompt_files:

    # Extract version name
    version_name = prompt_file.replace(".txt", "")

    st.divider()

    st.header(f"{version_name.upper()}")

    # ---------------------------------------------------
    # READ PROMPT
    # ---------------------------------------------------

    prompt_path = os.path.join(
        PROMPT_FOLDER,
        prompt_file
    )

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_text = file.read()

    st.subheader("Prompt")

    st.code(prompt_text)

    # ---------------------------------------------------
    # READ OUTPUT
    # ---------------------------------------------------

    output_filename = prompt_file.replace(
        "prompt",
        "output"
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    if os.path.exists(output_path):

        with open(output_path, "r", encoding="utf-8") as file:
            output_text = file.read()

        st.subheader("Generated Output")

        st.write(output_text)

    else:
        st.warning(f"{output_filename} not found.")

    # ---------------------------------------------------
    # READ EVALUATION JSON
    # ---------------------------------------------------

    evaluation_filename = prompt_file.replace(
        "prompt",
        "evaluation"
    ).replace(".txt", ".json")

    evaluation_path = os.path.join(
        EVALUATION_FOLDER,
        evaluation_filename
    )

    if os.path.exists(evaluation_path):

        with open(evaluation_path, "r", encoding="utf-8") as file:
            evaluation_data = json.load(file)

        st.divider()

        st.subheader("Evaluation Report")

        # Separate comments from scores
        scores = {}
        comments = ""

        for key, value in evaluation_data.items():

            if key == "Overall_Comments":
                comments = value

            else:
                scores[key] = value

        # Convert scores into dataframe
        df = pd.DataFrame({
            "Metric": list(scores.keys()),
            "Score": list(scores.values())
        })

        st.table(df)

        # Display comments
        st.subheader("Evaluator Comments")

        st.info(comments)

    else:
        st.warning(f"{evaluation_filename} not found.")

# ---------------------------------------------------
# OVERALL COMPARISON SECTION
# ---------------------------------------------------

st.divider()

st.header("Overall Prompt Comparison")

comparison_data = []

for prompt_file in prompt_files:

    evaluation_filename = prompt_file.replace(
        "prompt",
        "evaluation"
    ).replace(".txt", ".json")

    evaluation_path = os.path.join(
        EVALUATION_FOLDER,
        evaluation_filename
    )

    if os.path.exists(evaluation_path):

        with open(evaluation_path, "r", encoding="utf-8") as file:
            evaluation_data = json.load(file)

        row = {
            "Version": prompt_file.replace(".txt", "")
        }

        for key, value in evaluation_data.items():

            if key != "Overall_Comments":
                row[key] = value

        comparison_data.append(row)

# Create comparison dataframe
if comparison_data:

    comparison_df = pd.DataFrame(comparison_data)

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

else:
    st.warning("No evaluation data available.")