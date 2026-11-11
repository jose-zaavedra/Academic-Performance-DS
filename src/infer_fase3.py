"""Apply the Phase 3 model to a CSV containing the five predictor columns."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument(
        "--model", type=Path, default=Path("output/fase3/fase3_modelo_ganador.joblib")
    )
    args = parser.parse_args()

    bundle = joblib.load(args.model)
    features = bundle["features"]
    missing = [column for column in features if column not in pd.read_csv(args.input_csv, nrows=0).columns]
    if missing:
        raise ValueError(f"Faltan predictores requeridos: {missing}")

    data = pd.read_csv(args.input_csv)
    predictions = bundle["model"].predict(data[features])
    result = data.copy()
    result["grades_predicted"] = predictions
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_csv, index=False)
    print(f"Predicciones guardadas en {args.output_csv} ({len(result)} filas).")


if __name__ == "__main__":
    main()
