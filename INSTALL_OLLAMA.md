# Install Ollama for Free Local LLM

The Hugging Face API requires authentication. For free, local LLM access, install Ollama:

## Quick Install (macOS)

### Option 1: Using Homebrew (Recommended)

```bash
brew install ollama
```

### Option 2: Download from Website

1. Visit: https://ollama.ai/
2. Click "Download" for macOS
3. Install the application

## After Installation

1. **Start Ollama:**
   - If installed via Homebrew, Ollama should start automatically
   - If downloaded from website, open the Ollama app

2. **Download a Model:**
   ```bash
   ollama pull llama3.2
   ```
   
   Or for a smaller, faster model:
   ```bash
   ollama pull phi3
   ```

3. **Verify Installation:**
   ```bash
   ollama list
   ```
   
   You should see your downloaded model(s)

4. **Restart the Server:**
   ```bash
   # Stop the current server (if running)
   lsof -ti:8000 | xargs kill
   
   # Start again
   ./start_free.sh
   ```

## Available Models

Popular free models you can use:
- `llama3.2` - Good balance (2B or 3B parameters)
- `phi3` - Fast and efficient (3.8B parameters)
- `mistral` - High quality (7B parameters, requires more RAM)
- `gemma2` - Google's model (2B or 9B parameters)

## Troubleshooting

- **"ollama: command not found"**: Make sure Ollama is installed and in your PATH
- **Connection refused**: Make sure Ollama is running (`ollama serve`)
- **Model not found**: Run `ollama pull <model-name>`

Once Ollama is installed and running, the chatbot will automatically use it instead of Hugging Face API!

