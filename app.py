from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv

import json, ast

from tools import (
    load_and_parse_json_string,
    convert_docx_to_quiz,
    add_new_question,
    update_question,
    delete_question
)
from prompt import SYSTEM_PROMPT
import state  # <— import our global state holder

load_dotenv("cred.env")

llm = ChatOpenAI(temperature=0, model="gpt-4o")
agent_executor = initialize_agent(
    [add_new_question, update_question, delete_question],
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": SYSTEM_PROMPT}
)

app = Flask(__name__)
CORS(app)
app.json.sort_keys = False

def reformat_quiz_data(data):
    if isinstance(data, list):
        out = {}
        for item in data:
            if isinstance(item, dict) and "name" in item and "questions" in item:
                out[item["name"]] = {"questions": item["questions"]}
        return out
    return data

@app.route('/')
def index():
    return jsonify({"status": "Running"})

@app.route('/api/process', methods=['POST'])
def process_command():
    prompt = request.form.get('prompt','')
    quiz_data_str = request.form.get('quiz_data')
    selected_info_str = request.form.get('selected_question_info')

    # If the frontend sent quiz_data, overwrite global state
    if quiz_data_str:
        try:
            parsed = json.loads(quiz_data_str)
            state.QUIZ_DATA = reformat_quiz_data(parsed)
        except:
            pass

    # Handle file uploads (load quiz)
    files = request.files.getlist('files')
    if files:
        f = files[0]
        if f.filename.endswith('.json'):
            content = f.read().decode('utf-8')
            parsed = load_and_parse_json_string(content)
        else:
            parsed = convert_docx_to_quiz(f.stream)

        parsed = reformat_quiz_data(parsed)
        if "error" in parsed:
            return jsonify({"status":"error","message":parsed["error"]}),400

        state.QUIZ_DATA = parsed
        return jsonify({
            "status":"success",
            "action":"load_quiz",
            "message":f"Loaded {f.filename}",
            "data": state.QUIZ_DATA
        })

    # Otherwise, editing via the agent
    # Build agent prompt
    agent_input = f"User wants to edit the quiz:\n{prompt}"
    if selected_info_str:
        sel = json.loads(selected_info_str)
        agent_input += f"\nContext: selected question {sel['position']} in '{sel['category']}'"

    # Invoke the agent — tools will touch state.QUIZ_DATA directly
    agent_response = agent_executor.invoke({"input": agent_input})
    func_output = agent_response.get("output")  # 
    # Because our tools return the updated global, we can ignore func_output

    # Return the updated global quiz state
    return jsonify({
        "status":"success",
        "action":"update_quiz",
        "message":"Quiz updated",
        "data": state.QUIZ_DATA
    })

if __name__=='__main__':
    app.run(debug=True, port=5000)
