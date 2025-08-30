
import os
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
from .utils import setup_logger
from .transform import type_counts, mean_stats_by_type, top_by_experience

logger = setup_logger("poke_pipeline.report")

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def plot_type_distribution(counts_df: pd.DataFrame, output_dir: str) -> str:
    ensure_dir(output_dir)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts_df["Tipos"], counts_df["Quantidade"])
    ax.set_xlabel("Tipo de Pokémon")
    ax.set_ylabel("Quantidade")
    ax.set_title("Distribuição de Pokémon por Tipo")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out_path = os.path.join(output_dir, "distribuicao_por_tipo.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved chart: {out_path}")
    return out_path

def generate_and_export_reports(df: pd.DataFrame, output_dir: str) -> Tuple[str, str, str, str]:
    ensure_dir(output_dir)

    counts_df = type_counts(df)
    means_df = mean_stats_by_type(df)
    top5_df = top_by_experience(df, n=5)


    # Save CSVs
    #counts_csv = os.path.join(output_dir, "pokemon_por_tipo.csv")
    means_csv = os.path.join(output_dir, "media_stats_por_tipo.csv")
    top5_csv = os.path.join(output_dir, "top5_experiencia.csv")
    #full_csv = os.path.join(output_dir, "pokemon_dataset.csv")

    #counts_df.to_csv(counts_csv, sep=";", index=False)
    means_df.to_csv(means_csv, sep=";", index=False)
    top5_df.to_csv(top5_csv, sep=";", index=False)
    #df.to_csv(full_csv, sep=";", index=False)

    logger.info(f"Saved CSVs to {output_dir}")

    chart_path = plot_type_distribution(counts_df, output_dir)

    #return counts_csv, means_csv, top5_csv, chart_path
    return  means_csv, top5_csv, chart_path

