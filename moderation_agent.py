"""
Content Moderation & Classification Agent

Reads user-generated content (reviews, comments, forum posts) and
classifies each item with nuanced judgment — not simple keyword
matching. Distinguishes between clearly safe content, spam, content
that violates guidelines, and genuinely ambiguous content that a
human moderator should review.

This demonstrates a different agentic skill than the other two repos
in this portfolio: no tool calls or multi-step research here — the
value is entirely in structured judgment calls on a single piece of
input, including knowing when NOT to be confident.

Install:
    pip install anthropic

Run:
    export ANTHROPIC_API_KEY=your_key_here
    python agent.py
"""

import anthropic
import json

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a content moderation agent for a community platform.

Classify each piece of content into exactly one category:
- "safe": Fine to publish as-is
- "spam": Promotional, irrelevant, or repetitive junk content
- "violation": Clearly breaks guidelines (harassment, hate speech, threats)
- "needs_review": Ambiguous, sarcastic, borderline, or context-dependent —
  a human moderator should make the final call

Be conservative about "violation" — reserve it for clear-cut cases.
Sarcasm, strong criticism, and heated-but-civil disagreement are NOT
automatically violations; use "needs_review" when tone or intent is
genuinely unclear rather than guessing.

Respond ONLY with valid JSON in this exact shape, no other text:
{
  "category": "safe|spam|violation|needs_review",
  "confidence": "high|medium|low",
  "reasoning": "one sentence explaining the call"
}"""


def classify_content(text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Content to classify:\n\n{text}"}],
    )

    raw = response.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


if __name__ == "__main__":
    sample_content = [
        "This product completely changed how I manage my week. Highly recommend!",
        "CLICK HERE for FREE gift cards!!! www.totally-legit-prizes.com",
        "Oh sure, because THAT feature works so well. Real quality product, 10/10.",
        "Your support team is a joke and everyone who works there should be fired.",
        "Not what I expected but the customer service team resolved it quickly.",
    ]

    for text in sample_content:
        result = classify_content(text)
        print(f"Content: {text}")
        print(f"  -> {result['category']} (confidence: {result['confidence']})")
        print(f"     {result['reasoning']}\n")
