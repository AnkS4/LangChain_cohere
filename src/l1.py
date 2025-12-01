from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_cohere import ChatCohere
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
from langgraph.runtime import get_runtime


DEFAULT_QUESTION = "List top 10 artists with highest tracks"
DB_RELATIVE_PATH = Path("db") / "Chinook.db"

def create_database() -> SQLDatabase:
    """Initialize database connection."""
    db_path = Path(__file__).parent.parent / DB_RELATIVE_PATH  # Use the constant
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Define context structure to support dependency injection
@dataclass
class RuntimeContext:
    db: SQLDatabase

@tool
def execute_sql(query: str) -> str:
    """Execute SQL query and return results"""
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db

    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"


def create_sql_agent(db: SQLDatabase):
    """Create and configure the SQL agent."""
    system_prompt = f"""SQL analyst for music database (read-only).
Schema:
{get_compact_schema(db)}
Rules:
- Use execute_sql with explicit columns (avoid SELECT *)
- Limit 5 rows unless specified
- Fix and retry on errors"""
    
    return create_agent(
        model=ChatCohere(),
        tools=[execute_sql],
        system_prompt=system_prompt,
        context_schema=RuntimeContext
    )

def get_compact_schema(db: SQLDatabase) -> str:
    """Generate compact schema using SQLAlchemy inspector."""
    return '\n'.join(
        f"- {table}: {', '.join(col['name'] for col in db._inspector.get_columns(table))}"
        for table in db.get_usable_table_names()
    )

def get_user_question() -> str:
    """Prompt user for a question with a default value."""
    try:
        return input(f"Question [{DEFAULT_QUESTION}]: ").strip() or DEFAULT_QUESTION
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting...")
        exit(0)

def handle_error(e: Exception, context: str = "") -> None:
    """Handle and log errors."""
    print(f"\nError {context}: {e}")
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print(f"Response: {e.response.text}")

def main():
    """Main execution function."""
    load_dotenv()
    db = create_database()
    agent = create_sql_agent(db)
    
    question = get_user_question()
    print(f"\nProcessing: {question}\n")
    
    for step in agent.stream(
        {"messages": question},
        context={"db": db},
        stream_mode="values"
    ):
        try:
            step["messages"][-1].pretty_print()
        except Exception as e:
            handle_error(e, "processing stream")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        handle_error(e, "in main execution")
