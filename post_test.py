
import json
import time
import requests
import pandas as pd

from train_model import onehot_encoder
from data_prepare import cut


# mlflow models serve -m "models:/SOC_rf_model/3" --port 5002
host = "localhost"
port = "5002"

origin_data = pd.read_csv('data.csv', index_col="Coden")

# 读取数据
Maize = cut(origin_data, 'Maize')
Maize['Yield'] = Maize['Yield'] / 1000
Maize = onehot_encoder(Maize)


def make_request() -> str:
    data = Maize.sample(n=1)
    true_y = data['Yield'].values[0]
    data = data.drop(columns=['Yield'])

    payload = {"inputs": data.to_dict('records')}
    json_payload = json.dumps(payload)
    return json_payload, true_y

headers = {
    "Content-Type": "application/json",
}

## Pause to let server start
# time.sleep(5)

while True:
    json_payload, true_y = make_request()
    try:
        resp = requests.post(
            url=f"http://{host}:{port}/invocations",
            data=json_payload,
            headers=headers,
        )
        # print("Classification: %s" % ("ON-Time" if resp.text == "[0.0]" else "LATE"))
        pred_data = json.loads(resp.text)["predictions"][0]
        print(f'\nThe true value is {true_y}, \nwhile the predict value is {pred_data:.3f}, \nthe difference is {abs((true_y-pred_data)/true_y)*100:.2f} %.')
        time.sleep(2)
    except Exception as e:
        errmsg = f"Caught exception attempting to call model endpoint: {e}"
        print(errmsg, end="")
        print("Sleeping")
        time.sleep(20)
        

    
