#!/usr/bin/env python3
"""
CLI script for querying the RAG system
"""
import argparse
from src.rag import RAGQueryEngine


def main():
    parser = argparse.ArgumentParser(
        description="Query the RAG system from command line"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Your question"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of documents to retrieve"
    )

    args = parser.parse_args()

    query_engine = RAGQueryEngine(top_k=args.top_k)
    result = query_engine.query(args.query)

    print("\n" + "="*80)
    print("QUESTION:", result['query'])
    print("="*80)
    print("\nANSWER:")
    print(result['answer'])
    print("\n" + "="*80)
    print("SOURCES:")
    for source in result['sources']:
        print(f"  - {source['filename']}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
