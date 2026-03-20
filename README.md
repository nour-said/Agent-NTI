<<<<<<< HEAD
# Story Teller — Multi-Agent System

A LangGraph-based multi-agent storytelling pipeline.

## Architecture

```
START → [Orchestrator] → [Story Writer] → [Image Prompt] → [Image Generator] → END
```

| Agent | Role |
|-------|------|
| **Orchestrator** | Analyzes user seed, crafts a creative directive |
| **Story Writer** | Writes a ~200-word story from the directive |
| **Image Prompt** | Distills the story into a visual prompt |
| **Image Generator** | Generates an image via Pollinations.ai (free) |

## Setup

```bash
# 1. Clone / enter the repo
cd storyteller

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...   # Windows: set ANTHROPIC_API_KEY=...
```

## Run

### CLI (pure Python)
```bash
python agents.py
```

### Streamlit UI
```bash
streamlit run app.py
```

## Swap Image Backend

In `agents.py`, find `image_generator_node` and replace the Pollinations URL with:
- **Gemini Flash 2.0** (free tier): use `google-generativeai` SDK
- **DALL-E 3**: use `openai` SDK
- **Stable Diffusion**: use `diffusers` or Replicate API
=======
# Agent-NTI
>>>>>>> 32d0f63b31042717407e89f5d360ab8b7785e767
