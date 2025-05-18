import os
import click
import pandas as pd

import mlflow


def cut(df: pd.DataFrame, crop_type: str) -> pd.DataFrame:
            if crop_type != 'threecrops':
                filtered = df[df['Crop.type'] == crop_type]
                cols = {
                    'Maize': ["Yield", "Slope", "Irrigation", "Cropping.system.in.the.site", 
                            "Rotational.systems", "Name.of.previous.crop", "Growing.days", 
                            "GDD", "Tmax", "Tmin", "PRE", "RAD", "Soil.type", "SOC", "OP", 
                            "AK", "PH", "PK.fert", "N.fert", "SAND", "SILT", "CLAY", 
                            "AWC", "Bulk.density", "Crop.variety", "AI", "PET10"],
                    'Wheat': ["Yield", "Slope", "Irrigation", "Cropping.system.in.the.site",
                            "Rotational.systems", "Name.of.previous.crop", "Growing.days",
                            "GDD", "Tmax", "Tmin", "PRE", "RAD", "Soil.type", "SOC", "OP",
                            "AK", "PH", "PK.fert", "N.fert", "SAND", "SILT", "CLAY",
                            "AWC", "Bulk.density", "Crop.variety", "AI", "PET10"],
                    'Rice': ["Yield", "Slope", "Cropping.system.in.the.site", 
                            "Rotational.systems", "Growing.days", "GDD", "Tmax", "Tmin", 
                            "PRE", "RAD", "Soil.type", "SOC", "OP", "AK", "PH", "PK.fert", 
                            "N.fert", "SAND", "SILT", "CLAY", "AWC", "Bulk.density", 
                            "Crop.variety", "AI", "PET10"]
                }
                return filtered[cols[crop_type]]
            else:
                cols = ["Yield.normalized", "Slope", "Irrigation", "Cropping.system.in.the.site",
                    "Rotational.systems", "Name.of.previous.crop", "Growing.days", "GDD",
                    "Tmax", "Tmin", "PRE", "RAD", "Soil.type", "SOC", "OP", "AK", "PH",
                    "PK.fert", "N.fert", "SAND", "SILT", "CLAY", "AWC", "Bulk.density",
                    "Crop.variety", "AI", "PET10"]
                return df[cols]
            

@click.command(
        help="从 data.csv 文件中读取数据并取出对应作物数据集, 并保存为Mlflow artifact"
        " (pd.DataFrame) for use.' "
)
@click.option("--file-path", default="./data.csv")
@click.option("--crop-type", default="Maize")
def prepare_data(
        file_path: str = './data.csv',
        crop_type: str = "Maize") -> None:
    
    with mlflow.start_run() as run:

        data = pd.read_csv(file_path, index_col="Coden")

        processed = cut(data, crop_type)
        if crop_type == "threecrop":
            processed['Yield.normalized'] = processed['Yield.normalized'] / 1000
        else:
            processed['Yield'] = processed['Yield'] / 1000
        
        # 只保存当前作物类型数据
        os.makedirs("processed_data", exist_ok=True)
        filename = f"processed_data/{crop_type.lower()}_data.csv"
        processed.to_csv(filename)
        mlflow.log_artifact(filename, artifact_path="processed_data")
        
        print(f"Artifact saved at: {mlflow.get_artifact_uri()}/processed_data/{filename}")
            
        # 记录当前运行ID供后续使用
        mlflow.log_param("preprocessing_crop_type", crop_type)
        mlflow.set_tag("mlflow.project.entryPoint", "data_prepare")

if __name__ == '__main__':
    prepare_data()