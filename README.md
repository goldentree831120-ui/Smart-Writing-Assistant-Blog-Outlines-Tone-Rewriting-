# Smart Writing Assistant (Blog Outlines + Tone Rewriting) -> GenAI Writing Assistant Project

A simple AI writing assistant that can help with two common writing tasks. The main goal of this project is to show how **prompt engineering** can actually improve an AI application's output, rather than simply calling an API and displaying whatever it returns.

## What it does

The project currently has two modes:

1. **Blog Outline Generator** — Enter a topic and the assistant creates a structured blog outline with a title, sections, and sub-points.
2. **Message Rewriter** — Paste a rough email or message, choose the tone you want (formal, casual, persuasive, concise, etc.), and the assistant rewrites it while keeping the original meaning.

## The main idea: Few-Shot Prompting

The interesting part of this project is **few-shot prompting**.

Instead of simply telling the model something like *"Write a blog outline about this topic,"* we first give it an example of what a good response should look like. The model sees a fake user question followed by a well-written answer, and then receives the actual request.

This gives the model a concrete example to follow, which usually helps make the output more consistent in terms of **format, structure, and quality**.

You can see this in `app.py` through:

* `BLOG_OUTLINE_EXAMPLE_USER`
* `BLOG_OUTLINE_EXAMPLE_ASSISTANT`

These are included as part of the conversation before the user's actual request.

## Setup

### 1. Install Python

You'll need **Python 3.10 or newer**.

### 2. Create a virtual environment

**Windows PowerShell:**

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

There is only one main dependency for the project.

### 4. Get a Groq API key

Create a free API key from the Groq console:

https://console.groq.com/keys

### 5. Add your API key

**Windows PowerShell:**

```bash
$env:GROQ_API_KEY="gsk_..."
```

**Mac/Linux:**

```bash
export GROQ_API_KEY="gsk_..."
```

Make sure you set the variable in the same terminal where you'll run the application.

## Running the project

Once everything is set up:

```bash
python app.py
```

You'll see a simple menu:

```text
1. Generate a blog outline
2. Rewrite a message in a different tone
q. Quit
```

### Example: Blog Outline

```text
Enter a blog topic: How remote work changed team communication
```

The model might return something like:

```text
Title: Beyond the Office: How Remote Work Rewired Team Communication

1. The Old Model: Communication in a Shared Space
   ...

2. The Shift to Remote Work
   ...

3. How Teams Adapted
   ...
```

### Example: Message Rewriter

```text
Enter target tone: persuasive

Paste the message to rewrite:
hey can we push the deadline back a bit, still working on it
```

The assistant then rewrites the message in a more persuasive tone without changing the main idea.

## How it works

There are a few important pieces behind the application:

* **System prompt** — tells the model what role it should play and gives it rules for the response. For example, the message rewriter is instructed to return only the rewritten message without adding unnecessary explanations.

* **Few-shot example** — provides the model with a sample user request and a high-quality response. This helps the model understand the expected format instead of relying only on written instructions.

* **Temperature** — controls how much variation the model introduces. The blog outline uses `0.7` because we want slightly more creativity, while the message rewriter uses `0.5` to keep the rewrite closer to the original message.

## Ideas for improving the project

There are several easy ways to take this project further and make it more useful as a portfolio project.

### 1. Add more writing modes

For example:

* Cold outreach emails
* Resume bullet-point rewriting
* LinkedIn posts
* Social media captions
* Cover letters
* Professional emails

Each mode can have its own system prompt and few-shot examples.

### 2. Build a web interface

Instead of running everything from the terminal, you could build a simple interface using **Streamlit**.

That would make the project much easier to demonstrate to someone reviewing your portfolio.

### 3. Compare zero-shot vs. few-shot prompting

This would be one of the most interesting extensions.

You could send the same request using:

**Zero-shot:**

> Write a blog outline about remote work.

and then compare it with:

**Few-shot:**

> Here's an example of the kind of outline I want...
> Now create one for remote work.

Displaying both outputs side by side would give you a concrete way to show that prompt design can affect the model's output.

### 4. Add output validation

You could automatically check whether the generated outline contains:

* A title
* At least 3 sections
* Sub-points
* The expected numbering format

If the response doesn't meet these requirements, the application could automatically ask the model to regenerate it.

### 5. Create predefined tone options

Instead of asking users to type any tone they want, you could provide options such as:

* Formal
* Casual
* Professional
* Persuasive
* Friendly
* Urgent
* Apologetic
* Concise

You could also create different few-shot examples for each tone to make the results more consistent.

## Troubleshooting

### "Set your GROQ_API_KEY" error

This usually means the environment variable isn't available in your current terminal session.

Set the API key again and make sure you're running `python app.py` from that same terminal.

### Output is empty or gets cut off

Free-tier models can occasionally return incomplete responses, especially when the service is under heavy load.

Try running the request again. If you need longer responses, you can also increase the `max_tokens` value in the `client.chat.completions.create(...)` calls.

## What this project demonstrates

Although this is a beginner project, it covers some useful GenAI concepts:

* Calling an LLM API
* Writing system prompts
* Few-shot prompting
* Controlling model temperature
* Structuring LLM outputs
* Validating generated responses
* Comparing different prompting strategies

The main takeaway is that **building an AI application isn't only about connecting an API to a UI. The way you structure the instructions and examples you give the model can have a big impact on the final result.**
