# XAI
Transform human instructions into UNIX commands.

`xai` is a command-line tool that converts natural language instructions into executable UNIX commands.
Example: `xai list all files in the current directory` → `ls -la` (printed to stdout and copied to clipboard)

## Usage

```bash
xai "your natural language instruction here"

xai --help # for more information on available options
```

## Prerequisites

- Python 3.8 or higher
- An OpenRouter API key. You can obtain one by signing up at [OpenRouter](https://openrouter.ai/).

## Installation

1 Make sure to install the required dependencies.

```bash
# create a virtual environment with your preferred tool
uv venv

# install the required dependencies
uv pip install -r requirements.txt
```

2 Create a `.env` file in the root directory and add your OpenRouter key along with the prefered model.

```
# .env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=your_preferred_model_here
```

3 Create a global `xai` executable wrapper. Make sure to replace REPO_DIR with the actual path to the cloned repository (e.g., `/home/username/.xai`).

```bash
mkdir -p ~/.local/bin

# create the wrapper

cat > ~/.local/bin/xai << 'EOF'
#!/bin/bash
REPO_DIR="$HOME/.xai"
exec "$REPO_DIR/.venv/bin/python" "$REPO_DIR/xai.py" "$@"
EOF

# make it executable
chmod +x ~/.local/bin/xai
```

4 Ensure `~/.local/bin` is in your PATH. Add the following line to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```
