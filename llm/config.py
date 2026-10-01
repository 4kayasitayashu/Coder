import os
from dotenv import load_dotenv
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY")

# Optional per-agent overrides. If <AGENT>_PROVIDER / <AGENT>_MODEL are not set,
# the agent falls back to LLM_PROVIDER / LLM_MODEL above.
# Example in .env:
#   REVIEWER_PROVIDER=gemini
#   REVIEWER_MODEL=gemini-2.0-flash
AGENT_NAMES = ["PLANNER", "ARCHITECT", "CODER", "REVIEWER", "FIXER", "TESTER"]

AGENT_PROVIDER_OVERRIDES = {
    name: os.getenv(f"{name}_PROVIDER") for name in AGENT_NAMES
}
AGENT_MODEL_OVERRIDES = {
    name: os.getenv(f"{name}_MODEL") for name in AGENT_NAMES
}


def resolve_agent_config(agent_name: str):
    """Returns (provider, model) for a given agent, applying per-agent overrides."""
    key = agent_name.upper()
    provider = AGENT_PROVIDER_OVERRIDES.get(key) or LLM_PROVIDER
    model = AGENT_MODEL_OVERRIDES.get(key) or LLM_MODEL
    return provider, model