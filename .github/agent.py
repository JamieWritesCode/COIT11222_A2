import anthropic
import subprocess
import os
import json
import argparse
import sys
import shlex

# --- 1. DEFINE THE TOOLS CLAUDE CAN USE ---

tool_definitions = [
    {
        "name": "list_files",
        "description": "Lists all files and directories in a given path. Use '.' for the current directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "read_file",
        "description": "Reads the full content of a specified text file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to read."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "run_bash_command",
        "description": "Runs a single, non-interactive bash command in the shell. Use this to install dependencies (e.g., 'pip install -r requirements.txt'), create test files ('echo \"...\" > test.txt'), compile code ('mvn compile'), or run non-interactive scripts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The exact bash command to run."
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "submit_assessment",
        "description": "Call this tool ONLY when you are finished. This submits the final grade and detailed report to the autograding system.",
        "input_schema": {
            "type": "object",
            "properties": {
                "test_name": {
                    "type": "string",
                    "description": "The name for this test, e.g., 'AI Code Assessment'."
                },
                "points_earned": {
                    "type": "integer",
                    "description": "The final score the student earned."
                },
                "points_possible": {
                    "type": "integer",
                    "description": "The maximum possible score for the assignment (e.g., 12)."
                },
                "output_report": {
                    "type": "string",
                    "description": "The full, detailed markdown report justifying the score, as defined in the context.md output format."
                }
            },
            "required": ["test_name", "points_earned", "points_possible", "output_report"]
        }
    }
]

# --- 2. TOOL IMPLEMENTATION ---

def list_files(path):
    """Lists files in a directory, excluding noise."""
    try:
        all_files = os.listdir(path)
        # Filter out common noise
        filtered_files = [f for f in all_files if f not in ['.github', 'venv', '.venv', 'env', '.env', '__pycache__', 'node_modules', 'target']]
        return f"Files in '{path}': {', '.join(filtered_files)}"
    except Exception as e:
        return f"Error listing files: {str(e)}"

def read_file(path):
    """Reads a file's content."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def run_bash_command(command):
    """Runs a shell command and returns its output."""
    print(f"[AGENT RUNS]: {command}")
    try:
        # Use shlex.split to handle quotes and arguments properly
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=60  # 60-second timeout
        )
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nExit Code: {result.returncode}"
        return output
    except Exception as e:
        return f"Error running command: {str(e)}"

def submit_assessment(test_name, points_earned, points_possible, output_report):
    """Formats the JSON for the 'autograding-grading-reporter' action."""
    results_json = [
        {
            "test_name": test_name,
            "output": output_report,
            "status": "pass", # "pass" just means the test ran
            "points_earned": points_earned,
            "points_possible": points_possible
        }
    ]
    # This dictionary tells the main loop to stop
    return {"final_submission": True, "data": results_json}


# --- 3. THE AGENT RUNNER LOOP ---

def main(output_file):
    client = anthropic.Anthropic() # API key read from ANTHROPIC_API_KEY env var
    
    # Load all context
    try:
        with open(".github/prompt.md", "r") as f:
            system_prompt = f.read()
        with open(".github/context.md", "r") as f:
            context = f.read()
        with open(".github/instructions.md", "r") as f:
            instructions = f.read()
    except FileNotFoundError as e:
        print(f"::error::Missing required file: {e.filename}. Make sure .github/prompt.md, context.md, and instructions.md all exist.")
        sys.exit(1)
        
    initial_user_message = f"Here is the context for the assignment I need you to grade:\n{context}\n\nHere are the instructions that were given to the student:\n{instructions}\n\nPlease begin the assessment. Start by exploring the repository."
    
    messages = [{"role": "user", "content": initial_user_message}]
    print("--- Starting AI Agent ---")

    while True:
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307", # Fast and cost-effective
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tool_definitions,
                tool_choice={"type": "auto"}
            )
        except Exception as e:
            print(f"::error::Error calling Anthropic API: {str(e)}")
            sys.exit(1) 

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            tool_use_block = next(block for block in response.content if block.type == "tool_use")
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input
            tool_use_id = tool_use_block.id
            
            print(f"--- Claude wants to use tool: {tool_name} ---")
            
            # Call the correct Python function
            if tool_name == "list_files":
                tool_result = list_files(**tool_input)
            elif tool_name == "read_file":
                tool_result = read_file(**tool_input)
            elif tool_name == "run_bash_command":
                tool_result = run_bash_command(**tool_input)
            elif tool_name == "submit_assessment":
                tool_result = submit_assessment(**tool_input)
            else:
                tool_result = f"Unknown tool: {tool_name}"
            
            # Check if this was the final submission tool
            if isinstance(tool_result, dict) and tool_result.get("final_submission"):
                print("--- Assessment complete. Submitting results. ---")
                final_json = tool_result["data"]
                with open(output_file, 'w') as f:
                    json.dump(final_json, f)
                print(f"Results written to {output_file}")
                break # Exit the loop
            else:
                # Send the tool's output back to Claude
                messages.append({
                    "role": "user",
                    "content": [
                        { "type": "tool_result", "tool_use_id": tool_use_id, "content": str(tool_result) }
                    ]
                })
        else:
            # Handle cases where the agent just thinks or talks
            text_response = next((block.text for block in response.content if block.type == "text"), "")
            if text_response:
                print(f"--- Claude says: {text_response} ---")
            if response.stop_reason == "end_turn":
                continue # Let the agent think again
            else:
                print(f"::warning::Agent stopped unexpectedly: {response.stop_reason}")
                break # Exit loop on error or completion


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI Assessment Agent.")
    parser.add_argument("--output-file", default="results.json", help="File to write final JSON results to.")
    args = parser.parse_args()
    main(args.output_file)