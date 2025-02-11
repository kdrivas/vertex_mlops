import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error as MSE 

from price_model.constants import MODEL_PARAMS


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> xgb.core.Booster:
    """This function creates features for the data."""
    train_dmatrix = xgb.DMatrix(data=X_train, label=y_train) 
    xgb_model = xgb.train(params=MODEL_PARAMS, dtrain=train_dmatrix)

    return xgb_model


def evaluate_model(model: xgb.core.Booster, X_test: pd.DataFrame, y_test: pd.Series) ->  float:
    test_dmatrix = xgb.DMatrix(data=X_test,label=y_test)    
    pred = model.predict(test_dmatrix) 

    rmse = np.sqrt(MSE(y_test, pred)) 

    return rmse
