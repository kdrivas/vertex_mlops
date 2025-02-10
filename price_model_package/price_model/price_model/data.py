import pandas as pd
from sklearn.model_selection import train_test_split 

from price_model.constants import (
    TARGET_COL,
    ONE_HOT_RETAILER_COLS,
    ONE_HOT_COLOR_COLS,
    SELECTED_COLS,
)


def preprocess_data(df: pd.DataFrame) -> [pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    df = df.copy()

    df = df.drop_duplicates()
    df[TARGET_COL] = df[TARGET_COL].str.extract(r"(\d+(\.\d+)?)")[0].astype(float)

    train, test = train_test_split(df, test_size = 0.10, random_state = 0)
    X_train, y_train = train.drop(TARGET_COL, axis=1), train[TARGET_COL]
    X_test, y_test = test.drop(TARGET_COL, axis=1), test[TARGET_COL]

    return X_train, y_train, X_test, y_test


def create_features(df: pd.DataFrame, train: bool = True) -> pd.DataFrame:
    """This function creates features for the data."""

    df = df.copy() 

    df["retailer_l"] = df["retailer"].str.lower()
    for col in ONE_HOT_RETAILER_COLS:
        df[col] = df["retailer_l"].str.contains(col)

    reg = r"|".join(ONE_HOT_RETAILER_COLS)
    df["other_retailer"] = ~df["retailer_l"].str.contains(
        reg,
        case=False,
        na=False,
    )

    df["color_l"] = df["color"].str.lower()
    for col in ONE_HOT_COLOR_COLS:
        df[col] = df["color_l"].str.contains(col)

    reg = r"|".join(ONE_HOT_COLOR_COLS)
    df["other_color"] = ~df["color_l"].str.contains(
        reg,
        case=False,
        na=False,
    )

    df["mrp"] = df["mrp"].str.extract(r"(\d+(\.\d+)?)")[0].astype(float)

    df["product_name_len"] = df["product_name"].str.len()
    df["description_len"] = df["description"].str.len()

    df["rating_nan"] = df["rating"].isnull()

    df = df[SELECTED_COLS]

    return df
