
import json
import time
import requests
import pandas as pd

from train_model import onehot_encoder
from data_prepare import cut


# mlflow models serve -m "models:/SOC_rf_model/1" --port 5002
host = "localhost"
port = "5002"

origin_data = pd.read_csv('data.csv', index_col="Coden")

    # 读取数据
Maize = cut(origin_data, 'Maize')
Maize['Yield'] = Maize['Yield'] / 1000
Maize = onehot_encoder(Maize)

data = Maize.sample(n=1)
true_y = data['Yield']
data = data.drop(columns=['Yield'])
request = {
    "columns": [Maize.columns.tolist()],
    "data": [data]
}

headers = {
    "Content-Type": "application/json",
}

_data = {
    "columns": [
        "Year",
        "Month",
        "DayofMonth",
        "DayofWeek",
        "CRSDepTime",
        "CRSArrTime",
        "UniqueCarrier",
        "FlightNum",
        "ActualElapsedTime",
        "Origin",
        "Dest",
        "Distance",
        "Diverted",
    ],
    "data": [[1987, 10, 1, 4, 1, 556, 0, 190, 247, 202, 162, 1846, 0]],
}

## Pause to let server start
time.sleep(5)

while True:
    try:
        resp = requests.post(
            url=f"http://{host}:{port}/invocations",
            data=json.dumps({"dataframe_split": request}),
            headers=headers,
        )
        print("Classification: %s" % ("ON-Time" if resp.text == "[0.0]" else "LATE"))
        break
    except Exception as e:
        errmsg = f"Caught exception attempting to call model endpoint: {e}"
        print(errmsg, end="")
        print("Sleeping")
        time.sleep(20)
