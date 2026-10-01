import json

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from .config import (
    LLM_PROVIDER,
    LLM_MODEL,
    GROQ_API_KEY,
    GEMINI_API_KEY,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    resolve_agent_config,
)


def get_llm(provider=None, model=None, agent_name=None):
    """
    Build an LLM client.

    If `agent_name` is given (e.g. "reviewer"), per-agent overrides from
    .env (REVIEWER_PROVIDER / REVIEWER_MODEL, etc.) are applied first,
    letting different pipeline stages use different providers/models.
    Explicit `provider`/`model` args still win over everything.
    """
    if agent_name:
        agent_provider, agent_model = resolve_agent_config(agent_name)
        provider = provider or agent_provider
        model = model or agent_model

    provider = provider or LLM_PROVIDER
    model = model or LLM_MODEL

    if not model:
        raise ValueError("LLM_MODEL is not configured.")

    if provider == "groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        kwargs = dict(model=model, api_key=GROQ_API_KEY, temperature=0)
        if "gpt-oss" in model:
            kwargs["max_tokens"] = 3000
            kwargs["reasoning_effort"] = "low"
        return ChatGroq(**kwargs)

    elif provider in ("google", "gemini"):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        kwargs = dict(model=model, api_key=GEMINI_API_KEY)
        # Gemini 2.5 models think by default, which can cause the model to
        # echo the JSON *schema* instead of filling it in for structured
        # output calls. Disabling thinking makes structured output reliable.
        if "2.5" in model:
            kwargs["thinking_budget"] = 0
        return ChatGoogleGenerativeAI(**kwargs)

    elif provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")
        return ChatOpenAI(
            model=model,
            api_key=OPENAI_API_KEY
        )

    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not configured.")
        return ChatAnthropic(
            model=model,
            api_key=ANTHROPIC_API_KEY
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")


def invoke_structured(schema, prompt, agent_name=None, provider=None, model=None):
    if agent_name:
        agent_provider, agent_model = resolve_agent_config(agent_name)
        provider = provider or agent_provider
        model = model or agent_model

    llm = get_llm(provider=provider, model=model)
    resolved_provider = provider or LLM_PROVIDER
    resolved_model = model or LLM_MODEL

    attempts = []
    if resolved_provider == "groq":
        attempts.append(("groq json_schema", lambda: llm.with_structured_output(schema, method="json_schema").invoke(prompt)))
    attempts.append(("function_calling", lambda: llm.with_structured_output(schema).invoke(prompt)))

    last_err = None
    for label, attempt in attempts:
        try:
            result = attempt()
            if result is not None:
                return result
            last_err = ValueError(f"{label} returned None")
        except Exception as e:
            last_err = e
            print(f"[{agent_name or resolved_model}] structured output via {label} failed: {e}")

    print(f"[{agent_name or resolved_model}] all structured-output methods failed ({last_err}); falling back to raw JSON parsing.")
    schema_json = schema.model_json_schema()
    raw_prompt = (
        f"{prompt}\n\n"
        "IMPORTANT: Respond with ONLY a single valid JSON object matching this JSON Schema. "
        "Do not include markdown code fences, explanations, or any text before or after the JSON.\n"
        f"JSON Schema:\n{json.dumps(schema_json)}"
    )
    resp = llm.invoke(raw_prompt)
    text = getattr(resp, "content", str(resp)).strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    if not text.startswith("{"):
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]
    data = json.loads(text)
    return schema.model_validate(data)
