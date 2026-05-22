from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re
import pandas as pd


class RangeMapper(BaseEstimator, TransformerMixin):
    """Map human-readable range-like strings to numeric values.

    Heuristic rules:
    - 'none' -> 0
    - 'new' -> 0
    - 'x to y' -> mean(x,y) if numbers present
    - 'more than N' -> N+1
    - 'less than N' -> max(0, N-1)
    - extract first integer if single number present
    - otherwise return NaN
    """

    def fit(self, X, y=None):
        return self

    def _parse_val(self, v):
        if pd.isna(v):
            return np.nan
        s = str(v).strip()
        if s.lower() in ("none", "no", "new"):
            return 0.0
        # matches numbers
        nums = re.findall(r"-?\d+", s)
        if "to" in s and len(nums) >= 2:
            a, b = float(nums[0]), float(nums[1])
            return (a + b) / 2.0
        if "more than" in s.lower() and len(nums) >= 1:
            return float(nums[-1]) + 1.0
        if "less than" in s.lower() and len(nums) >= 1:
            return max(0.0, float(nums[-1]) - 1.0)
        if len(nums) == 1:
            return float(nums[0])
        # fallback: try to map some common words
        return np.nan

    def transform(self, X):
        # X may be 1d or 2d; preserve shape
        arr = np.array(X)
        orig_shape = arr.shape
        flat = arr.ravel()
        mapped = [self._parse_val(v) for v in flat]
        mapped = np.array(mapped, dtype=float)
        return mapped.reshape(orig_shape)


def range_mapper_transform(arr):
    """Top-level wrapper for RangeMapper.transform to allow pickling.

    Joblib/pickle cannot serialize locally defined lambdas. Using a
    top-level function ensures the transformer is picklable.
    """
    return RangeMapper().transform(arr)


def build_preprocessor(df, target_column):
    df = df.copy()

    # drop obvious identifier and low-utility columns
    drop_cols = [c for c in ("PolicyNumber", "RepNumber") if c in df.columns]
    df.drop(columns=drop_cols, inplace=True, errors="ignore")

    # drop Year if constant
    if "Year" in df.columns and df["Year"].nunique() <= 1:
        df.drop(columns=["Year"], inplace=True)

    # fix Age zeros as missing values (will impute)
    if "Age" in df.columns:
        df.loc[df["Age"] == 0, "Age"] = np.nan

    X = df.drop(columns=[target_column]) if target_column in df.columns else df

    # define columns that should be converted from human-readable ranges to numeric
    range_like_cols = [
        c for c in [
            "VehiclePrice",
            "Days_Policy_Accident",
            "Days_Policy_Claim",
            "PastNumberOfClaims",
            "AgeOfVehicle",
            "NumberOfSuppliments",
            "NumberOfCars",
        ]
        if c in X.columns
    ]

    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
    # remove range-like cols from categoricals so they are handled separately
    categorical_features = [c for c in categorical_features if c not in range_like_cols]

    numerical_features = X.select_dtypes(exclude=["object"]).columns.tolist()

    # numeric transformer: impute then scale
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # range-like transformer: map to numeric, impute, scale
    range_transformer = Pipeline(
        steps=[
            ("mapper", FunctionTransformer(range_mapper_transform, validate=False)),
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    transformers = []
    if numerical_features:
        transformers.append(("num", numeric_transformer, numerical_features))
    if range_like_cols:
        transformers.append(("range", range_transformer, range_like_cols))
    if categorical_features:
        transformers.append(("cat", categorical_transformer, categorical_features))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    return preprocessor