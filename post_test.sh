#!/bin/bash

# 设置主机和端口
host="localhost"
port="5002"

# 重试逻辑
max_attempts=5
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "尝试请求 (第 $attempt 次)..."
    
    # 发送请求并捕获响应
    response=$(curl -s -X POST "http://127.0.0.1:5002/invocations" \
        -H "Content-Type: application/json" \
        -d '{
            "inputs": [
                {
                    "Slope": 0.0,
                    "Growing.days": 151,
                    "GDD": 1860.9,
                    "Tmax": 27.13,
                    "Tmin": 18.86,
                    "PRE": 682.5,
                    "RAD": 1855.56,
                    "SOC": 12.41,
                    "OP": 15.6,
                    "AK": 206,
                    "PH": 5.2,
                    "PK.fert": 1,
                    "N.fert": 1.0,
                    "SAND": 35,
                    "SILT": 42,
                    "CLAY": 23,
                    "AWC": 0.147,
                    "Bulk.density": 1.38,
                    "AI": 1.238352,
                    "PET10": 810.91,
                    "Irrigation_No": 1,
                    "Irrigation_Yes": 0,
                    "Cropping.system.in.the.site_1 time a year": 1,
                    "Cropping.system.in.the.site_2 times a year": 0,
                    "Cropping.system.in.the.site_3 times a year": 0,
                    "Rotational.systems_Chili": 0,
                    "Rotational.systems_Cotton": 0,
                    "Rotational.systems_Maize": 1,
                    "Rotational.systems_Maize-buckwheat": 0,
                    "Rotational.systems_Maize-cotton": 0,
                    "Rotational.systems_Maize-garlic": 0,
                    "Rotational.systems_Maize-lima bean": 0,
                    "Rotational.systems_Maize-maize": 0,
                    "Rotational.systems_Maize-oilseed rape": 0,
                    "Rotational.systems_Maize-orchid seed": 0,
                    "Rotational.systems_Maize-pea": 0,
                    "Rotational.systems_Maize-potato": 0,
                    "Rotational.systems_Maize-radish": 0,
                    "Rotational.systems_Maize-rice": 0,
                    "Rotational.systems_Maize-soybean": 0,
                    "Rotational.systems_Maize-soybean-potato": 0,
                    "Rotational.systems_Maize-sweet potato": 0,
                    "Rotational.systems_Maize-sweet potato-vegetable": 0,
                    "Rotational.systems_Maize-taro": 0,
                    "Rotational.systems_Maize-tobacco": 0,
                    "Rotational.systems_Maize-vegetable": 0,
                    "Rotational.systems_Maize-wheat": 0,
                    "Rotational.systems_Maize-wheat-peanuts": 0,
                    "Rotational.systems_Maize-wheat-potato": 0,
                    "Rotational.systems_Maize-wheat-soilseed rape": 0,
                    "Rotational.systems_Maize-wheat-soybean": 0,
                    "Rotational.systems_Maize-wheat-sweet potato": 0,
                    "Rotational.systems_Millet": 0,
                    "Rotational.systems_Peanuts": 0,
                    "Rotational.systems_Rice": 0,
                    "Rotational.systems_Rice-broad bean": 0,
                    "Rotational.systems_Rice-garlic": 0,
                    "Rotational.systems_Rice-oilseed rape": 0,
                    "Rotational.systems_Rice-rice": 0,
                    "Rotational.systems_Rice-vegetabe": 0,
                    "Rotational.systems_Soybean": 0,
                    "Rotational.systems_Soybean-tobacco": 0,
                    "Rotational.systems_Sugarbeet": 0,
                    "Rotational.systems_Sweet potato": 0,
                    "Rotational.systems_Taro-buckwheat": 0,
                    "Rotational.systems_Tea": 0,
                    "Rotational.systems_Tobacco": 0,
                    "Rotational.systems_Watermelon": 0,
                    "Rotational.systems_Watermelon-maize": 0,
                    "Rotational.systems_Watermelon-oilseed rape": 0,
                    "Rotational.systems_Wheat": 0,
                    "Rotational.systems_Wheat-chili": 0,
                    "Rotational.systems_Wheat-cotton": 0,
                    "Rotational.systems_Wheat-peanuts": 0,
                    "Rotational.systems_Wheat-potato": 0,
                    "Rotational.systems_Wheat-rice": 0,
                    "Rotational.systems_Wheat-soybean": 0,
                    "Rotational.systems_Wheat-soybean-potato": 0,
                    "Rotational.systems_Wheat-sweet potato": 0,
                    "Rotational.systems_Wheat-tobacoo": 0,
                    "Name.of.previous.crop_Alfalfa": 0,
                    "Name.of.previous.crop_Asparagus lettuce": 0,
                    "Name.of.previous.crop_Barley": 0,
                    "Name.of.previous.crop_Broad bean": 0,
                    "Name.of.previous.crop_Buckwheat": 0,
                    "Name.of.previous.crop_Chili": 0,
                    "Name.of.previous.crop_Chinese cabbage": 0,
                    "Name.of.previous.crop_Chinese herb": 0,
                    "Name.of.previous.crop_Cotton": 0,
                    "Name.of.previous.crop_Eggplant": 0,
                    "Name.of.previous.crop_Fallow": 0,
                    "Name.of.previous.crop_Flax": 0,
                    "Name.of.previous.crop_Garlic": 0,
                    "Name.of.previous.crop_Ginseng": 0,
                    "Name.of.previous.crop_Green bean": 0,
                    "Name.of.previous.crop_Green manure crops": 0,
                    "Name.of.previous.crop_Highland barley": 0,
                    "Name.of.previous.crop_Kidney bean": 0,
                    "Name.of.previous.crop_Maize": 1,
                    "Name.of.previous.crop_Millet": 0,
                    "Name.of.previous.crop_Oilseed rape": 0,
                    "Name.of.previous.crop_Onion": 0,
                    "Name.of.previous.crop_Orchid seed": 0,
                    "Name.of.previous.crop_Pea": 0,
                    "Name.of.previous.crop_Peanuts": 0,
                    "Name.of.previous.crop_Pear": 0,
                    "Name.of.previous.crop_Potato": 0,
                    "Name.of.previous.crop_Pumpkin": 0,
                    "Name.of.previous.crop_Radish": 0,
                    "Name.of.previous.crop_Red bean": 0,
                    "Name.of.previous.crop_Rice": 0,
                    "Name.of.previous.crop_Shallot": 0,
                    "Name.of.previous.crop_Soybean": 0,
                    "Name.of.previous.crop_Sugarcane": 0,
                    "Name.of.previous.crop_Sweet potato": 0,
                    "Name.of.previous.crop_Taro": 0,
                    "Name.of.previous.crop_Tobacco": 0,
                    "Name.of.previous.crop_Tomato": 0,
                    "Name.of.previous.crop_Tree seedings": 0,
                    "Name.of.previous.crop_Vegetable": 0,
                    "Name.of.previous.crop_Watermelon": 0,
                    "Name.of.previous.crop_Wheat": 0,
                    "Soil.type_Aeolian sandy soils": 0,
                    "Soil.type_Albic soils": 0,
                    "Soil.type_Alluvial soils": 0,
                    "Soil.type_Black soils": 0,
                    "Soil.type_Brown earths": 0,
                    "Soil.type_Castanozems": 0,
                    "Soil.type_Chemozems": 0,
                    "Soil.type_Cinmon soils": 0,
                    "Soil.type_Fluvo-aquic soils": 0,
                    "Soil.type_Latosols": 0,
                    "Soil.type_Lime concretion fluvo-aquic soils": 0,
                    "Soil.type_Limestone soils": 0,
                    "Soil.type_Meadow soils": 0,
                    "Soil.type_Paddy soils": 0,
                    "Soil.type_Purplish soils": 0,
                    "Soil.type_Red earths": 0,
                    "Soil.type_Yellow earths": 1,
                    "Crop.variety_Early-maturing variety": 0,
                    "Crop.variety_Late-maturing variety": 0,
                    "Crop.variety_Medium-maturing variety": 1
                }
            ]
        }')
    
    # 检查响应状态
    if [ $? -eq 0 ]; then
        # 请求成功，检查响应内容
        echo "返回内容: $response"
        if [ "$response" = "[0.0]" ]; then
            echo "Classification: ON-Time"
            exit 0
        else
            echo "Classification: LATE"
            exit 0
        fi
    else
        # 请求失败，打印错误并重试
        echo "Caught exception attempting to call model endpoint: 请求失败"
        if [ $attempt -lt $max_attempts ]; then
            echo "Sleeping..."
            sleep 20
        fi
    fi
    
    attempt=$((attempt + 1))
done

echo "达到最大重试次数，请求失败"
exit 1