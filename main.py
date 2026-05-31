from google import genai
from dotenv import load_dotenv
import os
import json

# Load .env variables
load_dotenv()

# Get API key
API_KEY =  os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key= API_KEY)

# Folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

prompt_folder = os.path.join(BASE_DIR, "prompts")
output_folder = os.path.join(BASE_DIR, "outputs")
evaluation_folder = os.path.join(BASE_DIR, "evaluations")

# Traverse Each Prompt File
for file_name in os.listdir(prompt_folder):
    if file_name.endswith('.txt'):
        prompt_path = os.path.join(prompt_folder, file_name)

        # Open prompt
        with open(prompt_path, 'r', encoding= 'utf-8') as f:
            prompt = f.read()

        # Generate Response
        response = client.models.generate_content(model="gemini-3.5-flash", contents= prompt)

        output_text = response.text
        #print(output_text)

        # Create Output Filename
        base_name = file_name.replace(".txt", "")
        output_file = base_name.replace(
            "prompt",
            "output"
        ) + ".txt"
        
        output_path = os.path.join(output_folder, output_file)

        # Save Output File
        with open(output_path, 'w', encoding= 'utf-8') as f:
            f.write(output_text)
        
        print(f"Output Response is stored sucessfully in {output_file}")

        # Create Evaluation Prompt
        evaluation_prompt = f"""
Role : You are an AI Response Evaluator with 5 years of Experience. You are very good in giving scores according to the Metrics defined for the AI Response
Task : You need to Evaluate the following AI Generated Response. 
########################
Response :
{output_text}
########################
Evaluate using these Metrics:
1. Clarity
2. Accuracy
3. Structure 
4. Beginner-Friendly
5. Examples
6. Overall Comments
Give Score out of 10
Context : For Better Evaluation Process, i will explain the terms :
1. Clarity - it is a difficult language or not ?
2. Accuracy - it is a correct output/ technically correct for the concept ?
3. Structure - does it follow good formatting or not ?
4. Beginner-Friendly - does the Output can be easily understandable by a Slow Learner/ Beginner
5. Examples - does it providing any real-life examples/ concept-related examples
6. Overall Comments - generate a one line summary about the response on your own 
Rules : Do not generate other responses related to the output concept. give scores only between 0-10. return only in JSON format
Output : Generate the output only in valid JSON Format as shown as below:
{{
    "Clarity": 0,
    "Accuracy": 0,
    "Structure": 0,
    "Beginner_Friendliness": 0,
    "Examples": 0,
    "Overall_Comments": ""
}}
"""
        
        # Generate Evaluation Response
        evaluation_response = client.models.generate_content(model="gemini-3.5-flash", contents= evaluation_prompt)
        evaluation_text = evaluation_response.text

        # Clean JSON Formatting
        evaluation_text = evaluation_text.replace("```json", "")
        evaluation_text = evaluation_text.replace("```", "")
        evaluation_text = evaluation_text.strip()

        # Convert String to JSON
        evaluation_report = json.loads(evaluation_text)

        # Create evaluation filename
        base_name = file_name.replace(".txt", "")
        evaluation_file = base_name.replace(
            "prompt",
            "evaluation"
        ) + ".json"

        evaluation_path = os.path.join(evaluation_folder, evaluation_file)

        # Save Evaluation Report
        with open(evaluation_path, 'w', encoding= 'utf-8') as f:
            json.dump(evaluation_report, f, indent= 4)
        
        #print(evaluation_report)
        print(f"Evaluation Report is Saved Sucessfully in {evaluation_file}")
