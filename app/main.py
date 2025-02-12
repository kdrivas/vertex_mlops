from fastapi import FastAPI, Request

import joblib
import numpy as np
import os

from google.cloud import storage

from price_model.data import feature_eng_data

app = FastAPI()
gcs_client = storage.Client(os.environ["PROJECT_ID"])

with open("model.joblib", "wb") as model_f:
    gcs_client.download_blob_to_file(
        f"{os.environ["AIP_STORAGE_URI"]}/model.joblib", model_f
    )

_model = joblib.load("model.joblib")


@app.post(os.environ["AIP_PREDICT_ROUTE"])
async def predict(request: Request):
    body = await request.json()

    instances = body["instances"]
    inputs = np.asarray(instances)
    feats = feature_eng_data(inputs)
    print(feats.shape)
    outputs = _model.predict(feats)

    return {"predictions": outputs}


@app.get(os.environ["AIP_HEALTH_ROUTE"], status_code=200)
def health():
    return {}
