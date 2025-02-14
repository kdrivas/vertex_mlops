from kfp import compiler
from google.cloud import aiplatform as vertexai

import argparse
from datetime import datetime

from train_pipeline import kfp_pipeline


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--project_id", default="sublime-sunspot-431116-t0", type=str)
    parser.add_argument("--location", default="us-central1", type=str)
    parser.add_argument("--template_path", default="custom_train_pipeline.json", type=str)
    parser.add_argument("--serving_container_image_uri", default= "us-central1-docker.pkg.dev/sublime-sunspot-431116-t0/pred-api-container/endpoint:latest", type=str)
    parser.add_argument("--model_name", default="price-model", type=str)
    parser.add_argument("--model_version", default="1.0.0", type=str)
    parser.add_argument("--bucket_uri", default="gs://vertex-artifacts-bucket", type=str)
    parser.add_argument("--pipeline_root", default="gs://vertex-artifacts-bucket/pipeline", type=str)

    return parser.parse_args()


def run_compile(package_path="custom_train_pipeline.json"):
    compiler.Compiler().compile(pipeline_func=kfp_pipeline, package_path=package_path)


if __name__ == "__main__":
    args = parse_args()

    vertexai.init(project=args.project_id, staging_bucket=args.bucket_uri)
    run_compile(package_path=args.template_path)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    model_display_name = args.model_name + "-" + args.model_version
    job_id = "custom-train-pipeline-{0}".format(timestamp)

    job = vertexai.PipelineJob(
        display_name=args.model_name,
        template_path=args.template_path,
        job_id=job_id,
        pipeline_root=args.pipeline_root,
        parameter_values={
            "project": args.project_id,
            "location": args.location,
            "model_display_name": args.model_display_name,
            "serving_container_image_uri": args.serving_container_image_uri,
        },
        enable_caching=False,
    )

    job.submit(experiment=args.model_name)    
