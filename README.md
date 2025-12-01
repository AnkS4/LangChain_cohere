# LangChain Essencial programs using cohere

A collection of LangChain implementations using cohere's language models for natural language processing tasks.


## 🛠️ Prerequisites

- Python (3.11 to 3.13 (inclusive))
- [uv](https://github.com/astral-sh/uv) package manager (required for dependency management)
- [Cohere API Key](https://dashboard.cohere.com/api-keys) (required, set in `.env`)
- [LangSmith API Key](https://smith.langchain.com/) (required, set in `.env`)
- `make` (usually pre-installed on Unix-like systems)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnkS4/LangChain_cohere.git
   # git clone git@github.com:AnkS4/LangChain_cohere.git (For SSH)
   cd LangChain_cohere
   ```

2. **Set up environment variables**
   ```bash
   cp example.env .env
   # Edit .env and add your API keys
   ```

3. **Install dependencies**
   ```bash
   make install
   ```

4. **List the available progrmas**
    ```bash
    make list
    ```

5. **Run the application**
    ```bash
    make run SCRIPT=filename.py
    ```

    Ex. For l1.py
    ```bash
    make run SCRIPT=l1.py
    $ (Enter to use default query or ask query like "Which artists have the most albums?")
    ```

## 📂 Project Structure

```
LangChain_cohere/
├── src/                 # Directory for Python scripts
│   ├── l1.py              # Test application with LangChain agent and SQL integration
│   ├── l2.py
│   └── ...                
├── db/                  # Directory for database files
│   └── Chinook.db         # SQLite database (music store data)
├── .env                   # Environment variables (API keys, database config)
├── example.env            # Template for required environment variables
├── requirements.txt       # Python package dependencies
├── pyproject.toml         # Project configuration and metadata (For uv)
├── Makefile               # Common development commands
└── README.md              # Project documentation
```

## 🛠️ Available Commands

- `make help` - Show available commands
- `make list` - List all available Python programs
- `make install` - Install dependencies
- `make run SCRIPT=filename` - Run a specific Python program (default: l1.py)
- `make clean` - Clean up temporary files and virtual environment
