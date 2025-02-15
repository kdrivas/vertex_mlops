# test-task

## Content
1) Folder structure
2) Project overview
3) Endpoint
4) Comments and Improvements

## Folder structure

```
vertex_mlops
├── Dockerfile
├── Dockerfile.server      
├── README.md 
├── app                                   # Fastapi deployed in Vertex endpoint
│   ├── main.py
│   └── prestart.sh
├── cloud_function                        # Swagger configuration
│   ├── main.py
│   ├── openapi.yaml
│   └── requirements.txt
├── docs
├── infra
│   ├── artifact.tf
│   ├── iam.tf
│   ├── project.tf
│   ├── provider.tf
│   ├── storage.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── pipelines   
│   ├── run_pipeline.py
│   └── train_pipeline.py
├── poetry.lock
├── price_model                             # Pricing model package
│   ├── __init__.py
│   ├── constants.py
│   ├── data.py
│   └── model.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── tests
    ├── __init__.py
    └── test_data.py
```

## Project overview
- The first step was to create a training pipeline in kubeflow. The pipeline creates a trained model and registers it to model registry.
The figure below shows the steps of the kubeflow pipeline.
 <img src="docs/kubeflow_pipeline.png" >
- The following diagram contains the app architecture
<img src="docs/app_architecture.png" >

## Endpoint

### Prediction
Get the prediction given a name

**URL** : `https://price-api-3ijz0oh4.uc.gateway.dev/predict`

**Method** : `POST`

#### Data
 - product_name
 - mrp
 - price
 - pdp_url
 - brand_name
 - product_category
 - retailer
 - description
 - rating
 - review_count
 - style_attributes
 - total_sizes
 - available_size
 - color

#### Example

```
curl -X POST "https://price-api-3ijz0oh4.uc.gateway.dev/predict" \
     -H "Content-Type: application/json" \
     -d "@test.json"
```

#### Response

**Code** : `200 OK`

```json
{
    "predictions":[ 13.07923984527588 ]
}
```

## Comments and Improvements
- Use a tool to monitor metrics of the API such as latency, error count.
- Integrate a tool to send alerts if a SLO was achieved, for example, if the average latency in the last day was higher than 15sec
- Improve CI/CD pipeline and deploy the vertex endpoint (I didn't have enough time to include it)
- Use Redis to reduce time, this is not a big improvement for this app due to its simplicity, but could be a good improvement for complex models
