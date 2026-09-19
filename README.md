# Content Moderation & Classification Agent

An AI agent that classifies user-generated content (reviews, comments, posts) with nuanced judgment, built with the [Claude API](https://docs.claude.com).

## The problem

Keyword-based moderation filters are blunt instruments — they catch obvious spam but miss sarcasm, misclassify heated-but-civil criticism as abuse, and can't tell context-dependent content apart from clear violations. Human moderation teams get flooded with volume, most of which is unambiguous and doesn't need a person's attention at all. The real value is in a system that handles the clear-cut cases confidently and *knows when it's not sure*.

## What this agent does

Given a piece of content, it classifies it into one of four categories:

- **`safe`** — fine to publish as-is
- **`spam`** — promotional, irrelevant, or repetitive junk
- **`violation`** — clearly breaks guidelines (harassment, hate speech, threats)
- **`needs_review`** — ambiguous, sarcastic, or context-dependent — routed to a human rather than guessed at

Each classification comes with a confidence level and a one-sentence reason, so a moderation team can prioritize what to check first.

The important design choice: the agent is deliberately conservative about the `violation` label, and uses `needs_review` for anything genuinely ambiguous rather than forcing a guess. A moderation system that's overconfident about edge cases causes more harm (wrongly silencing people) than one that routes unclear cases to a human.

## Example output

```
Content: CLICK HERE for FREE gift cards!!! www.totally-legit-prizes.com
  -> spam (confidence: high)
     Promotional link with urgency language typical of spam/scam content.

Content: Oh sure, because THAT feature works so well. Real quality product, 10/10.
  -> needs_review (confidence: medium)
     Sarcastic criticism of the product — not a guideline violation, but tone
     is ambiguous enough to flag rather than auto-publish or auto-reject.

Content: Your support team is a joke and everyone who works there should be fired.
  -> needs_review (confidence: medium)
     Harsh criticism of a company/team rather than an individual; borderline
     enough to warrant human judgment rather than an automatic violation call.
```

## How it works

- Single-call classification using the Claude API's Messages endpoint — no multi-step tool use needed, since the task is a judgment call on one input rather than a multi-step workflow
- Structured JSON output makes it easy to pipe into a real moderation queue or dashboard
- System prompt explicitly defines what counts as ambiguous, steering the model away from overconfident calls on edge cases

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python agent.py
```

## Tech

- Python
- [Anthropic Claude API](https://docs.claude.com) (Claude Sonnet)
- Structured JSON output / classification
