- Make sure to install the required dependencies.

```bash
# create a virtual environment with your preferred tool
uv venv

# install the required dependencies
uv pip install -r requirements.txt
```

- Create a `.env` file in the root directory and add your OpenRouter key along with the prefered model.

```
# .env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=your_preferred_model_here
```

-

- Create a global `xai` executable wrapper. Make sure to replace REPO_DIR with the actual path to the cloned repository (e.g., `/home/username/.xai`).

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

- Ensure `~/.local/bin` is in your PATH. Add the following line to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```
