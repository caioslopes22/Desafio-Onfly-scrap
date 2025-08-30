
import pandas as pd
from .utils import setup_logger

logger = setup_logger("poke_pipeline.transform")

def categorize_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    def cat(exp):
        if pd.isna(exp):
            return "Desconhecido"
        if exp < 50:
            return "Fraco"
        if 50 <= exp <= 100:
            return "Medio"
        return "Forte"

    df = df.copy()
    df["Categoria"] = df["Experiencia Base"].apply(cat)
    return df

def type_counts(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Computing count of Pokémon by type")
    exploded = df.explode("Tipos").dropna(subset=["Tipos"])
    counts = exploded.groupby("Tipos", as_index=False).size().rename(columns={"size": "Quantidade"})
    counts = counts.sort_values("Quantidade", ascending=False).reset_index(drop=True)
    return counts

def mean_stats_by_type(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Computing mean stats (HP, Ataque, Defesa) by type")
    exploded = df.explode("Tipos").dropna(subset=["Tipos"])
    means = (exploded
             .groupby("Tipos", as_index=False)[["HP", "Ataque", "Defesa"]]
             .mean(numeric_only=True)
             .round(2))
    means = means.sort_values("Tipos").reset_index(drop=True)
    return means

def top_by_experience(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    top = df.sort_values("Experiencia Base", ascending=False).head(n)
    return top.reset_index(drop=True)
