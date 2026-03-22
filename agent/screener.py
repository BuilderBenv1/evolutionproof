"""Agent screening task logic — classifies agents as trustworthy or not."""

import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SCREENING_PROMPT = """Classify this on-chain agent as trustworthy or untrustworthy.

Simple rules:
- If erc8004_score > 50 and contract_verified is true: trustworthy
- If failed_tx_ratio > 0.15: untrustworthy
- If age_days < 30 and flagged_interactions > 2: untrustworthy
- If category is mev, attack, spam, or privacy: untrustworthy
- If contract_verified is false: untrustworthy
- Otherwise: trustworthy

Respond with ONLY: {"verdict": "trustworthy"} or {"verdict": "untrustworthy"}
"""


def screen_agents(profiles: list, prompt: str = None, client: anthropic.Anthropic = None) -> dict:
    """Screen a list of agent profiles and return predictions.

    Args:
        profiles: List of agent profile dicts from test_set.json
        prompt: The screening prompt to use (enables self-improvement)
        client: Anthropic client instance

    Returns:
        Dict mapping agent_id -> "trustworthy"|"untrustworthy"
    """
    if prompt is None:
        prompt = DEFAULT_SCREENING_PROMPT
    if client is None:
        client = anthropic.Anthropic()

    predictions = {}

    for profile in profiles:
        agent_id = profile["agent_id"]
        profile_str = json.dumps(profile, indent=2)

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nAgent profile to classify:\n{profile_str}",
                    }
                ],
            )

            result_text = response.content[0].text.strip()
            # Parse the JSON verdict
            try:
                result = json.loads(result_text)
                verdict = result.get("verdict", "untrustworthy")
            except json.JSONDecodeError:
                # Fallback: look for keywords
                lower = result_text.lower()
                if "trustworthy" in lower and "untrustworthy" not in lower:
                    verdict = "trustworthy"
                else:
                    verdict = "untrustworthy"

            predictions[agent_id] = verdict

        except Exception as e:
            print(f"Error screening {agent_id}: {e}")
            predictions[agent_id] = "untrustworthy"  # Conservative default

    return predictions
