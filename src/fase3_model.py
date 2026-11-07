"""Reusable modeling helpers for Phase 3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, cross_validate
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET = "grades"
FEATURES = [
    "gaming_hours",
    "study_hours",
    "sleep_hours",
    "attendance",
    "uso_no_gaming",
]
FEATURE_SET_CANDIDATES = {
    "Fase 2 + uso_no_gaming": FEATURES,
    "Fase 3 + social_activity": [
        "gaming_hours",
        "study_hours",
        "sleep_hours",
        "attendance",
        "social_activity",
    ],
    "Ambos complementarios": [
        "gaming_hours",
        "study_hours",
        "sleep_hours",
        "attendance",
        "uso_no_gaming",
        "social_activity",
    ],
}
RANDOM_STATE = 42


def build_models() -> dict[str, Pipeline | RegressorMixin]:
    """Return the baseline and the three candidate model families."""
    return {
        "DummyRegressor": DummyRegressor(strategy="mean"),
        "Linear Regression": Pipeline(
            [("scaler", StandardScaler()), ("model", LinearRegression())]
        ),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1
        ),
        "KNN": Pipeline(
            [("scaler", StandardScaler()), ("model", KNeighborsRegressor())]
        ),
    }


def parameter_grids() -> dict[str, dict[str, list[Any]]]:
    """Return modest grids suitable for reproducible classroom execution."""
    return {
        "Linear Regression": {},
        "Random Forest": {
            "n_estimators": [200, 300],
            "max_depth": [None, 10, 20],
            "min_samples_leaf": [1, 3],
        },
        "KNN": {
            "model__n_neighbors": [5, 11, 21, 31],
            "model__weights": ["uniform", "distance"],
            "model__p": [1, 2],
        },
    }


def regression_metrics(y_true: pd.Series, predictions: np.ndarray) -> dict[str, float]:
    """Calculate metrics, omitting undefined MAPE terms when grades are zero."""
    nonzero = y_true != 0
    mape = (
        float(np.mean(np.abs((y_true[nonzero] - predictions[nonzero]) / y_true[nonzero])) * 100)
        if nonzero.any()
        else float("nan")
    )
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y_true, predictions))),
        "MAE": float(mean_absolute_error(y_true, predictions)),
        "MAPE (%)": mape,
        "R2": float(r2_score(y_true, predictions)),
    }


def cross_validate_models(
    X_train: pd.DataFrame, y_train: pd.Series, cv: KFold
) -> pd.DataFrame:
    """Compare baseline and candidate families using the same folds."""
    rows: list[dict[str, float | str]] = []
    scoring = {
        "rmse": "neg_root_mean_squared_error",
        "mae": "neg_mean_absolute_error",
        "r2": "r2",
    }
    for name, model in build_models().items():
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring, n_jobs=1)
        rows.append(
            {
                "Modelo": name,
                "RMSE CV": float(-scores["test_rmse"].mean()),
                "MAE CV": float(-scores["test_mae"].mean()),
                "R2 CV": float(scores["test_r2"].mean()),
                "RMSE CV std": float(scores["test_rmse"].std()),
            }
        )
    return pd.DataFrame(rows).sort_values("RMSE CV").reset_index(drop=True)


def compare_feature_sets(
    df: pd.DataFrame, y: pd.Series, cv: KFold
) -> pd.DataFrame:
    """Compare documented predictor alternatives using identical CV folds."""
    rows: list[dict[str, float | str]] = []
    scoring = {
        "rmse": "neg_root_mean_squared_error",
        "mae": "neg_mean_absolute_error",
        "r2": "r2",
    }
    for feature_set_name, features in FEATURE_SET_CANDIDATES.items():
        X = df[features]
        for model_name, model in build_models().items():
            scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=1)
            rows.append(
                {
                    "Conjunto de predictores": feature_set_name,
                    "Modelo": model_name,
                    "RMSE CV": float(-scores["test_rmse"].mean()),
                    "MAE CV": float(-scores["test_mae"].mean()),
                    "R2 CV": float(scores["test_r2"].mean()),
                }
            )
    return pd.DataFrame(rows).sort_values("RMSE CV").reset_index(drop=True)


def tune_models(
    X_train: pd.DataFrame, y_train: pd.Series, cv: KFold
) -> tuple[dict[str, GridSearchCV | Pipeline], pd.DataFrame]:
    """Tune the three non-baseline families with identical cross-validation."""
    fitted: dict[str, GridSearchCV | Pipeline] = {}
    rows: list[dict[str, float | str]] = []
    models = build_models()
    for name in ("Linear Regression", "Random Forest", "KNN"):
        estimator = models[name]
        grid = parameter_grids()[name]
        if not grid:
            fitted[name] = estimator.fit(X_train, y_train)
            rows.append({"Modelo": name, "RMSE CV optimizado": float("nan"), "Mejores parámetros": {}})
            continue
        search = GridSearchCV(
            estimator,
            grid,
            scoring="neg_root_mean_squared_error",
            cv=cv,
            n_jobs=1,
            refit=True,
        )
        search.fit(X_train, y_train)
        fitted[name] = search
        rows.append(
            {
                "Modelo": name,
                "RMSE CV optimizado": float(-search.best_score_),
                "Mejores parámetros": search.best_params_,
            }
        )
    return fitted, pd.DataFrame(rows)


def evaluate_fitted_models(
    fitted: dict[str, GridSearchCV | Pipeline],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    """Evaluate fitted estimators on the untouched test split."""
    rows = []
    predictions: dict[str, np.ndarray] = {}
    for name, model in fitted.items():
        pred = model.predict(X_test)
        predictions[name] = pred
        rows.append({"Modelo": name, **regression_metrics(y_test, pred)})
    return pd.DataFrame(rows).sort_values("RMSE").reset_index(drop=True), predictions


def save_bundle(model: object, path: str | Path) -> None:
    """Persist the model and its input contract for inference."""
    bundle = {"model": model, "features": FEATURES, "target": TARGET}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path)
