# 由 Mlflow管理的 SOC 数据模型

## 项目构成
    ├── mlruns                  # .gitignore 运行文件
    ├── MLproject               # Mlflow 项目文件
    ├── data.csv                # 数据文件 
    ├── data_prepare.py         # 数据预处理

    ├── main.py                 # pipeline 主入口

    ├── train_model.py          # 训练模型
    ├── pipeline_utils.py       # pipeline运行组件
    ├── post_test.py            # 模型post测试程序
    
    ├── conda_env.yaml          # conda 环境
    ├── python_env.yaml         # python环境    ├── requirements.txt        # python依赖

    └── README.md               # 自述
## 介绍

## Mlflow