# Smart-Writing-Assistant-Blog-Outlines-Tone-Rewriting

A small AI writing tool with two modes, built to demonstrate real prompt
engineering — not just "call an API."

## What it does

1. **Blog Outline Generator** — give it a topic, get back a structured,
   numbered outline with a title and sub-points.
2. **Message Rewriter** — paste a rough email/text and a target tone
   (formal, casual, persuasive, concise, etc.), get a polished rewrite.

## The key technique: Few-Shot Prompting

Instead of just telling the model "write a blog outline," this project shows
the model **one fully worked example first** (a fake prior question + a
model-quality answer), before asking it to do the real task. This is called
**few-shot prompting**, and it's one of the most reliable ways to improve
output quality and format consistency — you're not just describing what you
want, you're *showing* it.

Look inside `app.py` at `BLOG_OUTLINE_EXAMPLE_USER` /
`BLOG_OUTLINE_EXAMPLE_ASSISTANT` — that's the few-shot example baked into
every request as fake conversation history.

## Setup

1. **Install Python 3.10+** if you don't have it.

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1        # Windows PowerShell
   source venv/bin/activate         # Mac/Linux
   ```

3. **Install the one dependency:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get a free Groq API key** (no credit card, no phone verification):
   https://console.groq.com/keys

5. **Set it as an environment variable:**
   ```bash
   $env:GROQ_API_KEY="gsk_..."      # Windows PowerShell
   export GROQ_API_KEY="gsk_..."    # Mac/Linux
   ```

## Run it

```bash
python app.py
```

You'll get a menu:
```
1. Generate a blog outline
2. Rewrite a message in a different tone
q. Quit
```

### Example: Blog outline
```
Enter a blog topic: How remote work changed team communication

Title: Beyond the Office: How Remote Work Rewired Team Communication
1. The Old Model: Communication in a Shared Space
   ...
```

### Example: Message rewriter
```
Enter target tone: persuasive
Paste the message to rewrite: hey can we push the deadline back a bit, still working on it
```

## How it works under the hood

- **System prompt**: sets the model's role and output format rules (e.g.
  "output ONLY the rewritten message, no preamble").
- **Few-shot example**: one fake user/assistant exchange showing exactly the
  format and quality expected, injected before the real request.
- **Temperature**: outline generation uses `0.7` (a bit more creative/varied),
  while rewriting uses `0.5` (more consistent, less prone to drifting from
  the original meaning).

## Ways to extend this (good next steps for your portfolio)

- **Add more modes**: cold outreach emails, resume bullet rewriting, social
  media captions — each is just a new system prompt + few-shot pair.
- **Add a web UI**: wrap this in a simple [Streamlit](https://streamlit.io)
  app so it's not just a terminal tool — huge portfolio upgrade for not much
  extra code.
- **A/B test prompting strategies**: compare zero-shot (no example) vs.
  few-shot (this version) output quality side by side — a great way to
  *demonstrate* why prompt engineering matters, with real before/after output.
- **Add output validation**: check that the blog outline actually has a title
  and at least 3 sections before showing it to the user; retry if not.
- **Swap in different tone presets**: build a fixed menu of tones (formal,
  casual, urgent, apologetic) instead of free-text, and few-shot each one
  differently for even more consistent results.

## Troubleshooting

- **"Set your GROQ_API_KEY" error** — make sure you set it in the *same*
  terminal session you're running `python app.py` from; it doesn't persist
  across new terminal windows.
- **Empty or cut-off output** — try re-running; occasionally free-tier
  responses get truncated under load. You can also increase
  `max_tokens` in the `client.chat.completions.create(...)` calls if you
  want longer, more detailed outlines.
