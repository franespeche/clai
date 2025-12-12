import requests
import json
import os
import sys
import pyperclip
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(
        description ="Convert a natural-language instruction into a Unix command.\n" "Example: 'xai list all files in the current directory' → 'ls -la' (printed to stdout and copied to clipboard).",
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument(
    "text",
    nargs=argparse.REMAINDER,
    help="The command description to convert into a unix command.",
)
parser.add_argument(
    "--list-models",
    action="store_true",
    help="List available models.",
)
parser.add_argument(
    "--model",
    help="Override the model used for this request."
)
parser.add_argument(
    "--status",
    action="store_true",
    help="Get API key status (rate limit / credits left).",
)

args = parser.parse_args()

# get available models
def print_available_models(apikey):
    response = requests.get(
      url="https://openrouter.ai/api/v1/models",
      headers={
          "Authorization": f"Bearer {apikey}"
      })
    models = response.json().get("data", [])
    if not models:
        print("No models returned.")
        return

    for m in models:
        model_id = m.get("id", "")
        name = m.get("name", "")
        ctx = m.get("context_length", None)
        pricing = m.get("pricing", {}) or {}

        prompt_price = pricing.get("prompt")
        completion_price = pricing.get("completion")

        # minimal, readable output
        line = model_id
        if name:
            line += f"  ({name})"
        print(line)

        details = []
        if ctx is not None:
            details.append(f"context: {ctx} tokens")
        if prompt_price is not None:
            details.append(f"in: ${prompt_price}/token")
        if completion_price is not None:
            details.append(f"out: ${completion_price}/token")

        if details:
            print("  " + " | ".join(details))
        print()  # blank line between models
    return response.json()

# get rate limit or credits left info
def get_api_key_info(apikey):
    response = requests.get(
      url="https://openrouter.ai/api/v1/key",
      headers={
        "Authorization": f"Bearer {apikey}"
    })
    return response.json()

# print(json.dumps(response.json(), indent=2))

# make a chat completion request
def get_unix_command(description, apikey, model):

    system_msg = (
        f"you will receive instructions for performing a specific task. "
        f"your job is to respond with a command that can be copy-pasted "
        f"directly into a linux shell. respond only with the command, "
        f"plain text, no markdown."
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {apikey}"},
        data=json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": description},
            ]
        })
    )
    cmd = response.json().get("choices", [])[0].get("message", {}).get("content", "")

    print(cmd)
    pyperclip.copy(cmd)
    

if __name__ == "__main__":
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
    apikey = os.getenv("OPENROUTER_API_KEY", "")

    if args.status:
        info = get_api_key_info(apikey)
        print(json.dumps(info, indent=2))
        sys.exit(0)

    if args.list_models:
        print_available_models(apikey)

        sys.exit(0)

    if args.model:
        model = args.model

    prompt = " ".join(sys.argv[1:])
    if not prompt:
       print("Error: No prompt provided.")
       sys.exit(1)

    get_unix_command(prompt, apikey, model)

