"""Télécharge les clôtures journalières et écrit quotes.json pour le portfolio.

Usage : python scripts/update_quotes.py site/quotes.json

Mêmes instruments et même méthode que le projet portfolio-risk-system :
cours ajustés Yahoo Finance, alignés sur les jours de bourse du CAC 40,
les autres séries étant reportées vers l'avant les jours sans cotation.
Le script s'arrête avec une erreur si les données sont incomplètes : le site
garde alors la dernière version valide ou, à défaut, le jeu de données intégré.
"""
import datetime as dt
import json
import pathlib
import sys

import pandas as pd
import yfinance as yf

TICKERS = {"^FCHI": "CAC40", "BNP.PA": "BNP_Paribas", "TTE.PA": "TotalEnergies",
           "GC=F": "Gold", "EURUSD=X": "EURUSD"}
DECIMALS = {"CAC40": 2, "BNP_Paribas": 2, "TotalEnergies": 2, "Gold": 2, "EURUSD": 4}
START = "2019-01-01"


def close_series(ticker: str, name: str) -> pd.Series:
    raw = yf.download(ticker, start=START, progress=False, auto_adjust=True)
    if raw.empty:
        raise RuntimeError(f"aucune donnée pour {ticker}")
    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw["Close"]
    else:
        raw = raw[["Close"]]
    return raw.iloc[:, 0].rename(name)


def main(out_path: str) -> None:
    frames = [close_series(t, n) for t, n in TICKERS.items()]
    df = pd.concat(frames, axis=1)[list(DECIMALS)]
    df = df.dropna(subset=["CAC40"]).ffill().dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)

    if len(df) < 1000:
        raise RuntimeError(f"historique trop court : {len(df)} jours")
    if (df <= 0).any().any():
        raise RuntimeError("prix négatif ou nul")
    age = (pd.Timestamp.utcnow().tz_localize(None) - df.index[-1]).days
    if age > 10:
        raise RuntimeError(f"dernière cotation trop ancienne : {age} jours")

    payload = {
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "Yahoo Finance via yfinance, cours ajustés",
        "dates": [d.strftime("%Y-%m-%d") for d in df.index],
        "px": {c: [round(float(x), DECIMALS[c]) for x in df[c]] for c in DECIMALS},
    }
    path = pathlib.Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"{len(df)} jours, dernière date {payload['dates'][-1]}, écrit dans {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "quotes.json")
