from dotenv import load_dotenv
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_cohere import ChatCohere
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
from langgraph.runtime import get_runtime


# Load environment variables from .env
load_dotenv()
# Initialize database connection
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

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

def get_compact_schema(db: SQLDatabase) -> str:
    """Generate compact schema using SQLAlchemy inspector (no SQL queries)."""
    schema_lines = []

    # Use SQLAlchemy's inspector - no actual SQL queries to DB
    for table_name in db.get_usable_table_names():
        # Get columns directly from SQLAlchemy metadata (cached)
        columns = db._inspector.get_columns(table_name)
        col_names = [col['name'] for col in columns]
        schema_lines.append(f"- {table_name}: {', '.join(col_names)}")

    return '\n'.join(schema_lines)


SYSTEM_PROMPT = f"""SQL analyst for music database (read-only).

Schema:
{get_compact_schema(db)}

Rules:
- Use execute_sql with explicit columns (avoid SELECT *)
- Limit 5 rows unless specified
- Fix and retry on errors"""

agent = create_agent(
    model=ChatCohere(),
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    context_schema=RuntimeContext
)

def get_user_question() -> str:
    """Prompt user for a question with a default value."""
    default_question = "List top 10 artists with highest tracks"
    user_input = input(f"Enter your question (press Enter to use default): "
                     f"\n[Default: {default_question}]\n> ")
    return user_input.strip() or default_question

def handle_error(e: Exception, context: str = "") -> None:
    """Handle and log errors with optional response details."""
    error_msg = [f"\nError {context}: {e}"]
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        error_msg.append(f"Response: {e.response.text}")
    print('\n'.join(error_msg))

if __name__ == "__main__":
    try:
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
    except Exception as e:
        handle_error(e, "in main execution")

