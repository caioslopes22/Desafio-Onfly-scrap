
from typing import List, Dict, Any, Optional
import time
import os
import pandas as pd
import requests
from .utils import setup_logger, make_session

POKEAPI_BASE = os.environ.get("POKEAPI_BASE", "https://pokeapi.co/api/v2")

logger = setup_logger("poke_pipeline.extract")

def get_pokemon_list(limit: int = 100, offset: int = 0, session: Optional[requests.Session] = None) -> List[Dict[str, Any]]:
    session = session or make_session()
    url = f"{POKEAPI_BASE}/pokemon?limit={limit}&offset={offset}"
    logger.info(f"Fetching pokemon list: {url}")
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])

def get_pokemon_details(identifier: str, session: Optional[requests.Session] = None) -> Dict[str, Any]:
    session = session or make_session()
    url = f"{POKEAPI_BASE}/pokemon/{identifier}"
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def build_dataset(limit: int = 100, offset: int = 0, request_delay: float = 0.05) -> pd.DataFrame:
    session = make_session()
    base_list = get_pokemon_list(limit=limit, offset=offset, session=session)
    records = []
    for idx, entry in enumerate(base_list, 1):
        name_url = entry.get("url", "")
        identifier = name_url.rstrip("/").split("/")[-1] if name_url else entry.get("name")
        try:
            details = get_pokemon_details(identifier, session=session)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch details for {identifier}: {e}")
            continue

        poke_id = details.get("id")
        base_exp = details.get("base_experience")
        name = str(details.get("name", "")).title()

        # Types
        types = [t["type"]["name"].title() for t in details.get("types", []) if "type" in t and "name" in t["type"]]

        # Stats mapping
        stats_map = {s["stat"]["name"].lower(): s.get("base_stat")
                     for s in details.get("stats", []) if "stat" in s and "name" in s["stat"]}

        record = {
            "ID": poke_id,
            "Nome": name,
            "Experiencia Base": base_exp,
            "Tipos": types,
            "HP": stats_map.get("hp"),
            "Ataque": stats_map.get("attack"),
            "Defesa": stats_map.get("defense"),
        }
        records.append(record)
        if request_delay and idx < len(base_list):
            time.sleep(request_delay)

    df = pd.DataFrame.from_records(records)
    # Ensure column order
    cols = ["ID", "Nome", "Experiencia Base", "Tipos", "HP", "Ataque", "Defesa"]
    df = df[cols]
    return df
