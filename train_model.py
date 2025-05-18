import mlflow
import click
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.metrics import mean_squared_error
from mlflow.models import infer_signature
from mlflow import MlflowClient
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe



# sklearn 模型需要One-hot预处理
def onehot_encoder(crop_type: pd.DataFrame):

    factor = crop_type.select_dtypes(include='object').columns.tolist()
    for _ in factor:
        one_hot = pd.get_dummies(crop_type[_], prefix=_, dtype=int)
        crop_type = pd.concat([crop_type, one_hot], axis=1)

    crop_type = crop_type.drop(columns=factor)
    return crop_type


# 数据集分割
def split_dataset(dataset: pd.DataFrame, test_ratio: float=0.30, random_state=42):
    np.random.seed(random_state)
    test_indices = np.random.rand(len(dataset)) < test_ratio
    return dataset[~test_indices], dataset[test_indices]

# 训练模型
def train_model4mlflow_hyperopt(
        params: dict = {},
        train_X: pd.DataFrame = None,
        train_y: pd.DataFrame = None,
        test_X: pd.DataFrame = None,
        test_y: pd.DataFrame = None,
        signature: object = None
) -> dict:

    rf_model = RandomForestRegressor(
                                n_estimators=int(params['n_estimators']),
                                max_features=int(params['max_features']),
                                oob_score=True,
                                random_state=123)
    
    with mlflow.start_run(nested=True):
        rf_model.fit(train_X, train_y)

        pred_y = rf_model.predict(test_X)
        eval_mse = mean_squared_error(test_y, pred_y)

        mlflow.log_params(params)
        mlflow.log_metric("eval_mse", eval_mse)
    
        # Log model
        mlflow.sklearn.log_model(rf_model, "model", signature=signature)

        return {"loss": eval_mse, "status": STATUS_OK, "model": rf_model}
    


def train_model4mlflow(
        params: dict = {},
        train_X: pd.DataFrame = None,
        train_y: pd.DataFrame = None,
        test_X: pd.DataFrame = None,
        test_y: pd.DataFrame = None,
) -> dict:
    
    rf_model = RandomForestRegressor(
                                n_estimators=params['n_estimators'],
                                max_features=params['max_features'],
                                oob_score=True,
                                random_state=123)
    
    
    rf_model.fit(train_X, train_y)
    
    pred_y = rf_model.predict(test_X)
    eval_mse = mean_squared_error(test_y, pred_y)
    signature = infer_signature(train_X, rf_model.predict(train_X))

    mlflow.log_params(params)
    mlflow.log_metric("eval_mse", eval_mse)

    importance = pd.Series(rf_model.feature_importances_, index=train_X.columns)
    mlflow.log_text(importance.to_csv(), "feature_importance.csv")

    return rf_model, signature
   

def rf_sklearn_evaulate_model(
        model,
        test_data: pd.DataFrame,
        label: str = 'Yield'
) -> float:
    # test_ds_pd = onehot_encoder(test_data)

    X = test_data.drop(columns=[label])
    y = test_data[label]

    pred_y = model.predict(X)
    mse_score = mean_squared_error(y, pred_y)
    # r2 = r2_score(y, pred)
    # oob = model.oob_score_

    return mse_score

@click.command(help="使用预处理后的数据")
@click.option("--preprocessing-run-id", help="预处理步骤的Run ID", required=True)
@click.option("--crop-type", required=True, type=click.Choice(['Maize', 'Wheat', 'Rice', 'threecrops']))
@click.option("--hyperopt", default=False, help="是否运行超参数优化")
def train_model(
        preprocessing_run_id: str, 
        crop_type: str = 'Maize',
        hyperopt: bool = False
) -> None:
    
    np.random.seed(42)

    # 自动超参调优 参数及范围
    space = {
        "n_estimators": hp.uniformint("n_estimators", 100, 1000),
        "max_features": hp.uniformint("max_features", 3, 8)
    }

    params = {
            'n_estimators': 500,
            'max_features': 5,
            'oob_score': True,
            'random_state': 123,
    }

    client = MlflowClient()
    data_run = client.get_run(preprocessing_run_id)
    artifact_uri = f"{data_run.info.artifact_uri}/processed_data/{crop_type.lower()}_data.csv"
    
    # 直接使用本地路径加载
    local_path = mlflow.artifacts.download_artifacts(artifact_uri)
    df = pd.read_csv(local_path)
    # mlflow自动记录 https://mlflow.org/docs/latest/tracking/autolog
    mlflow.sklearn.autolog()

    # 加载数据
    #artifact_uri = f"runs:/{preprocessing_run_id}/processed_data/{crop_type.lower()}_data.csv"
    # try:
    #     df = pd.read_csv(mlflow.get_artifact_uri(artifact_uri))
    # except FileNotFoundError:
    #     raise ValueError(f"Artifact not found: {artifact_uri}")
 
    label = 'Yield'
    df = onehot_encoder(df)
    train_ds_pd, test_ds_pd = split_dataset(df, random_state=42)
    train_X = train_ds_pd.drop(columns=[label])
    train_y = train_ds_pd[label]
    test_X = test_ds_pd.drop(columns=[label])
    test_y = test_ds_pd[label]
    
    mlflow.log_param("crop_type", crop_type)
    mlflow.set_tag("mlflow.project.entryPoint", "train_model")

    if hyperopt:
        # TODO sinature 此处推断不正确
        signature = infer_signature(train_X, train_y)

        with mlflow.start_run(nested=True):
            def objective(params):
                # MLflow will track the parameters and results for each run
                result = train_model4mlflow_hyperopt(
                    params,
                    train_X=train_X,
                    train_y=train_y,
                    test_X=test_X,
                    test_y=test_y,
                    signature=signature
                )
                return result
            trails = Trials()
            best = fmin(
                fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=8,
                trials=trails,
            )
            best_run = sorted(trails.results, key=lambda x: x["loss"])[0]
            # Log the hyperparameters
            mlflow.log_params(best)

            # Log the mse metric
            mlflow.log_metric("eval_mse", best_run["loss"])

            mlflow.sklearn.log_model(
                sk_model=best_run["model"],
                artifact_path="model",
                input_example=train_X,
                signature=signature,
                # artifact_path=artifact_path
            )  

            print(f"Best parameters: {best}")
            print(f"Best eval mse: {best_run['loss']}")
    else:
        rf_model, signature = train_model4mlflow(
                params=params,
                train_X=train_X,
                train_y=train_y,
                test_X=test_X,
                test_y=test_y)

        # Log the model
        mlflow.sklearn.log_model(
            sk_model=rf_model,
            artifact_path="model",
            signature=signature,
            input_example=train_X,
            registered_model_name="注册模型",
        )


if __name__ == "__main__":
    train_model()