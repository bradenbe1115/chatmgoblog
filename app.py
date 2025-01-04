import argparse
import requests

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple command-line app that answers questions about Michigan Football using a RAG pipeline and MGoBlog content.")

    # Add argument for the question
    parser.add_argument('question', type=str, help="The question to ask the app")

    # Parse the arguments
    args = parser.parse_args()

    print(f"You asked: {args.question}")
    context = requests.get("http://localhost:5005/user_query", json={"user_query": args.question})
    response = requests.get("http://localhost:5008/gen_chat_with_context", json={"question": args.question, "context": [x["text"] for x in context.json()]})
    print(f"Response: {response.json()["response"]}")

if __name__ == "__main__":
    main()