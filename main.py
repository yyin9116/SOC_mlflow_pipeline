import click
import mlflow
from pipeline_utils import get_or_run

@click.command()
@click.option("--file-path", default="./data.csv")
@click.option("--crop-type", required=True, type=click.Choice(['Maize', 'Wheat', 'Rice', 'threecrops'])) 
@click.option("--hyperopt", default=False, type=bool)
@click.option("--use-cache", default=True, type=bool)
def workflow(file_path, crop_type, hyperopt, use_cache):
    # 设置跟踪服务器和实验
    mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
    mlflow.set_experiment("MLflow_SOC_hyperopt")
    with mlflow.start_run(run_name="parent_run") as parent_run:
        data_run = get_or_run(
            entry_point="data_prepare",
            parameters={
                "file_path": file_path,
                "crop_type": crop_type
            },
            use_cache=use_cache
        )
        
        # Step 2: 模型训练（自动传递依赖的run_id）
        train_run = get_or_run(
            entry_point="train_model",
            parameters={
                "preprocessing_run_id": data_run.info.run_id,
                "crop_type": crop_type,
                "hyperopt": hyperopt
            },
            use_cache=use_cache
        )
        
        # 记录运行拓扑关系
        mlflow.log_params({
            "data_run_id": data_run.info.run_id,
            "train_run_id": train_run.info.run_id,
            "parent_run_id": parent_run.info.run_id
        })

if __name__ == "__main__":
    workflow() 