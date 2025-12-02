from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage
from pprint import pprint


DEFAULT_SYSTEM_PROMPT = "You are a helpful geography assistant"
DEFAULT_HUMAN_PROMPT = "What is the capital of Laos?"

def get_prompt(prompt_type):
    """Prompt user with a default value."""
    try:
        default = DEFAULT_SYSTEM_PROMPT if prompt_type == "system" else DEFAULT_HUMAN_PROMPT
        return input(f"{prompt_type.title()} Prompt [{default}]: ").strip() or default
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting...")
        exit(0)

def create_agent():
    """Create a Cohere chat agent and invoke it."""
    model = ChatCohere()
    system_prompt = get_prompt("system")
    human_prompt = get_prompt("human")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    return model.invoke(messages)

def interactive_response_viewer(response):
    """Interactive viewer for exploring response details."""
    if not hasattr(response, 'response_metadata'):
        print("No detailed metadata available for this response.")
        return
    
    while True:
        print("\nResponse Details Menu:\n1. Show raw response\n2. Show response metadata\n3. Show available messages\n0. Exit")
        choice = input("\nEnter your choice (0-3): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            print("\nRaw Response:")
            pprint(vars(response))
        elif choice == '2':
            print("\nResponse Metadata:")
            pprint(response.response_metadata)
        elif choice == '3':
            print(f"\nAvailable Message Types:\n{'-'*50}")
            messages = response.messages if hasattr(response, 'messages') else [response]
            for i, msg in enumerate(messages, 1):
                content_preview = str(msg.content) if hasattr(msg, 'content') and msg.content else '[No content]'
                print(f"{i}. {type(msg).__name__}: {content_preview}")
        else:
            print("\nInvalid choice. Please try again.")

def handle_error(e, context=""):
    """Handle and log errors."""
    print(f"\nError {context}: {e}")
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print(f"Response: {e.response.text}")

def main():
    """Main execution function."""
    load_dotenv()
    print("\nStarting chat with agent...\n")
    try:
        response = create_agent()
        print(f"\nAgent response:\n{'-'*50}\n{response.content}\n{'-'*50}")
        interactive_response_viewer(response)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        handle_error(e, "during agent invocation")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        handle_error(e, "in main execution")
