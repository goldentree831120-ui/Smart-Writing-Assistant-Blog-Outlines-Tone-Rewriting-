import json
import re
import time
from app import get_client, generate_blog_outline, rewrite_message, MODEL

REWRITE_TEST_SET = [
    {
        "tone": "formal",
        "message": "hey can you send me that report when u get a chance, kinda need it soon lol",
    },
    {
        "tone": "casual",
        "message": "I am writing to inform you that the project deadline has been extended by two weeks due to unforeseen circumstances.",
    },
    {
        "tone": "persuasive",
        "message": "We should probably switch to the new vendor, their prices seem lower.",
    },
    {
        "tone": "concise",
        "message": "I wanted to reach out and let you know that, after much thought and consideration over the past few days, I've decided that I think it would probably be a good idea for us to reschedule our meeting to sometime next week instead, if that works for you.",
    },
    {
        "tone": "apologetic",
        "message": "The order is late. Not our fault, shipping company messed up.",
    },
]

BLOG_TOPIC_TEST_SET = [
    "How to start a vegetable garden",
    "The benefits of remote work",
    "Beginner's guide to budgeting",
    "Why sleep quality matters",
    "How to learn a new language faster",
]


# ---------------------------------------------------------------------------
# LLM-as-judge helpers
# ---------------------------------------------------------------------------

JUDGE_SYSTEM_PROMPT = """You are a strict evaluator. You will be given an original \
message, a target tone, and a rewritten version. Score the rewrite on two \
criteria, each from 1 (poor) to 5 (excellent):

- tone_match: does the rewrite genuinely match the requested tone?
- meaning_preserved: does the rewrite keep the same facts/intent as the original, \
without adding or dropping information?

Respond with ONLY valid JSON in this exact format, nothing else:
{"tone_match": <1-5>, "meaning_preserved": <1-5>, "reasoning": "<one short sentence>"}"""


def judge_rewrite(client, original, tone, rewritten):
    """Ask the model to score its own rewrite. Returns a dict or None on failure."""
    judge_prompt = (
        f"Target tone: {tone}\n"
        f"Original message: {original}\n"
        f"Rewritten message: {rewritten}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": judge_prompt},
        ],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    # Models sometimes wrap JSON in ```json ... ``` — strip that if present.
    raw = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"    (warning: could not parse judge response: {raw[:100]})")
        return None


def check_outline_structure(outline_text):
    """
    Cheap, non-LLM structural checks for a blog outline — no API call needed.
    Returns a dict of pass/fail booleans.
    """
    has_title = bool(re.search(r"title\s*:", outline_text, re.IGNORECASE))
    numbered_sections = re.findall(r"^\s*\d+\.\s", outline_text, re.MULTILINE)
    has_enough_sections = len(numbered_sections) >= 3
    has_subpoints = outline_text.count("-") >= 6  # rough check for sub-bullets

    return {
        "has_title": has_title,
        "has_enough_sections": has_enough_sections,
        "section_count": len(numbered_sections),
        "has_subpoints": has_subpoints,
    }


# ---------------------------------------------------------------------------
# Main evaluation run
# ---------------------------------------------------------------------------

def run_evaluation():
    client = get_client()
    if client is None:
        return

    print("=" * 55)
    print("PART 1: Message Rewriter — tone accuracy & meaning preservation")
    print("=" * 55)

    rewrite_results = []
    for i, test in enumerate(REWRITE_TEST_SET, start=1):
        start = time.time()
        rewritten = rewrite_message(client, test["tone"], test["message"])
        gen_time = time.time() - start

        judged = judge_rewrite(client, test["message"], test["tone"], rewritten)

        if judged:
            rewrite_results.append(judged)
            print(f"\n[{i}/{len(REWRITE_TEST_SET)}] tone='{test['tone']}' ({gen_time:.1f}s)")
            print(f"    tone_match: {judged['tone_match']}/5 | meaning_preserved: {judged['meaning_preserved']}/5")
            print(f"    reasoning: {judged['reasoning']}")
        else:
            print(f"\n[{i}/{len(REWRITE_TEST_SET)}] tone='{test['tone']}' — judge scoring failed, skipped")

    print("\n" + "=" * 55)
    print("PART 2: Blog Outline Generator — structural compliance")
    print("=" * 55)

    outline_results = []
    for i, topic in enumerate(BLOG_TOPIC_TEST_SET, start=1):
        start = time.time()
        outline = generate_blog_outline(client, topic)
        gen_time = time.time() - start

        structure = check_outline_structure(outline)
        outline_results.append(structure)

        status = "PASS" if (structure["has_title"] and structure["has_enough_sections"]) else "FAIL"
        print(f"\n[{i}/{len(BLOG_TOPIC_TEST_SET)}] {status} ({gen_time:.1f}s) — {topic}")
        print(f"    has_title: {structure['has_title']} | sections: {structure['section_count']} | has_subpoints: {structure['has_subpoints']}")

    # ---- Aggregate metrics ----
    print("\n" + "=" * 55)
    print("RESULTS")
    print("=" * 55)

    if rewrite_results:
        avg_tone = sum(r["tone_match"] for r in rewrite_results) / len(rewrite_results)
        avg_meaning = sum(r["meaning_preserved"] for r in rewrite_results) / len(rewrite_results)
        print(f"Message Rewriter — avg tone match     : {avg_tone:.1f}/5")
        print(f"Message Rewriter — avg meaning preserved: {avg_meaning:.1f}/5")
    else:
        avg_tone = avg_meaning = 0
        print("Message Rewriter — no valid judge scores collected")

    structure_pass_rate = sum(
        1 for r in outline_results if r["has_title"] and r["has_enough_sections"]
    ) / len(outline_results) * 100
    print(f"Blog Outline — structural compliance   : {structure_pass_rate:.0f}%  ({len(outline_results)} topics tested)")

    print("=" * 55)
    print("\nThese are the numbers: ")
    print(f'  "Built a GenAI writing assistant with few-shot prompting;')
    print(f'   evaluated via LLM-as-judge scoring {avg_tone:.1f}/5 on tone accuracy')
    print(f'   and {avg_meaning:.1f}/5 on meaning preservation, with {structure_pass_rate:.0f}%')
    print(f'   structural compliance on generated outlines."')


if __name__ == "__main__":
    run_evaluation()
