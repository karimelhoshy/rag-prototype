#!/usr/bin/env python3
"""
CLI script for document ingestion
"""
import argparse
from src.ingestion import IngestionPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documents from cloud storage into vector database"
    )
    parser.add_argument(
        "--storage",
        type=str,
        choices=["s3", "gcp", "azure"],
        required=True,
        help="Cloud storage provider"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        help="Storage prefix/folder path to filter files"
    )

    args = parser.parse_args()

    print(f"Starting ingestion from {args.storage}...")
    pipeline = IngestionPipeline(storage_type=args.storage)
    pipeline.run(prefix=args.prefix)
    print("Ingestion complete!")


if __name__ == "__main__":
    main()
