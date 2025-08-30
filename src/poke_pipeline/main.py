
import argparse
import os
from .utils import setup_logger
from .extract import build_dataset
from .transform import categorize_by_experience
from .report import generate_and_export_reports

def run(limit: int, offset: int, output_dir: str, request_delay: float):
    logger = setup_logger("poke_pipeline")
    logger.info("Starting PokeAPI pipeline")
    os.makedirs(output_dir, exist_ok=True)

    # Extraction
    df = build_dataset(limit=limit, offset=offset, request_delay=request_delay)
    logger.info(f"Extracted {len(df)} records")

    # Transformation
    df = categorize_by_experience(df)

    # Reporting / Export
    #counts_csv, means_csv, top5_csv, chart_path = generate_and_export_reports(df, output_dir=output_dir)
    means_csv, top5_csv, chart_path = generate_and_export_reports(df, output_dir=output_dir)

    logger.info("Pipeline finished successfully")
    #logger.info(f"Outputs:\n- {counts_csv}\n- {means_csv}\n- {top5_csv}\n- {chart_path}")
    logger.info(f"Outputs:\n- {means_csv}\n- {top5_csv}\n- {chart_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PokeAPI ETL Pipeline")
    parser.add_argument("--limit", type=int, default=100, help="Number of Pokémon to fetch")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--output-dir", type=str, default="/app/outputs", help="Directory to save outputs")
    parser.add_argument("--request-delay", type=float, default=0.05, help="Delay (seconds) between API requests")
    args = parser.parse_args()
    run(limit=args.limit, offset=args.offset, output_dir=args.output_dir, request_delay=args.request_delay)
