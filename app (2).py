"""
GenAI Writing Assistant
=========================
A small tool with two modes, both built on PROMPT ENGINEERING techniques
(not just "call an API and hope"):

  1. Blog Outline Generator — give it a topic, get a structured outline.
  2. Message Rewriter — paste a rough email/message + a target tone, get a
     polished rewrite.

Both modes use FEW-SHOT PROMPTING: instead of just asking the model to do
the task, we show it 1-2 worked examples first, so it learns the exact
format/style we want before it generates anything. This is a core prompt
engineering technique — it consistently improves output quality and
format-consistency compared to a plain "zero-shot" instruction.

Before running, set your FREE Groq API key (get one at
https://console.groq.com/keys — no credit card needed):
    $env:GROQ_API_KEY="gsk_..."     (Windows PowerShell)
    export GROQ_API_KEY="gsk_..."   (Mac/Linux)

Then run:
    python app.py
"""

import os
from groq import Groq

MODEL = "openai/gpt-oss-120b"  # same model we confirmed working in the RAG project


def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: Set your GROQ_API_KEY environment variable first. See the top of this file.")
        return None
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# MODE 1: Blog Outline Generator
# ---------------------------------------------------------------------------

BLOG_OUTLINE_SYSTEM_PROMPT = """You are an expert content strategist who writes clear, \
practical blog outlines. Follow the exact format shown in the example below. \
Do not add commentary before or after the outline."""

# This is the "few-shot" example: one fully worked input/output pair, given
# to the model as a fake prior conversation turn. The model then mimics this
# exact structure and tone for the real topic.
BLOG_OUTLINE_EXAMPLE_USER = "Topic: How to start meal prepping for beginners"
BLOG_OUTLINE_EXAMPLE_ASSISTANT = """Title: Meal Prep 101: A Beginner's Guide to Eating Well Without the Stress

1. Why Meal Prep Matters
   - Saves time during busy weekdays
   - Reduces impulsive, unhealthy food choices
   - Saves money compared to eating out

2. Getting Started: The Basics
   - Choose 2-3 recipes to start (don't overcomplicate it)
   - Pick a consistent prep day (e.g., Sunday)
   - Invest in a few good storage containers

3. Building a Simple Weekly Plan
   - Pick a protein, a carb, and a vegetable for each meal
   - Batch-cook in bulk (rice cooker, sheet pan, slow cooker)
   - Portion into containers immediately after cooking

4. Common Beginner Mistakes to Avoid
   - Prepping too many different meals at once
   - Not accounting for variety (getting bored by day 3)
   - Ignoring proper storage/food safety guidelines

5. Keeping It Sustainable
   - Rotate between 4-5 go-to recipes
   - Prep in stages if a full day feels overwhelming
   - Adjust portions based on real hunger, not guesswork"""


def generate_blog_outline(client, topic):
    messages = [
        {"role": "system", "content": BLOG_OUTLINE_SYSTEM_PROMPT},
        {"role": "user", "content": BLOG_OUTLINE_EXAMPLE_USER},
        {"role": "assistant", "content": BLOG_OUTLINE_EXAMPLE_ASSISTANT},
        {"role": "user", "content": f"Topic: {topic}"},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,  # a bit of creativity is good for outlines
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# MODE 2: Message / Email Rewriter
# ---------------------------------------------------------------------------

REWRITE_SYSTEM_PROMPT = """You are an expert editor who rewrites messages to match a \
requested tone while preserving the original meaning and key details. \
Follow the exact format shown in the example below: output ONLY the rewritten \
message, nothing else — no preamble, no explanation."""

REWRITE_EXAMPLE_USER = """Tone: formal
Message: hey can you send me that report when u get a chance, kinda need it soon lol"""
REWRITE_EXAMPLE_ASSISTANT = """Hello,

Could you please send over the report at your earliest convenience? I need it relatively soon.

Thank you."""


def rewrite_message(client, tone, message):
    messages = [
        {"role": "system", "content": REWRITE_SYSTEM_PROMPT},
        {"role": "user", "content": REWRITE_EXAMPLE_USER},
        {"role": "assistant", "content": REWRITE_EXAMPLE_ASSISTANT},
        {"role": "user", "content": f"Tone: {tone}\nMessage: {message}"},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    client = get_client()
    if client is None:
        return

    print("GenAI Writing Assistant")
    print("=" * 40)
    print("1. Generate a blog outline")
    print("2. Rewrite a message in a different tone")
    print("q. Quit")

    while True:
        choice = input("\nChoose an option (1/2/q): ").strip().lower()

        if choice == "q":
            break

        elif choice == "1":
            topic = input("Enter a blog topic: ").strip()
            if not topic:
                continue
            print("\nGenerating outline...\n")
            outline = generate_blog_outline(client, topic)
            print(outline)

        elif choice == "2":
            tone = input("Enter target tone (e.g. formal, casual, persuasive, concise): ").strip()
            print("Paste the message to rewrite (press Enter when done):")
            message = input().strip()
            if not tone or not message:
                continue
            print("\nRewriting...\n")
            rewritten = rewrite_message(client, tone, message)
            print(rewritten)

        else:
            print("Please enter 1, 2, or q.")


if __name__ == "__main__":
    main()
