"""Self-improvement logic — rewrites screening prompt based on failures."""

import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

META_PROMPT = """You are a meta-learning system that improves an agent screening prompt.

The current screening prompt is used to classify on-chain agents as "trustworthy" or "untrustworthy".
Your job is to rewrite the screening prompt to fix misclassifications while maintaining or improving performance on correctly classified cases.

Current screening prompt:
<current_prompt>
{current_prompt}
</current_prompt>

The following agents were MISCLASSIFIED by the current prompt:
<failures>
{failures}
</failures>

Current iteration: {iteration}
Current accuracy: {accuracy:.1%}

Instructions:
1. Analyze WHY each failure was misclassified
2. Identify patterns in the failures (common signals that were missed or overweighted)
3. Rewrite the screening prompt to address these specific failures
4. Keep the prompt concise and focused — avoid adding too many edge-case rules
5. Maintain the same output format requirement (JSON with "verdict" field)
6. Do NOT make the prompt overly complex — simple clear rules work best

Return ONLY the new screening prompt text, nothing else. Do not wrap it in quotes or markdown."""


def rewrite(current_prompt: str, failures: list, iteration: int,
            accuracy: float = 0.0, client: anthropic.Anthropic = None) -> str:
    """Rewrite the screening prompt to fix failures.

    Args:
        current_prompt: The current screening prompt text
        failures: List of failure dicts with agent profiles
        iteration: Current iteration number
        accuracy: Current accuracy score
        client: Anthropic client instance

    Returns:
        New screening prompt string
    """
    if client is None:
        client = anthropic.Anthropic()

    if not failures:
        return current_prompt

    failures_str = json.dumps(failures, indent=2)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": META_PROMPT.format(
                    current_prompt=current_prompt,
                    failures=failures_str,
                    iteration=iteration,
                    accuracy=accuracy,
                ),
            }
        ],
    )

    new_prompt = response.content[0].text.strip()

    # Sanity check: must contain verdict instruction
    if "verdict" not in new_prompt.lower():
        new_prompt += '\n\nFor each agent, respond with ONLY a JSON object: {"verdict": "trustworthy"} or {"verdict": "untrustworthy"}'

    return new_prompt
