from kfp.dsl import pipeline, component, If, Input, Output, Dataset, Model, Artifact


@component(base_image="cap2nemo/price-model:latest")
def preprocess_data_component(
    train_preprocessed_data: Output[Dataset],
    test_preprocessed_data: Output[Dataset],
    train_labels_data: Output[Dataset],
    test_labels_data: Output[Dataset],
):
    """
    Preprocess the data.

    Args:
        processed_train_data (Output[Dataset]): Path to the train data.
        processed_test_data (Output[Dataset]): Path to the test data.
        train_labels_data (Output[Dataset]): Path to the train labels.
        test_labels_data (Output[Dataset]): Path to the test labels.
    """

    from price_model.data import preprocess_data
    import joblib
    import pandas as pd
    from eccd_datasets import load_lingerie

    datasets = load_lingerie()
    df = pd.concat([datasets[k] for k in datasets.keys()], axis=0)

    X_train, y_train, X_test, y_test = preprocess_data(df)

    joblib.dump(X_train, train_preprocessed_data.path)
    joblib.dump(X_test, test_preprocessed_data.path)
    joblib.dump(y_train, train_labels_data.path)
    joblib.dump(y_test, test_labels_data.path)


@component(base_image="cap2nemo/price-model:latest")
def feature_engineering_component(
    train_preprocessed_data: Input[Dataset],
    test_preprocessed_data: Input[Dataset],
    train_features_data: Output[Dataset],
    test_features_data: Output[Dataset],
):
    """
    Run feature engineering using the preprocessed data.

    Args:
        processed_data (Input[Dataset]): Path to the preprocessed data.
        features (Output[Dataset]): Path to the features.
    """

    from price_model.data import feature_eng_data
    import joblib

    df_train = joblib.load(train_preprocessed_data.path)
    df_test = joblib.load(test_preprocessed_data.path)
    
    df_train_feat = feature_eng_data(df_train)
    df_test_feat = feature_eng_data(df_test)

    joblib.dump(df_train_feat, train_features_data.path)
    joblib.dump(df_test_feat, test_features_data.path)


@component(base_image="cap2nemo/price-model:latest")
def train_model_component(
    train_features_data: Input[Dataset],
    train_labels_data: Input[Dataset],
    model: Output[Model],
):
    """
    Run feature engineering using the preprocessed data.

    Args:
        processed_data (Input[Dataset]): Path to the preprocessed data.
        features (Output[Dataset]): Path to the features.
    """

    from price_model.model import train_price_model
    import joblib

    X_train = joblib.load(train_features_data.path)
    y_train = joblib.load(train_labels_data.path)
    print(X_train.head())

    xgb_model = train_price_model(X_train, y_train)

    joblib.dump(xgb_model, model.path)


@component(base_image="cap2nemo/price-model:latest")
def evaluate_model_component(
    test_features_data: Input[Dataset],
    test_labels_data: Input[Dataset],
    model: Input[Model],
    eval_metrics: Output[Artifact],
):
    """
    Evaluates the trained model.

    Args:
        processed_test_data (Input[Dataset]): Input processed test data.
        test_labels_data (Input[Dataset]): Input test labels data.
        model (Input[Model]): Input trained model.
        evaluation_metrics (Output[Artifact]): Output evaluation metrics.
    """
    from price_model.model import evaluate_model
    import joblib
    import json

    xgb_model = joblib.load(model.path)
    X_test = joblib.load(test_features_data.path)
    y_test = joblib.load(test_labels_data.path)

    test_rmse = evaluate_model(xgb_model, X_test, y_test)

    with open(eval_metrics.path, "w") as f:
        json.dump({"rmse": test_rmse}, f)


@component(base_image="cap2nemo/price-model:latest")
def register_model_component(
    project: str,
    location: str,
    model_display_name: str,
    serving_container_image_uri: str,
    model: Input[Model],
    metrics: Input[Artifact],
):
    """
    Registers a model in Vertex AI Model Registry with a group name based on style.
    
    Args:
        project (str): Project ID.
        location (str): GCP location (e.g. `us-central1`).
        model (Input[Model]): Input trained model artifact.
        metrics (Input[Artifact]): Input metrics report.
    """
    import json
    from path import Path

    from google.cloud import aiplatform

    with open(metrics.path, "r") as f:
        evaluation_metrics = json.load(f)

    # Using a dummy threshold
    if evaluation_metrics["rmse"] < 10000:
        aiplatform.init(project=project, location=location)

        # Register the model
        _ = aiplatform.Model.upload(
            artifact_uri=str(Path(model.path).parent),
            display_name=model_display_name,
            serving_container_image_uri=serving_container_image_uri,
            serving_container_predict_route="/predict",  # Prediction route
            serving_container_health_route="/health",
        )


@pipeline(name="custom-pipeline")
def kfp_pipeline(project: str, location:str, model_display_name: str, serving_container_image_uri:str):
    """
    Pipeline for train and evaluate the pricing model.

    Args:
        project: Input GCP project name.
        location: Input location (e.g. `us-central1`)
        model_display_name: Model name.
        serving_container_image_uri: The container used by the endpoint.
    """

    # 1. Preprocess data
    preprocess_task = preprocess_data_component()

    # 2. Create features
    fe_task = feature_engineering_component(
        train_preprocessed_data=preprocess_task.outputs["train_preprocessed_data"],
        test_preprocessed_data=preprocess_task.outputs["test_preprocessed_data"],
    )

    # 3. Train model
    train_task = train_model_component(
        train_features_data=fe_task.outputs["train_features_data"],
        train_labels_data=preprocess_task.outputs["train_labels_data"],
    )

    # 4. Evaluate model
    evaluation_task = evaluate_model_component(
        test_features_data=fe_task.outputs["test_features_data"],
        test_labels_data=preprocess_task.outputs["test_labels_data"],
        model=train_task.outputs["model"],
    )

    # 5. Register model
    register_model_task = register_model_component(
        project=project,
        location=location,
        model_display_name=model_display_name,
        serving_container_image_uri=serving_container_image_uri,
        model=train_task.outputs["model"],
        metrics=evaluation_task.outputs["eval_metrics"],
    )
