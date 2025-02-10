import pytest
import pandas as pd

from price_model.data import create_features


@pytest.fixture
def sample_df():
    """Creates a sample dataframe for testing."""
    data = {
        "retailer": ["Victoria Secret", "Amazon", "Other"],
        "color": ["Red ligth", "Dark blue", "Other"],
        "mrp": ["$25.50", "30.99 USD", "15"],
        "product_name": ["Product 111111111", "Product 2", "Product 33333"],
        "description": ["Lorem Ipsum", "Lorem", "Ipsum"],
        "rating": [4.5, None, 3.9],
    }
    return pd.DataFrame(data)

def test_create_features(sample_df):
    """Test if create_features correctly transforms the dataframe."""
    transformed_df = create_features(sample_df)

    # Check if columns are correctly created
    assert "retailer_l" in transformed_df.columns
    assert "color_l" in transformed_df.columns
    assert "mrp" in transformed_df.columns
    assert "rating_nan" in transformed_df.columns

    # Check one-hot encoding
    assert transformed_df["amazon"].tolist() == [True, False, False]
    assert transformed_df["victoria"].tolist() == [False, True, False]
    assert transformed_df["other_retailer"].tolist() == [False, False, True]

    assert transformed_df["red"].tolist() == [True, False, False]
    assert transformed_df["blue"].tolist() == [False, True, False]
    assert transformed_df["other_color"].tolist() == [False, False, True]

    # Check numerical extraction
    assert transformed_df["mrp"].tolist() == [25.5, 30.99, 15.0]

    # Check text length calculations
    assert transformed_df["product_name_len"].tolist() == [6, 10, 5]
    assert transformed_df["description_len"].tolist() == [12, 13, 8]
