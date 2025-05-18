# pipeline_utils.py
import subprocess
from typing import Dict, Optional
from mlflow.tracking import MlflowClient
from mlflow.entities import Run, RunStatus
from mlflow.utils.mlflow_tags import MLFLOW_GIT_COMMIT, MLFLOW_PROJECT_ENTRY_POINT
import mlflow

def _get_git_commit() -> str:
    """获取当前git commit hash"""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                      stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "no_git"

def _already_ran(
    entry_point_name: str,
    parameters: Dict,
    experiment_id: Optional[str] = None
) -> Optional[Run]:
    """检查是否存在相同参数的已完成运行"""
    client = MlflowClient()
    experiment_id = experiment_id or mlflow.active_run().info.experiment_id
    
    # 构建查询条件
    filter_str = f"tags.{MLFLOW_PROJECT_ENTRY_POINT} = '{entry_point_name}'"
    
    # 参数匹配检查
    param_checks = [f"params.{k} = '{v}'" for k, v in parameters.items()]
    if param_checks:
        filter_str += " and " + " and ".join(param_checks)
    
    runs = client.search_runs(
        experiment_ids=[experiment_id],
        filter_string=filter_str,
        max_results=1
    )
    
    if not runs:
        return None
        
    candidate_run = runs[0]
    # 检查运行状态
    if candidate_run.info.status != RunStatus.FINISHED:
        print(f'Run {candidate_run.info.run_id} found but status is {candidate_run.info.status}, skipping reuse')
        return None
    
    # 检查代码版本
    current_commit = _get_git_commit()
    run_commit = candidate_run.data.tags.get(MLFLOW_GIT_COMMIT)
    if run_commit and current_commit != run_commit:
        print(f"Code version mismatch (current: {current_commit}, run: {run_commit}), skipping reuse")
        return None
    
    return candidate_run

def get_or_run(
    entry_point: str,
    parameters: Dict,
    use_cache: bool = True
) -> Run:
    """获取或执行指定步骤"""
    experiment = mlflow.get_experiment(mlflow.active_run().info.experiment_id)
    git_commit = _get_git_commit()
    
    if use_cache:
        existing_run = _already_ran(entry_point, parameters, experiment.experiment_id)
        if existing_run:
            print(f"Reusing cached run {existing_run.info.run_id} for {entry_point} with params {parameters}")
            return existing_run
    
    print(f"Launching new run for {entry_point} with params {parameters}")
    submitted_run = mlflow.run(
        ".", 
        entry_point,
        parameters=parameters,
        env_manager="local"
    )
    run = MlflowClient().get_run(submitted_run.run_id)
    
    # 记录代码版本
    if git_commit != "no_git":
        mlflow.set_tag(MLFLOW_GIT_COMMIT, git_commit)
    mlflow.set_tag(MLFLOW_PROJECT_ENTRY_POINT, entry_point)
    
    return run