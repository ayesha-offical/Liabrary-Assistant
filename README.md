# 📚 Library Assistant

AI-powered **Library Assistant** that helps users with library-related
queries:\
- ✅ Search books\
- ✅ Member verification\
- ✅ Check book availability\
- ✅ Get library timings\
- ❌ Ignore non-library queries

------------------------------------------------------------------------

## 🚀 Features

-   Uses **OpenAI Agents SDK** for AI logic.\
-   Implements **Guardrails** to block irrelevant queries.\
-   Provides simple **CLI-based interface**.\
-   Book database stored locally in Python dictionary.

------------------------------------------------------------------------

## 📂 Project Structure

    assignment_6/
    │── app/
    │   ├── agent.py          # Library Agent setup
    │   ├── guardrails.py     # Guardrails for input/output
    │   ├── instructions.py   # Agent instructions
    │   ├── tools.py          # Tools for search, availability, timings
    │   ├── utils.py          # User context model
    │   ├── data.py           # Dummy book database
    │   └── main.py           # Entry point (Runner)
    │
    │── .env                  # API keys (not pushed to repo)
    │── requirements.txt      # Dependencies
    │── README.md             # Documentation

------------------------------------------------------------------------

## 🔑 Requirements

-   Python 3.10+\
-   OpenAI Agents SDK\
-   Dependencies listed in `requirements.txt`

------------------------------------------------------------------------

## ⚙️ Installation

1.  Clone the repository:

    ``` bash
    git clone https://github.com/your-username/Library-Assistant.git
    cd Library-Assistant
    ```

2.  Create a virtual environment:

    ``` bash
    uv venv
    uv pip install -r requirements.txt
    ```

3.  Add your **OpenAI API Key** in `.env` file:

        OPENAI_API_KEY=your_api_key_here

------------------------------------------------------------------------

## ▶️ Run Project

``` bash
uv run python -m app.main
```

------------------------------------------------------------------------

## 💻 Usage Example

    Welcome to Library Assistant 👋
    • Start: type your name
    • Then: system will verify if you’re a member
    • Commands:
       - search "book name"
       - availability "book name"
       - timings
       - exit

Example flow:

    🧑 You: search Python Basics
    🤖 Assistant: ✅ Yes, we have "Python Basics" available.

    🧑 You: availability Python Basics
    🤖 Assistant: 📦 3 copies available.

------------------------------------------------------------------------


