# Feature engineering constants
ONE_HOT_RETAILER_COLS = [ 
    "victoria",
    "macys",
    "hankypanky",
    "amazon",
    "ae",
    "nordstrom",
    "calvin",
    "btemptd",
    "topshop",
]

ONE_HOT_COLOR_COLS = ["black", "white", "pink", "blue", "red", "green", "bayberry", "lilac", "maroon"]

SELECTED_COLS = ONE_HOT_COLOR_COLS + ONE_HOT_RETAILER_COLS + [
    "other_retailer",
    "other_color",
    "mrp",
    "product_name_len",
    "description_len",
    "rating",
    "rating_nan",
    "review_count",
]

TARGET_COL = "price"

# Model configuration constants
MODEL_PARAMS = {
    "objective":"reg:squarederror",
    "max_depth": 10,
}

MODEL_VERSION = "1_0_0"
