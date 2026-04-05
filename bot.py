import argparse
import sys
from src.database import ErrorDB
from src.llm import FixGenerator

def main():
    parser = argparse.ArgumentParser(description="AI Bug Fix Suggestion Bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest historical error data from a JSON file")
    ingest_parser.add_argument("file", type=str, help="Path to JSON file with error data")

    # Suggest command
    suggest_parser = subparsers.add_parser("suggest", help="Suggest a fix for a given error log")
    suggest_parser.add_argument("error_log", type=str, help="The error message or stack trace to fix")

    args = parser.parse_args()

    # Initialize ChromaDB client lazily
    db = ErrorDB()

    if args.command == "ingest":
        print(f"Ingesting data from {args.file}...")
        try:
            db.ingest_data(args.file)
            print("Ingestion complete. The database has been updated.")
        except Exception as e:
            print(f"Failed to ingest data: {e}", file=sys.stderr)
    elif args.command == "suggest":
        print("Searching for similar historical cases...")
        similar_cases = db.query_similar_errors(args.error_log, n_results=2)
        
        num_found = len(similar_cases.get('documents', [[]])[0])
        print(f"Found {num_found} similar historical cases.")
        
        print("Generating suggested fix...")
        try:
            generator = FixGenerator()
            suggestion = generator.generate_fix(args.error_log, similar_cases)
            print("\n" + "="*50)
            print("🚀 SUGGESTED FIX")
            print("="*50)
            print(suggestion)
            print("="*50)
        except ValueError as ve:
            print(ve, file=sys.stderr)
            print("Please create an .env file with GEMINI_API_KEY or export it.", file=sys.stderr)
        except Exception as e:
            print(f"Failed to generate fix: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
